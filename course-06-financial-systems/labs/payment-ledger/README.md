# Lab: Payment Ledger – Financial Transaction System

## Overview
Build a double-entry payment ledger with idempotent transaction processing. This lab covers transactional integrity, idempotency keys, audit logging, and reconciliation.

## Architecture

```
API Client --> Payment API --> Ledger Service --> PostgreSQL (double-entry ledger)
                                              --> Audit Log
                                              --> Notification Service
```


## Learning Objectives
- Implement double-entry bookkeeping for financial transactions.
- Use idempotency keys to prevent duplicate charges.
- Build an audit trail that satisfies compliance requirements.

## Prerequisites
- Python 3.10+
- Basic understanding of SQL and database transactions.

## Getting Started

1. Install dependencies:
   ```bash
   cd starter-code
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Initialize the database:
   ```bash
   python init_db.py --db ledger.db
   ```
3. Start the API server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
4. Create a test transaction:
   ```bash
   curl -X POST http://localhost:8000/transactions \
     -H "Idempotency-Key: test-001" \
     -d '{"from": "account_a", "to": "account_b", "amount": 100}'
   ```

## Validation

```bash
# Replay the same request; the response should be identical and no duplicate entries created.
curl -s -X POST http://localhost:8000/transactions \
  -H "Idempotency-Key: test-001" \
  -H 'Content-Type: application/json' \
  -d '{"from": "account_a", "to": "account_b", "amount": 100}' | jq

# Check balances; they should sum to 0 across both accounts.
curl -s http://localhost:8000/accounts/account_a/balance | jq
curl -s http://localhost:8000/accounts/account_b/balance | jq
```

## Experiment

Send the same transaction concurrently (e.g. two terminals) with the same idempotency key and confirm the ledger stays consistent.

## Deliverables
- A working ledger API that correctly debits and credits accounts.
- Idempotency demonstrated by replaying the same request and verifying no duplicate entry.
- An audit log showing all transaction records.

## Solution
See the `solution/` directory for a reference implementation.

