# Lab: Payment Ledger – Financial Transaction System

## Overview
Build a double-entry payment ledger with idempotent transaction processing. This lab covers transactional integrity, idempotency keys, audit logging, and reconciliation.

## Architecture

```
API Client --> Payment API --> Ledger Service --> PostgreSQL (double-entry ledger)
                                              --> Audit Log
                                              --> Notification Service
```

See `architecture.png` for a detailed component diagram.

## Learning Objectives
- Implement double-entry bookkeeping for financial transactions.
- Use idempotency keys to prevent duplicate charges.
- Build an audit trail that satisfies compliance requirements.

## Prerequisites
- Python or Node.js.
- Docker and Docker Compose installed locally.
- Basic understanding of SQL and database transactions.

## Getting Started

1. Start the database:
   ```bash
   docker-compose up -d postgres
   ```
2. Run database migrations:
   ```bash
   python manage.py migrate
   ```
3. Review the starter code in `starter-code/` and implement the `TODO` sections in `ledger.py`.
4. Start the API server:
   ```bash
   python app.py
   ```
5. Create a test transaction:
   ```bash
   curl -X POST http://localhost:8000/transactions \
     -H "Idempotency-Key: test-001" \
     -d '{"from": "account_a", "to": "account_b", "amount": 100}'
   ```

## Deliverables
- A working ledger API that correctly debits and credits accounts.
- Idempotency demonstrated by replaying the same request and verifying no duplicate entry.
- An audit log showing all transaction records.

## Solution
See the `solution/` directory for a reference implementation.
