# Lecture 2: Compliance, Fraud, and the Audit Log

## Overview

A ledger that balances is not yet a financial system. Someone will ask who moved the money, a stolen card will try to move it first, and a regulator will ask you to prove both answers months later. This lecture covers the controls around the ledger from [Lecture 1](lecture-01-payments-idempotency-availability.md): reducing what you are in scope for, detecting abuse in time to matter, and keeping a record you cannot quietly rewrite.

## Topics

### 1. Compliance as a scope problem

PCI-DSS is the card-data regime. SOX is the public-company "the numbers are real and the access is controlled" regime. You do not need to memorize the control catalogs. You need the engineering moves that make the catalogs survivable.

- **Do not touch card numbers if you can avoid it.** A processor (Stripe, in the case study) gives you a token. Your database stores the token. The card number lives in a vault you do not administer. Everything that only sees tokens is out of the strictest scope. This is the highest-leverage compliance decision available to an application team.
- **Separate duties.** The person who can deploy the ledger service should not be the only person who can read the production database and also approve a payout destination change. Split the roles. Log the assumption of each role.
- **Retain what the rule says, and no more.** Some records must be kept for years. Some data (a card number, a national id) should not be kept at all. "Keep everything forever in the warehouse" fails both.
- **Access is a control, not a courtesy.** Production data access is time-limited, justified, and logged. A shared admin password is a finding, not a shortcut.

Design the system so the common path never sees the sensitive field. Bolting encryption on after every service has already copied the column into its own database does not shrink scope.

### 2. Fraud detection

Fraud is a real-time decision with a late label. The card is stolen on Monday. The chargeback arrives in three weeks. The system has to decide in the milliseconds before authorization, and learn in the weeks after.

- **Decide on the authorization path,** with a tight budget (tens of milliseconds). Fetch a few features (velocity of this card, this device, this address), score, and return approve, step-up (ask for a second factor), or decline. A timeout must have a written default. For a new product, declining on timeout is safer and will annoy legitimate users; approving on timeout will be the incident. Pick it deliberately, per [the serving lecture](../../course-04-ai-systems/lectures/lecture-02-serving-mlops-monitoring.md).
- **Features are counts over short windows** ("cards tried from this device in 10 minutes"), which is the windowed aggregation from [Course 05](../../course-05-realtime-systems/lectures/lecture-01-events-streams-windows.md) with a product reason. The same event stream feeds the model later.
- **Step-up is the middle.** A decline is expensive (lost order, angry customer). A silent approve is expensive (you eat the chargeback). A challenge is the valve.
- **Rules and models together.** A rule ("more than 5 failed attempts in a minute, block") is understandable and fast. A model catches what you did not write down. Rules are also how you react today, before a retrain exists.
- **Adversaries adapt.** A rule you publish in an error message will be routed around by tomorrow. Do not explain the exact threshold to the client.

The [Shopify ML platform](../../case-studies/shopify-ml-platform.md) case is the platform version of this: fraud models retrain often, and a false positive is a merchant who cannot sell.

### 3. Audit logging

An audit log answers "who changed this, when, from where, and what did they change." It is not the application log, and it is not a column you update in place.

- **Append only.** A correction is a new record that points at the old one. Update and delete are not operations the application role has.
- **Same transaction as the change** when the change is in your database, so you cannot commit a transfer and fail to record it. The lab writes `audit_log` in the same transaction as the entries. `GET /audit` reads that table back.
- **Cover the sensitive actions,** not every GET. Money movement, permission changes, payout-destination changes, admin access to cardholder data. A log of every health check is noise that hides the payout change.
- **Include the actor and the reason.** A user id, an admin id, the idempotency key, the request id, the source IP. "The system did it" is not an actor.
- **Protect the log from the people it watches.** Shipping it to a store the application cannot delete from, in another account, is the usual shape. If the attacker who owns the app can also truncate the log, you do not have a log.

### 4. Integrity

- **Constraints in the database,** not only in the service. A unique idempotency key, a check that amount is positive, foreign keys from entries to transactions. A bug that bypasses the service should still fail the write.
- **Continuous reconciliation.** Sum of entries is zero, per transaction and per day. Sum of ledger balances equals cash at the bank, within the timing difference you have documented. Alert on a mismatch. Do not discover it at the end of the quarter.
- **Immutable artifacts for the outside world.** Statements and webhook events have ids and are replayable. Regenerating a statement so that it quietly differs from the one the customer downloaded is a serious bug, not a convenience.

### 5. What not to build

Do not build your own card vault, your own public-key infrastructure for the webhook signatures if a library already does it correctly, or your own fraud model before you have the event log and the labels. Do build the idempotent ledger, the append-only audit, the reconciliation job, and the refusal to approve when you are blind. Those four are the system. The rest is a vendor plus a feature pipeline.

## Key Takeaways

1. **Tokenize card data** so most of the system never sees it. Scope is a design choice.
2. **Fraud decides in milliseconds and learns in weeks.** Write the timeout default down. Prefer a challenge over a silent approve.
3. **The audit log is append-only, written in the same transaction, and stored where the app cannot delete it.**
4. **Reconcile continuously.** A ledger that is never summed is a ledger you hope is right.
5. **Enforce invariants in the database.** Application checks are not the last line.

## Further Reading

- [Stripe payment system](../../case-studies/stripe-payment-system.md) — tokens, idempotency, and the ledger.
- [Payment ledger lab](../labs/payment-ledger) — the audit row and the zero-sum check.
- [Shopify ML platform](../../case-studies/shopify-ml-platform.md) — fraud as a model-serving problem.
- [Course 07, Lecture 5](../../course-07-advanced-system-design/lectures/lecture-05-security-zero-trust.md) — identity and trust boundaries around these controls.
