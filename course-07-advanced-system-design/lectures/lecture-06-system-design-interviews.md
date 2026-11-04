# Lecture 6: System Design Interviews and Design Communication

## Overview

A system design interview is a conversation about trade-offs under a clock. The interviewer is grading whether you can find the constraints, commit to a design, and explain what you gave up. This lecture is the communication method for the five exercises in this course. The same method is how you should write a design doc for a real system.

## Topics

### 1. Spend the first minutes on the contract

Do not draw yet. Agree the problem in this order:

1. **Users and the one job** the system does. "Shorten a URL and redirect" is a job. "A platform for links" is not.
2. **Functional scope.** What is in, and what you are explicitly leaving out (analytics, custom aliases, auth).
3. **Non-functional targets.** Latency, availability, consistency, and durability, as numbers.
4. **Scale.** Ask for DAU, read/write ratio, and retention, or state an assumption and write it down.

Assumptions are fine. Hidden assumptions are not. Say "I am assuming 100 million new URLs a day and a 100:1 read ratio. Stop me if that is off."

### 2. Estimate on purpose

One or two estimates that change the design are worth more than a page of arithmetic.

- Convert per-day totals to per-second, and apply a peak factor.
- Estimate storage as `records × bytes × replicas × years`.
- Estimate bandwidth as `QPS × bytes`.
- Say which number forced a decision: "116k reads/sec means the database is not on the redirect path."

Round to one significant figure and keep the formula visible. The interviewer is checking the formula, not the last digit. The exercises in this course show the formulas next to the architecture so you can practice saying them out loud.

### 3. A design narrative that fits on one board

Use the same shape every time:

1. **Happy-path API.** Two or three endpoints. Name the idempotency story on anything that writes.
2. **One diagram.** Client, edge, service, cache, source of truth. Arrow labels are data, not just "requests."
3. **Data model.** The primary key, the partition key if it differs, and one index. Explain the query that key serves.
4. **The hard part.** Pick the piece that can fail the requirements (unique ID generation, hot keys, fan-out, cross-region writes) and go deep.
5. **Trade-offs.** Name the alternative you rejected and the condition that would make you pick it.

```
1. Contract     what, for whom, how fast, how big
2. API          the writes and the reads
3. Diagram      where state lives
4. Deep dive    the one hard problem
5. Trade-off    what you gave up, and why
```

If you are still drawing new boxes at the end, you never reached the hard part.

### 4. How to talk about trade-offs

A trade-off is a sentence with both sides and a reason:

- "Redirects are eventually consistent with the write for up to the cache TTL, which I set to one minute, because a stale redirect is rare and a 116k QPS read of the primary is not."
- "I accept losing the in-flight second of analytics on a region failure because those events are derived, not the mapping."

Avoid "it depends" with no condition, and avoid a distributed-systems slogan ("we'll use Kafka for scalability") that is not tied to a number.

Useful pairs in this course:

| Choice | You gain | You give up |
|--------|----------|-------------|
| Cache on the read path | Latency, read capacity | Freshness, invalidation complexity |
| Hash partitioning | Even write spread | Easy range scans, cheap reshard |
| Single-region primary | Strong consistency, simple failover story | Write latency for distant users |
| Async derived index | Source of truth stays simple | Search or feed can lag the write |
| Fail-closed rate limit | Safety under limiter failure | Availability coupled to Redis |

### 5. Failure, because they will ask

For the design you drew, be ready with:

- What happens when the cache is empty (thundering herd) or down.
- What happens when one shard is down. Is the error partial or total.
- How a retry avoids a double write.
- How you know it is unhealthy (one signal: error rate, lag, or saturation) and what you do.

You do not need a novel monitoring stack. You need one loop: measure the requirement you claimed (redirect p99, delivery delay, limit accuracy), alert when it slips, and know which component you will shed first.

### 6. Practice with the exercises

Each exercise in [exercises/](../exercises/system-design-exercises.md) is written as a worked interview: requirements, estimates, diagram, data model, deep dive, and a trade-off section. Use them in two passes.

1. Close the solution. Spend 35 minutes producing your own one-page design.
2. Open the solution and diff the decisions, not the wording. Where you skipped an estimate or a failure mode, that is the gap.

Related production stories, linked from each exercise, are there to check whether your trade-off shows up in a real system. Read the case study after you have a design, so you are comparing judgments rather than memorizing a diagram.

## Key Takeaways

1. **Agree the contract and the numbers** before the diagram.
2. **One diagram, one data model, one deep dive** beats a tour of every technology you know.
3. **State trade-offs as a gain, a loss, and a reason.**
4. **Say what a retry, a dead cache, and a dead shard do.**
5. **Practice under a timer** on the five exercises, then compare decisions.

## Further Reading

- [System design exercises](../exercises/system-design-exercises.md) — five worked problems in the format above.
- [Architecture Diagrams Guide](../../architecture-diagrams-guide.md) — patterns worth being able to draw quickly.
- Xu, A. *System Design Interview* — a published worked-example style. Use it for practice volume; use the exercises here for the estimates and trade-offs tied to this curriculum.
