# Lecture 1: Payments, Idempotency, and Staying Available

## Overview

Financial systems fail in one direction that other systems do not: they can create or destroy value by losing a message, retrying one, or being unavailable at the moment of a charge. This lecture covers the transaction path, idempotency, and the availability choices that do not corrupt a ledger. The [payment ledger lab](../labs/payment-ledger) is the smallest version of the invariant.

## Topics

### 1. What a payment system has to guarantee

Three properties, and they are in tension with uptime:

- **No lost money and no invented money.** Every movement is a debit and a credit of the same amount. The sum of a transaction is zero. The sum of the ledger is the sum of what customers brought in. This is an invariant you can check, and you should check it continuously, not in an annual audit.
- **No double charge.** A retry, a timeout, or a user double-click charges once.
- **A durable record** of who did what, that you cannot quietly edit. Corrections are new transactions, not updates.

[Stripe](../../case-studies/stripe-payment-system.md) is the production telling of these three. The lab is the schema: `transactions` plus `entries` that must net to zero, plus an `audit_log` row written in the same commit.

### 2. The payment path

```
 client ──Idempotency-Key──▶ API ──▶ ledger (one transaction)
                                 ├──▶ card network / bank (external, slow, ambiguous)
                                 └──▶ outbox ──▶ webhooks, email, ledger readers
```

Split the path into the part you control and the part you do not.

- **You control the ledger.** It commits in your database, under a transaction, with the idempotency key.
- **You do not control the card network.** A call to it can succeed, fail, or succeed without you seeing the response. That third case is the whole design problem. You store the intent before the call, you store the outcome after, and a sweeper asks the network about anything left in the middle. You do not "retry the charge" blindly.

Authorization (is this card good for this amount) and capture (move the money) are different steps in real card systems. Collapsing them is fine for the lab and wrong for a product that needs to place a hold. Model them as two ledger events if you need both: a hold, then a capture or a release.

### 3. Idempotency

A client generates a unique key per logical operation and sends it on every retry. The server:

1. Looks up the key.
2. If it has seen it, returns the stored response and does nothing else.
3. If it has not, does the work and stores the response under that key, in the same transaction as the work.

The key is not a hash of the request body that you recompute loosely. It is an id the client chose for that attempt's intent. The same key with a different body is a conflict (`409`), not a second charge. Keys expire on a window you publish (24 hours is a common choice); after that, a retry is a new operation and the client must not reuse the key.

The scope of the key is the operation and the account, not a global counter. Two different merchants can use the same UUID without colliding if the unique constraint is `(merchant, key)`.

At-least-once delivery of the *outcome* (webhooks to the merchant) uses the same idea. The merchant dedupes on your event id. You retry until you receive a success, and you sign the webhook so a third party cannot forge "payment succeeded."

"Exactly once" across your database and a card network does not exist as a single commit. What exists is: the ledger transition is exactly once because of the idempotency key and the transaction, and the external side is reconciled until it matches the ledger. Reconciliation is the product. Anyone who tells you the network gave them exactly-once is describing this pattern in fewer words.

### 4. Availability without corrupting the ledger

A ledger wants a single ordered writer per account (or per shard of accounts). That is in conflict with "always accept a write in any region."

- **Prefer refusing the write** over accepting it in two places. A payment API that returns 503 and asks the client to retry is correct. A payment API that applies the debit twice is not. This is the opposite of a social feed, which should usually serve a stale read.
- **Shard by account** so one hot account does not order the whole world, and so one shard's failure refuses only that shard's accounts. The refusal has to be visible. Silent queueing of charges during a partition is how you discover, after the fact, that you captured twice.
- **Read replicas** can serve balance *displays* if the UI says the figure may be a few seconds old. They must not serve the balance check that decides whether to approve a debit, unless you enjoy overdrafts.
- **Backups are not a failover plan** unless you have restored one. Test the restore, and know the minute you would lose.

Multi-region active-active for a ledger means a conflict rule for "both regions debited the last $10." There is no good automatic rule. Pin an account to a home region, and fail over the shard with a fence so the old region cannot keep writing. [Course 07's multi-region lecture](../../course-07-advanced-system-design/lectures/lecture-02-global-multi-region.md) covers the fence. Use it. Do not invent a CRDT for money.

### 5. The lab's invariant

In [payment-ledger](../labs/payment-ledger), `create_transfer` writes the transaction, both entries, and the audit row in one transaction, and it returns the original row when the idempotency key repeats. The smoke test checks the two things that matter: a replay does not move money again, and the two balances sum to zero. Hold onto those two checks when you add a real external network. The network call sits *between* "intent recorded" and "outcome recorded," and the invariant still has to hold.

## Key Takeaways

1. **Debits and credits of one transaction sum to zero.** Check that invariant in the write path and again as a continuous job.
2. **Idempotency keys make retries safe.** Same key, same body, same response. Same key, different body, conflict.
3. **External networks are ambiguous.** Record intent, call, record outcome, sweep what is left in between. Do not blind-retry a charge.
4. **Refuse writes you cannot order.** A 503 is a better failure than a double debit.
5. **Replicas can show a stale balance. They cannot approve one.**

## Further Reading

- [Stripe payment system](../../case-studies/stripe-payment-system.md)
- [Payment ledger lab](../labs/payment-ledger)
- [Lecture 2](lecture-02-compliance-fraud-audit.md) — the record, the attacker, and the regulator.
