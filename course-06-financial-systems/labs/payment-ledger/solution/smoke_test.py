"""Create a transfer, replay it, and check the ledger still balances.

    python init_db.py --db /tmp/ledger-smoke.db
    LEDGER_DB=/tmp/ledger-smoke.db python smoke_test.py
"""

import os
import tempfile

from fastapi.testclient import TestClient

from db import connect
from init_db import SCHEMA


def main():
    handle = tempfile.NamedTemporaryFile(prefix="ledger-", suffix=".db", delete=False)
    handle.close()
    os.environ["LEDGER_DB"] = handle.name

    conn = connect(handle.name)
    conn.executescript(SCHEMA)
    conn.close()

    # Import after LEDGER_DB is set. app reads the path at import time.
    import importlib
    import app as app_module

    importlib.reload(app_module)
    client = TestClient(app_module.app)

    body = {"from": "account_a", "to": "account_b", "amount": 100}
    headers = {"Idempotency-Key": "test-001"}
    first = client.post("/transactions", json=body, headers=headers)
    second = client.post("/transactions", json=body, headers=headers)
    if first.status_code != 200 or second.status_code != 200:
        raise SystemExit((first.status_code, first.text, second.status_code, second.text))
    if first.json()["tx_id"] != second.json()["tx_id"]:
        raise SystemExit("idempotency key created two transactions")

    bal_a = client.get("/accounts/account_a/balance").json()["balance"]
    bal_b = client.get("/accounts/account_b/balance").json()["balance"]
    if bal_a != -100 or bal_b != 100 or bal_a + bal_b != 0:
        raise SystemExit(f"balances {bal_a} {bal_b}")

    audit = client.get("/audit").json()["events"]
    if len(audit) != 1 or audit[0]["event"] != "transfer_created":
        raise SystemExit(f"audit log {audit}")

    missing = client.post("/transactions", json=body)
    if missing.status_code != 400:
        raise SystemExit("expected 400 without an idempotency key")

    print("ledger smoke ok")


if __name__ == "__main__":
    main()
