# Case Study: Kafka Event Streaming – Distributed Append-Only Logs at Scale

## Overview

Apache Kafka, developed at LinkedIn, has become the de facto standard for event streaming. It stores and processes terabytes of events per day across thousands of organizations, enabling real-time data pipelines and stream processing applications.

## Key Challenges

- **Throughput**: Millions of messages/sec per broker; terabytes/day per cluster
- **Durability**: Messages persist for days/weeks; zero loss during failures
- **Latency**: Sub-100ms end-to-end for real-time applications
- **Exactly-Once Semantics**: Transactional processing; messages processed exactly once despite failures

## Architecture Highlights

- **Append-Only Logs**: Topics are divided into partitions; each partition is an immutable, append-only log on disk
- **Broker Replication**: Each partition is replicated across 3+ brokers; ISR (In-Sync Replicas) guarantee durability
- **Consumer Groups**: Multiple consumers in a group parallelize work; each partition assigned to one consumer
- **Distributed Transactions**: Kafka transactions (KIP-98) enable exactly-once semantics across partitions

```
┌─────────────────────────────────────────────┐
│           Kafka Cluster                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Broker 1 │  │ Broker 2 │  │ Broker 3 │  │
│  │          │  │          │  │          │  │
│  │Part 0 ───┼──┼→ Part 0 ─┼──┼→ Part 0  │  │ Topic A
│  │Part 1    │  │  Part 1  │  │  Part 1  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│       ↑              ↑              ↑        │
│       └──────────────┼──────────────┘        │
│         All replicas in sync (ISR)          │
└─────────────────────────────────────────────┘
        ↑                           ↓
    Producers            Consumer Groups
```

## Technology Stack

- Broker: JVM-based, custom storage engine
- Consumer APIs: Java, Python, Go, Rust
- Ecosystem: Kafka Connect (ingestion), Kafka Streams (stream processing), KSQL
- Cloud: Confluent Cloud, Amazon MSK

## Lessons Learned

1. **Immutable append-only logs are a foundation for streaming** — Simple, durable, and amenable to replication
2. **Partitioning enables parallelism without distributed consensus** — Each partition is owned by one consumer; no coordination
3. **Replication latency matters** — In-Sync Replica (ISR) design ensures durability without waiting for slow replicas
4. **The log abstraction is remarkably versatile** — Log-based architectures power transactions, snapshots, and stream processing

## Where this fits in the curriculum

- [Course 07, Exercise 2: Notifications](../course-07-advanced-system-design/exercises/02-notification-system.md) — the log between accept and channel workers.
- [Course 02 Kafka lab](../course-02-distributed-systems/labs/kafka-pipeline).
- Course pointer: [course 07 wrapper](../course-07-advanced-system-design/case-studies/kafka-event-streaming.md).

## Further Reading

- [The Design of Kafka](https://docs.confluent.io/kafka/design/index.html)
- [Exactly-Once Delivery and Transactional Messaging Refinements in Apache Kafka (KIP-98)](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging+Refinements)
