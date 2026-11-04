# Lecture 1: Designing for Scale

## Overview

Scale is a set of constraints, not a badge. This lecture is the working method for Course 07: name the bottleneck, estimate it, then pick the smallest design that survives the next order of magnitude. Horizontal and vertical scaling are the first fork. Everything later (regions, databases, rate limits) hangs off that choice.

## Topics

### 1. Start from the workload, not the diagram

Before drawing boxes, write four numbers:

- **QPS** for reads and writes, including peak (usually 2–5× the average).
- **Payload size** for the hot path.
- **Working set** that must stay in memory to hit the latency target.
- **Growth horizon** (6 months, 2 years). Design for the horizon, not for infinity.

```
requests/day ÷ 86,400 = average QPS
average QPS × peak factor = provisioned QPS
QPS × bytes/request = bandwidth
records × bytes/record × replicas = storage
```

If you cannot fill in the numbers, you do not yet know whether you need to shard.

### 2. Vertical scaling (scale up)

Add CPU, memory, disk, or network to one machine.

- **Use it when** the bottleneck is a single hot process, the dataset fits on one box, and coordination would cost more than the hardware.
- **It fails when** you hit a hardware ceiling, a reboot becomes downtime, or one failure takes the whole service with it.
- **Typical ceiling:** a well-tuned database on a large instance handles tens of thousands of simple queries per second. Past that, more cores often lose to lock and I/O contention.

Vertical scaling is the right first move for a new product and for components that are hard to split (a single-writer ledger, a primary index).

### 3. Horizontal scaling (scale out)

Add machines that do the same job. This only works if requests are independent or you can partition the state they touch.

**Stateless services** scale by putting a load balancer in front of identical instances. Session state moves to a cookie, a token, or a shared store.

**Stateful services** scale by partitioning:

- **Range:** keys A–M on shard 1. Simple, but a celebrity or a time-range becomes a hot shard.
- **Hash:** `hash(key) % N`. Even spread, painful reshard when N changes. Consistent hashing and virtual nodes reduce the data you move.
- **Directory:** a lookup table maps key → shard. Flexible, and the directory itself must be cached and highly available.

```
                    ┌──────────┐
 client ───────────▶│ balancer │
                    └────┬─────┘
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
        shard A       shard B       shard C
        (hash 0)      (hash 1)      (hash 2)
```

### 4. The scale-out tax

Horizontal scaling is not free. You pay with:

- **Partial failure.** Some shards are up, some are not. Clients need timeouts, retries, and idempotency.
- **Hot keys.** A uniform hash still melts if one key is 10,000× hotter than the rest. Isolate hot keys onto their own shard or cache them.
- **Cross-shard work.** Joins, global uniqueness, and multi-row transactions become application problems. Prefer a partition key that keeps a user’s writes on one shard.
- **Operational load.** Deploys, capacity, and debugging multiply by the number of instances.

A useful rule: scale the stateless tier horizontally first, cache the read path, and only shard the database when a single primary cannot meet write throughput or storage.

### 5. A scaling ladder

Apply changes in this order. Stop when the numbers fit.

1. Measure. Most “scale” problems are one slow query or a missing index.
2. Scale the database vertically and add read replicas for read-heavy paths.
3. Add a cache for the hot working set. Accept that invalidation is part of the design.
4. Split by workload (browse vs. checkout, reads vs. writes) so they scale separately.
5. Shard the state that is still too big, using a key you will not have to change.
6. Push work to the edge (CDN, regional caches) when the bottleneck is geography or bandwidth, not CPU.

### 6. Worked sketch: read-heavy redirect service

100 million new URLs per day is about **1,160 writes/sec**. At a 100:1 read ratio that is about **116,000 reads/sec**.

- Writes fit on a modest primary, especially if IDs are generated in batches so the database is not the ID allocator.
- Reads do not. A cache in front of the mapping, plus replicas, is the design. The database is the source of truth, not the serving path.
- Storage over five years at ~200 bytes per row is on the order of **tens of terabytes** before replication. That is a sharding problem later, not on day one.

The full worked design is in [Exercise 1](../exercises/01-url-shortener.md).

## Key Takeaways

1. **Estimate first.** QPS, payload, working set, and horizon decide the architecture.
2. **Scale up until a single machine is the risk**, then scale out.
3. **Stateless tiers scale by copying.** Stateful tiers scale by partitioning.
4. **Hot keys and cross-shard transactions** are the usual reasons a sharded design fails.
5. **Climb the ladder.** Caching and workload splits come before exotic sharding.

## Further Reading

- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. Chapters on partitioning and replication.
- [Lecture 2: Building Scalable Systems](../../course-01-engineering-foundations/lectures/lecture-02-building-scalable-systems.md) — caching, replication, and load balancing foundations.
- [Shopify Flash Sale Scaling](../../case-studies/shopify-flash-sale-scaling.md) — separating browse traffic from checkout under a spike.
