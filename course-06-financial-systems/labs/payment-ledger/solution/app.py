from __future__ import annotations

import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from db import connect
from ledger import create_transfer, get_balance


DB_PATH = os.getenv("LEDGER_DB", "ledger.db")

app = FastAPI(title="Payment Ledger")


class TransferRequest(BaseModel):
    from_: str = Field(alias="from", min_length=1)
    to: str = Field(min_length=1)
    amount: int = Field(gt=0)


@app.post("/transactions")
def post_transaction(
    payload: TransferRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="missing_idempotency_key")

    conn = connect(DB_PATH)
    try:
        tx = create_transfer(
            conn,
            idempotency_key=idempotency_key,
            from_account=payload.from_,
            to_account=payload.to,
            amount=payload.amount,
        )
    finally:
        conn.close()

    return {
        "tx_id": tx.tx_id,
        "idempotency_key": tx.idempotency_key,
        "from": tx.from_account,
        "to": tx.to_account,
        "amount": tx.amount,
        "created_at": tx.created_at,
    }


@app.get("/accounts/{account}/balance")
def get_account_balance(account: str):
    conn = connect(DB_PATH)
    try:
        bal = get_balance(conn, account)
    finally:
        conn.close()
    return {"account": account, "balance": bal}
