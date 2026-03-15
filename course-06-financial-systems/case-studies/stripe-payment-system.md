# Case Study: Stripe Payment System

## Overview
Stripe processes hundreds of billions of dollars in payments annually for millions of businesses. This case study examines how Stripe engineers its payment infrastructure for extreme reliability, idempotency, and compliance while maintaining developer-friendly APIs.

## Key Challenges
- **Idempotency**: Preventing duplicate charges in the face of network retries and client errors.
- **Consistency**: Ensuring money is never created or destroyed, only moved.
- **Compliance**: Meeting PCI-DSS requirements for handling cardholder data.
- **Global reliability**: Maintaining high availability for businesses and their customers worldwide.

## Architecture Highlights

### Idempotency Keys
Every Stripe API request that creates or modifies a resource accepts an `Idempotency-Key` header. Stripe stores the key and the resulting response for a rolling window. If the same key is seen again (e.g., due to a network timeout and retry), Stripe returns the stored response without re-executing the operation. This prevents double charges.

### Charges and the Ledger
Stripe maintains a double-entry ledger at its core. Every charge creates a corresponding set of ledger entries: a debit from the card network and a credit to Stripe's internal balance, with subsequent credits to the merchant's balance. The ledger is append-only and immutable for audit purposes.

### PCI-DSS Compliance and Vaulting
Cardholder data (card numbers, CVVs) is handled in a dedicated, highly isolated environment — Stripe's "Vault". The rest of Stripe's systems interact with tokenized references to cards, never with raw card data. This dramatically reduces the PCI-DSS compliance scope for downstream systems.

### Distributed Rate Limiting
Stripe exposes public APIs and must protect backend services from both accidental and malicious traffic spikes. Rate limits are enforced at the API gateway level using token bucket algorithms backed by Redis clusters.

### Failure Handling and Retries
Stripe uses exponential backoff with jitter for internal service retries. Financial operations that fail partway through are reconciled by background jobs that detect and resolve inconsistent states (e.g., a charge that reached the card network but whose result was not received by Stripe).

## Technology Stack
- **Languages**: Ruby, Scala, Go
- **Databases**: MySQL (primary transactional store), Redis (rate limiting, ephemeral state)
- **Infrastructure**: AWS, multi-region active-active deployment
- **Compliance**: Dedicated PCI-DSS environment for card vaulting

## Lessons Learned
1. Idempotency is not optional in payment systems — it must be designed in from the start.
2. A double-entry ledger provides a built-in audit trail and a natural consistency check.
3. Minimizing the PCI scope through tokenization dramatically simplifies compliance across the rest of the system.
4. Reconciliation jobs are essential: assume any distributed operation can fail partway through.

## Further Reading
- [Stripe Engineering Blog – Idempotency](https://stripe.com/blog/idempotency)
- [Stripe Engineering Blog – Online Migrations at Scale](https://stripe.com/blog/online-migrations)
- [Stripe Engineering Blog – Scaling your API with Rate Limiters](https://stripe.com/blog/rate-limiters)
