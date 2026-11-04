# Case Study: Stripe Payment System – Financial Transactions at Scale

## Overview

The course-assigned write-up is [Stripe Payment System](stripe-payment-system.md). This note is the shorter companion and covers the same system.

Stripe processes hundreds of billions of dollars in payments annually for millions of businesses. Its payment infrastructure must ensure idempotency, consistency (money never created/destroyed), PCI-DSS compliance, and 99.99%+ reliability.

## Key Challenges

- **Idempotency**: Network failures must not cause duplicate charges; same request must be idempotent
- **Consistency**: Double-entry ledger must balance; audit trails must be immutable
- **PCI Compliance**: Payment data is heavily regulated; tokenization minimizes compliance scope
- **Global Reliability**: Payment systems must be available worldwide; failures are costly for merchants

## Architecture Highlights

- **Idempotency Keys**: Clients provide an idempotency key; Stripe stores key + response and returns cached result on retries
- **Double-Entry Ledger**: All transactions recorded as pairs (debit/credit); automatically audit trailing; balance is checkable
- **Payment Tokenization**: Card data stored securely in isolated "Vault"; rest of system uses tokens, minimizing PCI scope
- **Rate Limiting**: Token-bucket algorithm at API gateway prevents overload and DDoS
- **Reconciliation**: Background jobs match API ledger with payment processor ledger; catch discrepancies early

## Technology Stack

- Ruby (API servers), Scala (batch processing), Go (infrastructure)
- MySQL (ledger), Kafka (event stream), Redis (rate limiting)
- AWS multi-region active-active, dedicated PCI compliance environment

## Lessons Learned

1. **Idempotency must be designed in from the start** — Retrofitting idempotency is hard; built-in idempotency keys are essential
2. **Double-entry ledger = audit trail + consistency** — Every transaction creates a debit/credit pair; balance is a consistency invariant
3. **Tokenization minimizes PCI scope** — Isolating payment data enables minimal PCI compliance scope for the rest of the system
4. **Reconciliation jobs are essential** — Distributed systems have transient failures; background reconciliation catches and fixes discrepancies
5. **Rate limiting protects both customer and system** — Prevents individual customers from overloading the system; protects against attacks

## Further Reading

- [Stripe Blog: Building Stripe](https://stripe.com/blog/engineering)
- [Designing for Idempotency (Stripe Engineering)](https://stripe.com/blog/idempotency)
