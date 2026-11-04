# Lecture 2: Event-Driven Systems

## Overview

[Lecture 1](lecture-01-distributed-fundamentals.md) covered what breaks when a call crosses a network. This lecture covers a way of structuring services so a user's request does not wait on every downstream effect: record the fact, return, and let other services react. The [Kafka lab](../labs/kafka-pipeline) is the mechanism. [Course 05](../../course-05-realtime-systems/lectures/lecture-01-events-streams-windows.md) goes further into windows and time.

## Topics

### 1. Commands, events, and the request

A **command** is a request to do something (`ChargeCard`). It can be refused. An **event** is a statement that something happened (`CardCharged`). Producers of events do not call consumers. They append to a log. Consumers subscribe.

Use a synchronous call when the user is waiting on the answer (did the charge succeed, does this user exist). Use an event when other work should happen because of the answer (send a receipt, update analytics, recompute a feature). Putting the receipt send on the request thread couples checkout latency to an email provider.

### 2. The log

An append-only log, partitioned by a key, gives you three things a pile of HTTP calls does not:

- **Replay.** A new consumer reads history and builds its own view. A bug in a consumer is fixed by reading the log again, if retention still holds it.
- **A buffer.** Producers and consumers scale separately. A slow consumer falls behind instead of slowing the write, until the lag is large enough that you must shed or scale. Lag is the metric.
- **Per-key order.** Events for one user, on one partition, stay in order. That is the order you can program against.

The [Kafka case study](../../case-studies/kafka-event-streaming.md) describes replication and the consumer group. In the lab, the partition key is `user_id` by default. Switching it to `product_id` is the experiment: ordering and aggregation follow the key, not the topic name.

### 3. Idempotent consumers

The log delivers at least once. A consumer that increments a counter on every delivery will increment twice whenever a worker crashes after the side effect and before the offset commit. Prefer:

- Store the event id you have applied, and skip ids you know.
- Or make the write naturally idempotent (set balance to the value computed from the event's own version, insert a row with a unique event id).

Commit the offset after the side effect is durable. The [payment lecture](../../course-06-financial-systems/lectures/lecture-01-payments-idempotency-availability.md) is the strict version of the same rule.

### 4. What not to put on the bus

Do not use the log as the only copy of a fact you cannot lose and cannot replay from somewhere else, unless the producer's `acks=all` and the retention and replication match that promise. Do not publish an event that is missing the data consumers need and then require every consumer to call you back; you have reintroduced the synchronous coupling and added a race. Do not share one topic across unrelated facts "to keep things simple." A topic is a contract. Version the payload, and add fields instead of changing the meaning of old ones.

## Key Takeaways

1. **Synchronous calls for the answer the user is waiting on. Events for the consequences.**
2. **A partitioned log gives replay, buffering, and per-key order.**
3. **Consumers will see duplicates.** Make the side effect idempotent, then commit the offset.
4. **The partition key is the design.** Aggregation and order follow it.
5. **A topic is a contract.** Version the payload, and do not make consumers call home for the rest of the fact.

## Further Reading

- [Kafka lab](../labs/kafka-pipeline)
- [Kafka event streaming](../../case-studies/kafka-event-streaming.md)
- [Slack's message queue](../../case-studies/slack-message-queue.md)
- [Course 05, Lecture 1](../../course-05-realtime-systems/lectures/lecture-01-events-streams-windows.md)
