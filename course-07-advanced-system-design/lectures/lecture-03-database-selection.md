# Lecture 3: Database Selection and Schema Design

## Overview

The database is where scale, consistency, and product requirements meet. This lecture is a selection method: match the access pattern and the correctness requirement first, then the product name. Schema design is part of that choice, because a key you cannot query is a key you will have to redesign under load.

## Topics

### 1. Access pattern before engine

Write the queries the product actually runs:

- Point read by primary key (URL redirect, session lookup).
- Range scan (inbox by time, feed by user).
- Secondary filters and full text ("shoes under $50 in Berlin").
- Multi-row transactions (transfer $100 from A to B).
- Analytics scans over months of events.

An engine that is excellent at one of these is often a poor fit for another. Many production systems use two stores on purpose: one for the transaction, one for the query.

### 2. A practical selection map

| Need | Usually fits | Watch out for |
|------|----------------|---------------|
| Multi-row transactions, strong integrity | Relational (Postgres, MySQL) | Write throughput and vertical ceiling |
| Primary-key reads and writes at very high QPS | Wide-column or key-value (Cassandra, DynamoDB) | Secondary indexes, transactions across keys |
| Document-shaped records that change shape | Document store | Unbounded arrays inside one document |
| Relationships you traverse (social graph) | Graph, or relational with care | Super-nodes |
| Full-text search and ranking | Search index (Lucene / Elasticsearch / OpenSearch) | It is a derived index, not the source of truth |
| Working set on the hot path | In-memory (Redis) | Durability and memory cost |
| Global external consistency | Spanner-class | Cost and write latency |

If the table and the product disagree, believe the access pattern.

### 3. Consistency is a product decision

- **Money, inventory, permissions:** one transaction must move the system from one valid state to another. Use a transactional store and a single partition key when you can.
- **Counts, feeds, presence:** stale by a few seconds is acceptable. A replica or a derived store is appropriate.
- **Uniqueness** (one account per email, one short URL per id) needs an atomic compare-and-set or a unique index. "Check then insert" from application code will race.

Double-entry bookkeeping is a schema that makes an invariant checkable: every transaction's deltas sum to zero. The [payment ledger lab](../../course-06-financial-systems/labs/payment-ledger) and the [Stripe case study](../../case-studies/stripe-payment-system.md) are the concrete versions of this idea.

### 4. Schema choices that survive growth

**Model the primary key as the partition key.** In a sharded store, queries that do not include it become scatter-gather. If the product reads "all orders for a user," the partition key is the user, not the order id. Keep a secondary lookup if you also fetch by order id.

**Avoid hot partitions in the key.** A key of `yyyy-mm-dd` puts today's traffic on one shard. Prefix a high-cardinality id, or write to a bucket (`user_id#day`) and merge on read.

**Bound the row.** A chat document that appends every message forever will eventually exceed practical row or document limits. Store messages as their own rows, partitioned by channel and time bucket. Discord's move away from a single document per channel is this lesson; see [Discord message storage](../../case-studies/discord-message-storage.md).

**Index for the query you run, and know the write cost.** Every secondary index is another write. On a search engine, the inverted index is that trade made on purpose: expensive writes, cheap term lookups. See [Exercise 4](../exercises/04-full-text-search.md).

### 5. Derived data

Treat caches, search indexes, and feed timelines as **derived**. They can be rebuilt from the source of truth.

- Write the source of truth first, then update the derived store, or emit an event and let a consumer update it.
- Make the consumer idempotent. At-least-once delivery will apply the same event twice.
- Plan a rebuild. If the only copy of a field lives in Redis, it is not a cache.

```
  client write
       │
       ▼
  source of truth  ──event──▶  indexer / cache builder  ──▶  derived store
  (transaction)                                              (rebuildable)
```

### 6. Migrations

Schema changes on a large table are availability events. Expand, then contract:

1. Add the new column or table. Deploy code that writes both and reads the old.
2. Backfill.
3. Switch reads to the new shape.
4. Drop the old path only after you have measured it.

Locking `ALTER`s and "we'll reshard over the weekend" are how otherwise sound selections fail in production.

## Key Takeaways

1. **Choose from the access pattern and the invariant**, then the product.
2. **Transactional integrity and global low-latency writes** rarely come from the same store.
3. **The partition key is the schema.** Queries that omit it do not scale.
4. **Derived stores must be rebuildable** and updates must be idempotent.
5. **Migrate by expand-then-contract**, not by a single locking change.

## Further Reading

- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. Chapters on data models and transactions.
- [Google Spanner](../../case-studies/google-spanner-consistency.md) — when global consistency is the requirement.
- [Discord message storage](../../case-studies/discord-message-storage.md) — what happens when a document grows without bound.
