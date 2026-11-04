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


def _row_to_tx(row: sqlite3.Row) -> Transaction:
    return Transaction(
        tx_id=row["tx_id"],
        idempotency_key=row["idempotency_key"],
        from_account=row["from_account"],
        to_account=row["to_account"],
        amount=int(row["amount"]),
        created_at=row["created_at"],
    )


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

    conn.execute("BEGIN")
    try:
        existing = conn.execute(
            "SELECT * FROM transactions WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
        if existing is not None:
            conn.execute("COMMIT")
            return _row_to_tx(existing)

        tx_id = uuid4().hex
        created_at = datetime.utcnow().isoformat() + "Z"

        conn.execute(
            "INSERT INTO transactions(tx_id, idempotency_key, from_account, to_account, amount, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (tx_id, idempotency_key, from_account, to_account, amount, created_at),
        )

        conn.execute(
            "INSERT INTO entries(tx_id, account, delta, created_at) VALUES (?, ?, ?, ?)",
            (tx_id, from_account, -amount, created_at),
        )
        conn.execute(
            "INSERT INTO entries(tx_id, account, delta, created_at) VALUES (?, ?, ?, ?)",
            (tx_id, to_account, amount, created_at),
        )

        # Sanity check: double-entry must net to zero.
        row = conn.execute(
            "SELECT SUM(delta) AS net FROM entries WHERE tx_id = ?",
            (tx_id,),
        ).fetchone()
        net = int(row["net"]) if row is not None else 0
        if net != 0:
            raise RuntimeError("double_entry_violation")

        conn.execute(
            "INSERT INTO audit_log(tx_id, event, created_at) VALUES (?, ?, ?)",
            (tx_id, "transfer_created", created_at),
        )
        conn.execute("COMMIT")

        return Transaction(
            tx_id=tx_id,
            idempotency_key=idempotency_key,
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            created_at=created_at,
        )
    except Exception:
        conn.execute("ROLLBACK")
        raise


def list_audit(conn: sqlite3.Connection, limit: int = 50) -> list[dict]:
    rows = conn.execute(
        "SELECT audit_id, tx_id, event, created_at FROM audit_log ORDER BY audit_id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [
        {
            "audit_id": row["audit_id"],
            "tx_id": row["tx_id"],
            "event": row["event"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def get_balance(conn: sqlite3.Connection, account: str) -> int:
    row = conn.execute(
        "SELECT COALESCE(SUM(delta), 0) AS bal FROM entries WHERE account = ?",
        (account,),
    ).fetchone()
    return int(row["bal"]) if row is not None else 0
