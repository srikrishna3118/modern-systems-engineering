# Course 02: Distributed Systems

**Duration:** 5 weeks. **Prerequisite:** Course 01.

## Topics

- Service discovery
- RPC and gRPC
- Event-driven architecture
- Data sharding
- Fault tolerance
- Multi-region systems

## Learning Objectives

- Explain why a distributed call can succeed and still be invisible to the caller, and design for that.
- Choose a partition key and say what happens to order and hot keys.
- Build a small gRPC service and a small Kafka pipeline, and run the reference solutions.

## Weekly Plan

Week 1: Distributed systems fundamentals — [Lecture 1](lectures/lecture-01-distributed-fundamentals.md)

Week 2: Event-driven systems — [Lecture 2](lectures/lecture-02-event-driven-systems.md)

Week 3: Data partitioning — [Lecture 3](lectures/lecture-03-partitioning-and-fault-tolerance.md)

Week 4: Fault tolerance — Lecture 3, and the [reliability lab](../course-01-engineering-foundations/labs/reliability-toolkit) if you skipped it

Week 5: Global infrastructure — Lecture 3, then [Course 07, Lecture 2](../course-07-advanced-system-design/lectures/lecture-02-global-multi-region.md) when you reach that course

## Labs

This course has two labs. That is the whole hands-on scope.

- [Lab 1: Chat System (gRPC)](labs/chat-system) — bidirectional streaming, rooms, history
- [Lab 2: Kafka Pipeline](labs/kafka-pipeline) — keyed produce, consume, running aggregation

## Case studies

Canonical copies live in [`../case-studies/`](../case-studies/). Course-local files are pointers.

- [Netflix streaming](../case-studies/netflix-streaming-architecture.md)
- [Uber dispatch](../case-studies/uber-dispatch-system.md)
- [Kafka](../case-studies/kafka-event-streaming.md)
- [Google Spanner](../case-studies/google-spanner-consistency.md)
- [Discord chat infrastructure](../case-studies/discord-chat-infrastructure.md)

## How to complete this course

1. Read Lecture 1 before the chat lab, Lecture 2 before the Kafka lab, Lecture 3 before you argue about sharding.
2. Run each lab's reference smoke check after you have tried the starter.
3. Read the case studies against the lecture, not instead of it.
