# Lecture 3: Partitioning and Fault Tolerance

## Overview

Lecture 1 introduced replication, failure modes, and consensus. This lecture is the operational half of the Course 02 syllabus: how you split data so one machine is not the ceiling, and how you keep serving when pieces fail. Global product design on top of these mechanisms is [Course 07](../../course-07-advanced-system-design/lectures/lecture-02-global-multi-region.md).

## Topics

### 1. Partitioning

Partition when one node cannot hold the working set or the write rate. Not before: a single primary plus a replica is easier to reason about and easier to back up.

- **Hash the key** you actually look up. `user_id` if every query is "this user's orders." A query that does not include the partition key is a scatter across every shard, and it will become the outage.
- **Avoid monotonic keys as the only shard key.** Inserting on a timestamp puts all of today's writes on one shard. Mix in a high-cardinality id.
- **Plan the move.** Adding a shard with `hash % N` moves almost every key. Consistent hashing, or a directory that maps ranges to shards, moves a fraction. Either way, copy, then flip reads, then flip writes, then delete the old copy. Do not flip first.
- **Hot keys are not solved by more shards.** A celebrity account is one key. Give it its own shard, cache it, or split the key into buckets (`user_id#bucket`) and merge on read.

[Discord's storage history](../../case-studies/discord-message-storage.md) is a partitioning story: the original document shape stopped working, and the key became channel plus time.

### 2. Fault tolerance is a behavior, not a component

For each dependency, write down the timeout, the retry, and what happens when retries are exhausted.

- **Timeouts** are shorter than the caller's timeout, so a slow dependency becomes an error you can handle instead of a queue of waiting requests. A default of "no timeout" is a failure mode.
- **Retry** only idempotent operations, with jittered backoff, and with a limit. Retrying a non-idempotent charge, immediately, from every client, is how a blip becomes an outage. The [reliability lab](../../course-01-engineering-foundations/labs/reliability-toolkit) measures the latency you pay for the retries.
- **A circuit breaker** stops calling a dependency that is failing, so you spend your threads on work that can succeed, and you probe occasionally to see if it has recovered.
- **Bulkheads** isolate pools. The pool that calls the payment provider is not the pool that serves health checks. One saturated dependency should not exhaust every thread in the process.
- **Load shedding** refuses work you cannot do, early, with a clear error. A server at 100% CPU that still accepts requests is a server whose tail latency is already unusable.

### 3. Detecting failure

You cannot tell a dead process from a slow network. A timeout is a guess. Consensus systems (from Lecture 1) treat failure as "did not respond to the vote," and they only promote a new leader with a majority so two leaders cannot both believe they are in charge. Carry that suspicion into application failover: fence the old writer. A database primary that is merely unreachable from you may still be writing.

Health checks should test the thing you actually need. A process that answers `/health` from memory while its database is gone will stay in the load balancer and fail every real request. Readiness should fail when the dependency required to serve is gone. Liveness should fail only when restarting the process might help. Restarting will not bring the database back, and a liveness check that depends on the database will restart every pod at once.

### 4. Multi-region, at this course's depth

A second region is another copy of the failure domain, far away.

- Replicate asynchronously if you can tolerate losing the last few seconds on failover (most derived data, most feeds).
- Replicate synchronously, or pin writes to one region, if you cannot (the ledger, inventory you promised not to oversell).
- Practice the failover. A replica you have never promoted is a backup in theory.
- Know which region is allowed to write a given key, and how the old region loses that right.

The mechanisms are replication lag, fencing, and a witness for quorum. The product choices (active-passive versus per-user home regions) are Course 07. [Spanner](../../case-studies/google-spanner-consistency.md) is what it costs to refuse that choice and offer global strong consistency instead. [AWS cells](../../case-studies/aws-cell-architecture.md) are the complementary idea: even inside one region, do not put every customer in one failure domain.

## Key Takeaways

1. **Partition by the key you query, and plan how data moves when you add a shard.**
2. **Hot keys ignore extra shards.** Isolate them.
3. **Timeout, bounded retry with jitter, and a breaker** are the default dependency policy. Retry only idempotent work.
4. **Readiness reflects the dependency. Liveness reflects the process.** Fencing reflects the suspicion that "unreachable" is not "dead."
5. **A second region copies the problem unless you have decided what a lagging replica is allowed to do.**

## Further Reading

- [Lecture 1](lecture-01-distributed-fundamentals.md) — CAP, Raft, replication.
- [Reliability lab](../../course-01-engineering-foundations/labs/reliability-toolkit)
- [Discord message storage](../../case-studies/discord-message-storage.md)
- [Course 07, Lecture 2](../../course-07-advanced-system-design/lectures/lecture-02-global-multi-region.md)
