# Lecture 4: Rate Limiting, Throttling, and Quotas

## Overview

Rate limiting protects a shared system from one client, one bug, or one attack. Throttling slows a client down. Quotas cap how much of a resource an account may consume over a longer window. They look similar in an interview and they fail differently in production. This lecture separates them and shows how to enforce a limit in under a few milliseconds across many servers.

## Topics

### 1. Three different promises

- **Rate limit:** N operations per short window, per key (user, token, IP). A client who exceeds it gets `429 Too Many Requests` and a `Retry-After`. The goal is fairness and overload protection.
- **Throttle:** the server still accepts the work but slows the client (delayed responses, smaller page sizes, degraded features). Use this when dropping the request is worse than serving it late.
- **Quota:** a budget over hours or a billing period (10,000 SMS per day, 100 GB egress). Exceeding it is a product and billing event, not just an overload signal. Quotas must survive restarts and be auditable.

Do not implement a monthly quota as a 30-day sliding window in the request path. Check a counter that a billing job maintains, and keep the hot-path limiter on a short window.

### 2. Algorithms

**Token bucket.** A bucket holds up to `C` tokens and refills at `R` per second. Each request takes one token. It allows a burst of `C` and then a steady rate `R`. This is the default choice for APIs.

**Leaky bucket.** Requests enter a queue that drains at a fixed rate. Bursts are smoothed rather than allowed. Good when the downstream system cannot tolerate a burst (a payment processor with a hard connection cap).

**Fixed window.** Count requests in the current minute. Simple, and wrong at the boundary: a client can send `N` at 0:59 and `N` at 1:00, which is `2N` in two seconds.

**Sliding window log.** Store every timestamp and count those inside the window. Accurate, and expensive in memory.

**Sliding window counter.** Keep the previous window's count and the current count. Estimate the overlap by weighting the previous window by how much of it still falls inside the rolling window. Accurate enough, cheap enough.

```
tokens
  C ┤████████████████░░░░   refill at R per second
    ┤
  0 ┼────────────────────── time
         burst allowed, then steady
```

### 3. Where the decision runs

The limiter has to sit on the path that is being protected, and it has to be fast.

- **Edge / API gateway** for authentication abuse, scrapers, and per-IP floods. The request should die before it reaches the application. [Cloudflare's layered filters](../../case-studies/cloudflare-ddos-defense.md) are this idea taken to network scale: drop the obvious attacks before they cost application CPU.
- **Per service** for an expensive endpoint (search, checkout, password reset) whose limit is tighter than the global API limit.
- **Per dependency** so one caller cannot exhaust a shared database or a third-party SMS provider.

A local in-process counter is fast and wrong in a fleet: ten instances each allow `N`, so the client gets `10N`. A shared store (Redis, or a dedicated limiter service) is the usual fix. The cost is a network hop, which is why the check must be a single atomic operation, not a read-modify-write from the application.

Atomic token bucket in Redis is one `EVAL` script or one increment-with-TTL. Approximate limits are acceptable; a limiter that adds 20 ms to every call is not, if the budget is 10 ms.

### 4. Failure mode of the limiter itself

Decide this before the outage:

- **Fail open** when the limiter store is down and the endpoint is cheap and low-risk. Availability wins. You may be overloaded.
- **Fail closed** when the endpoint is expensive or dangerous (password reset, card charge, unauthenticated write). A limiter outage becomes a dependency outage, so the limiter needs its own redundancy.

Cache a recent allow decision for a few hundred milliseconds so a Redis blip does not stall the fleet. Never cache a deny for long; clocks and refills move.

### 5. Keys, tiers, and fairness

- Key the limit on the identity that should be fair: user id for logged-in calls, API token for partners, IP only as a fallback. IP keys punish NAT and mobile carriers.
- Tiers are different buckets, not branches sprinkled through business logic: `free: 60/min`, `paid: 600/min`. Store the tier on the token so the limiter does not query the user database.
- Separate **global safety limits** (protect the cluster) from **product limits** (what the plan paid for). The global limit should be invisible to a well-behaved paid customer.

### 6. What clients need

A `429` without a retry hint creates a retry storm. Return:

- `429` and `Retry-After`
- remaining budget (`RateLimit-Remaining`) when you can do it cheaply
- a stable error body so SDKs can back off with jitter

Clients must treat the retry as idempotent. A limiter that causes a duplicate charge has failed, even if the count was accurate. Pair limits with [idempotency keys](../../case-studies/stripe-payment-system.md) on any unsafe method.

The worked design, including a Redis script sketch and the distributed-failure follow-ups, is [Exercise 3](../exercises/03-rate-limiter.md).

## Key Takeaways

1. **Rate limits, throttles, and quotas** answer different questions. Do not mix their windows.
2. **Token bucket** is the default algorithm because it allows a bounded burst.
3. **Enforce the limit in one atomic shared operation**, close to the edge.
4. **Choose fail-open or fail-closed explicitly** for when the limiter store is down.
5. **Tell the client when to retry**, and make that retry safe.

## Further Reading

- [Exercise 3: Rate Limiter](../exercises/03-rate-limiter.md)
- [Cloudflare DDoS Defense](../../case-studies/cloudflare-ddos-defense.md) — dropping abusive traffic before it reaches the origin.
- [Shopify Flash Sale Scaling](../../case-studies/shopify-flash-sale-scaling.md) — bots, fairness, and checkout under a spike.
