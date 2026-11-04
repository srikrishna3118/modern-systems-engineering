# Lecture 1: Events, Streams, and Windows

## Overview

Real-time systems are not "fast request/response." They are a log of things that happened, consumed by whoever cares, with a clear story for order, duplicates, and time. This lecture covers the event-driven shape, Kafka as the log, and windowed computation on that log.

## Topics

### 1. Event-driven architecture

A service that calls five other services in one user request owns all five failures. An event-driven service records what happened and returns. Other services react.

- **An event is a fact.** `OrderPlaced`, with an id, a time, and the payload needed to react. It is not a command disguised as a noun (`PleaseChargeCard`), and it is not a pointer that forces every consumer to call back for the data.
- **Producers do not know the consumers.** Adding a new consumer (analytics, fraud, notifications) does not change the producer. This is the actual benefit. "We used Kafka" is not.
- **Delivery is at least once** in every system you will operate. The consumer must be idempotent: processing the same event twice is a no-op. Exactly-once is a property you build inside one system (a transactional consume-and-write), not a promise from the network.
- **Order is per key, not global.** Kafka orders events inside a partition. The partition key is the scope of the order you need (a user, an account, a document). A global order is a single partition, which is a single machine's write rate.

The [notification exercise](../../course-07-advanced-system-design/exercises/02-notification-system.md) is this shape: accept and record, then let channel workers react, with a dedup key so a redelivery does not page the user twice.

### 2. Kafka as the log

Kafka is a partitioned, replicated, append-only log.

- **A topic** is the name of the stream. **Partitions** are the unit of parallelism and of order. **A consumer group** splits partitions across members. Two members, four partitions: each member owns some partitions, and a message is processed by one member of the group.
- **The offset** is the consumer's cursor. Committing an offset says "I have handled everything before here." Commit after the side effect, or you will lose the message. Commit before, and a crash retries it; that is the at-least-once case, and it is the one idempotency is for.
- **Retention** is by time or size. The log is not a queue that forgets on read. A new consumer can replay from the start if the retention window still holds the data. That replay is how you rebuild a derived view.
- **Replication** keeps the log available when a broker dies. A producer that waits for all in-sync replicas (`acks=all`) does not acknowledge a write that only one disk has seen.

The [Kafka lab](../../course-02-distributed-systems/labs/kafka-pipeline) builds the small version: a producer keyed by `user_id`, a consumer group, and a running fold. [Kafka's own design](../../case-studies/kafka-event-streaming.md) is the same idea without the training wheels.

### 3. Stream processing

A stream processor is a consumer that maintains state and emits new events.

- **Stateless map and filter** are easy and embarrassingly parallel.
- **A keyed aggregation** (revenue per category, in the lab) needs all events for a key on the same partition, which is why the producer chooses the key deliberately. Change the key and you change the answer.
- **Joins** between two streams require both to be partitioned the same way, and they require a bound on how late the other side may be. An unbounded join is a memory leak.

Frameworks (Kafka Streams, Flink) store the aggregation state in a local store and changelog it back to a topic, so a crashed processor restores state instead of starting from zero. You can also keep the fold in a database and treat the log as the source of retries. Either is fine. "State only in memory, and we will not crash" is not.

### 4. Time and windows

Event time and processing time are different clocks. Event time is when the thing happened. Processing time is when you saw it. Late events are normal (a mobile client reconnects, a producer retries).

Window types you should be able to pick from:

- **Tumbling:** fixed, non-overlapping (revenue per minute). Simple, and an event near the boundary falls in one bucket.
- **Sliding:** overlapping (the last 5 minutes, updated every minute). Smoother, more state.
- **Session:** a window per burst of activity, closed after a gap. Fits "a user's visit."

```
 event time ──▶  [ 10:00 , 10:01 ) [ 10:01 , 10:02 )   tumbling
                 [ 10:00 , 10:05 )
                   [ 10:01 , 10:06 )                   sliding
```

Close a window on a **watermark**: a claim that you are unlikely to see events older than T. Late events after the watermark are dropped, or they update a previously emitted result if the downstream can tolerate a correction. Say which one you do. Silence is how dashboards disagree with finance.

### 5. Time-series data

Window results and metrics are time series. Store them as such: a timestamp, a set of tags with bounded cardinality, and a value. Unbounded cardinality (a tag per user id) will take the metrics system down. Raw events stay in the log or the warehouse. The series stores the aggregates you alert on.

## Key Takeaways

1. **Events are facts with a key.** Order holds for that key, and consumers must tolerate duplicates.
2. **A consumer group splits partitions.** It does not split a partition, and it does not create a global order.
3. **Commit the offset after the side effect,** and make the side effect idempotent.
4. **Aggregations follow the partition key.** Repartition when the key is wrong; do not scan every partition per event.
5. **Windows close on event time, with a watermark.** Decide what a late event does.

## Further Reading

- [Kafka event streaming](../../case-studies/kafka-event-streaming.md)
- [Slack's message queue](../../case-studies/slack-message-queue.md)
- [Kafka lab](../../course-02-distributed-systems/labs/kafka-pipeline)
- [Lecture 2](lecture-02-websockets-latency-backpressure.md) — pushing the result to a waiting client.
