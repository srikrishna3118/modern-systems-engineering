# Case Study: Shopify Flash Sale Scaling – Handling 10x Traffic Spikes

## Overview

During flash sales and major shopping events (Cyber Monday, Black Friday, seasonal sales), Shopify's platform experiences 10–100x traffic spikes. The architecture must scale elastically to handle unprecedented load without degradation.

## Key Challenges

- **Predictable Spikes**: Traffic patterns are known hours/days in advance; pre-warming is possible
- **Database Bottleneck**: Inventory lookups and order creation must scale linearly with traffic
- **Checkout Conversion**: Slow checkout loses sales; p99 latency must remain < 200ms even during spikes
- **Fairness**: Prevent sophisticated bot attacks from consuming all inventory; ensure human shoppers can purchase

## Architecture Highlights

- **Pre-warming**: Days before a sale, spin up excess capacity (containers, database replicas, cache clusters)
- **Read Replicas**: Separate read replicas for product browsing; writes go to primary
- **Inventory Locking**: Optimistic locking (version fields) on inventory to detect conflicts without pessimistic locks
- **Queue-Based Checkout**: During spikes, enqueue checkout requests and process serially to prevent double-bookings
- **Bot Detection**: Rate limiting per IP, device fingerprinting, CAPTCHA challenges

## Technology Stack

- Kubernetes (auto-scaling), Postgres (inventory), Redis (session/cache)
- CDN (CloudFlare) for static content and DDoS protection
- Custom queue system for checkout serialization

## Lessons Learned

1. **Stateless services scale horizontally** — Shopify's microservices architecture enables horizontal scaling without shared state bottlenecks
2. **Inventory management is the hard part** — Optimistic locking prevents double-booking without expensive pessimistic locks; version fields are critical
3. **Separate concerns for traffic spikes** — Product browsing (read-heavy) is separate from checkout (transactional); different scaling strategies apply to each
4. **Pre-warming is essential** — Spinning up capacity during a spike is too slow; warm up in advance while traffic is still manageable
5. **Bot traffic is real and non-trivial** — During major sales, 50%+ of traffic is often bots; fingerprinting and rate limiting are necessary

## Where this fits in the curriculum

- [Course 07, Lecture 1: Designing for scale](../course-07-advanced-system-design/lectures/lecture-01-designing-for-scale.md) — split browse from checkout, pre-warm, then shard.
- [Course 07, Exercise 5](../course-07-advanced-system-design/exercises/05-video-streaming.md) — the same pre-warm move, applied to a hot video instead of a hot SKU.
- Course pointer: [course 07 wrapper](../course-07-advanced-system-design/case-studies/shopify-flash-sale-scaling.md).

## Further Reading

- [Shopify Engineering: Scaling Black Friday](https://shopify.engineering/)
- [The Evolution of Shopify's Architecture](https://shopify.engineering/)
