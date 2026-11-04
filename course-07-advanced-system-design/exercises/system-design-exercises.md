# Course 07: System Design Exercises

Five interview-style designs with worked solutions. Each solution has requirements, capacity estimates, an API, a data model, a mermaid architecture, the hard part of the design, and an explicit trade-off table.

How to use them: [Lecture 6: System Design Interviews](../lectures/lecture-06-system-design-interviews.md). Close the solution, spend about 35 minutes, then compare decisions.

| # | Problem | What the numbers force | Worked solution |
|---|---------|------------------------|-----------------|
| 1 | URL shortener | ~240k peak redirects/sec, writes are easy | [01-url-shortener.md](01-url-shortener.md) |
| 2 | Real-time notifications | Priority isolation and at-least-once delivery | [02-notification-system.md](02-notification-system.md) |
| 3 | Rate limiter | One atomic decision under 10 ms across a fleet | [03-rate-limiter.md](03-rate-limiter.md) |
| 4 | Full-text search | A derived index, tenant fan-out, freshness lag | [04-full-text-search.md](04-full-text-search.md) |
| 5 | Video streaming | Tens of petabytes a day of egress, served from a CDN | [05-video-streaming.md](05-video-streaming.md) |

## What to hand in

If you are using these as assignments, each write-up should include:

1. Requirements you are actually designing for, including what you left out.
2. The estimates that changed the design, with the formula.
3. A diagram (mermaid is fine).
4. The data model and the partition key.
5. One deep dive, not a catalog of products.
6. Trade-offs: what you gain, what you give up, and what would change your mind.

## Exercise 1: URL shortener

Design a TinyURL-style service. 100 million new URLs per day. Redirects under 100 ms. Optional one-year expiry.

Cover unique code generation, the read path, and what happens when the cache is flushed. [Worked solution](01-url-shortener.md).

## Exercise 2: Real-time notifications

Deliver push, email, SMS, and in-app notifications to a large user base. Critical alerts under 1 second. Marketing must not block them. [Worked solution](02-notification-system.md).

## Exercise 3: Rate limiter

Decide allow or deny in under 10 ms, for different API tiers, across many stateless servers. [Worked solution](03-rate-limiter.md).

## Exercise 4: Full-text search

Index 100 million documents. Search under 500 ms at 10,000 queries/sec, with filters, ranking, and suggestions. [Worked solution](04-full-text-search.md).

## Exercise 5: Video streaming

Upload, transcode, and play video globally with adaptive bitrate. The egress estimate is the design. [Worked solution](05-video-streaming.md).

## Case studies to read after you have a design

- [Cloudflare DDoS defense](../../case-studies/cloudflare-ddos-defense.md) — shedding abusive traffic before the application.
- [GitHub code search](../../case-studies/github-code-search.md) — a real index built for code.
- [Shopify flash-sale scaling](../../case-studies/shopify-flash-sale-scaling.md) — known spikes, hot rows, fairness.
- [YouTube video delivery](../../case-studies/youtube-video-delivery.md) and [Netflix streaming](../../case-studies/netflix-streaming-architecture.md) — CDN, encode cost, playback.
- [Kafka](../../case-studies/kafka-event-streaming.md) and [Slack's queue](../../case-studies/slack-message-queue.md) — the log behind fan-out.

The course map of these studies is [case-studies/README.md](../case-studies/README.md).
