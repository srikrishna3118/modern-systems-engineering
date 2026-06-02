from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)
class Transaction:
    tx_id: str
    idempotency_key: str
    from_account: str
    to_account: str
    amount: int
    created_at: str


def create_transfer(
    conn: sqlite3.Connection,
    *,
    idempotency_key: str,
    from_account: str,
    to_account: str,
    amount: int,
) -> Transaction:
    if amount <= 0:
        raise ValueError("amount must be > 0")
    if from_account == to_account:
        raise ValueError("from and to must differ")

    # TODO (exercise): ensure this is fully idempotent under concurrency.
    existing = conn.execute(
        "SELECT * FROM transactions WHERE idempotency_key = ?",
        (idempotency_key,),
    ).fetchone()
    if existing is not None:
        return Transaction(
            tx_id=existing["tx_id"],
            idempotency_key=existing["idempotency_key"],
            from_account=existing["from_account"],
            to_account=existing["to_account"],
            amount=int(existing["amount"]),
            created_at=existing["created_at"],
        )

    tx_id = uuid4().hex
    created_at = datetime.utcnow().isoformat() + "Z"

    conn.execute("BEGIN")
    try:
        conn.execute(
            "INSERT INTO transactions(tx_id, idempotency_key, from_account, to_account, amount, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (tx_id, idempotency_key, from_account, to_account, amount, created_at),
        )

        # Double-entry: one debit, one credit.
        conn.execute(
            "INSERT INTO entries(tx_id, account, delta, created_at) VALUES (?, ?, ?, ?)",
            (tx_id, from_account, -amount, created_at),
        )
        conn.execute(
            "INSERT INTO entries(tx_id, account, delta, created_at) VALUES (?, ?, ?, ?)",
            (tx_id, to_account, amount, created_at),
        )

        conn.execute(
            "INSERT INTO audit_log(tx_id, event, created_at) VALUES (?, ?, ?)",
            (tx_id, "transfer_created", created_at),
        )

        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise

    return Transaction(
        tx_id=tx_id,
        idempotency_key=idempotency_key,
        from_account=from_account,
        to_account=to_account,
        amount=amount,
        created_at=created_at,
    )


def get_balance(conn: sqlite3.Connection, account: str) -> int:
    row = conn.execute(
        "SELECT COALESCE(SUM(delta), 0) AS bal FROM entries WHERE account = ?",
        (account,),
    ).fetchone()
    return int(row["bal"]) if row is not None else 0
