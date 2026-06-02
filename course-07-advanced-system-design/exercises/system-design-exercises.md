# Course 07: Advanced System Design Exercises

## Exercise 1: Design a URL Shortener (Tiny URL)

### Problem Statement
Design a URL shortening service like Tiny URL that:
- Takes long URLs and generates short, unique identifiers
- Redirects users to the original URL when accessing the short link
- Supports 100M new unique URLs per day
- Answers redirect requests in < 100ms

### Requirements
1. **Functional Requirements:**
   - Generate short URL for a long URL
   - Redirect short URL to long URL
   - Expiration (optional; short URLs might expire after 1 year)

2. **Non-Functional Requirements:**
   - Low latency (< 100ms for redirects)
   - High availability
   - Scalability (handle 1000s of requests/sec)

### Design Considerations

**URL Generation:**
- Use base62 encoding (A-Z, a-z, 0-9) to generate short URLs
- 6-character short URL = 62^6 ≈ 56 trillion combinations
- Use Zookeeper or similar to generate unique IDs across distributed system

**Storage:**
- Write-heavy for new URLs (100M/day = ~1200/sec)
- Read-heavy for redirects (~100:1 read/write ratio)
- Use NoSQL (DynamoDB, Cassandra) for write scalability

**Architecture:**
```
┌─────────────────────────────────────┐
│      API Gateway (Load Balancer)    │
├─────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────────┐ │
│  │Create Svc│  │ Redirect Service  │ │
│  │(write)   │  │ (read)            │ │
│  └────┬─────┘  └──────┬───────────┘ │
│       │                │             │
│  ┌────▼────────────────▼──────────┐  │
│  │     Cache (Redis)              │  │
│  │  (hot URLs cached)             │  │
│  └────────────────┬───────────────┘  │
│                   │                  │
│  ┌────────────────▼──────────────┐  │
│  │      Database (NoSQL)         │  │
│  │  short-id → long-url mapping  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Follow-Up Questions
1. How would you handle collisions in short URL generation?
2. How would you handle expired URLs?
3. How would you track analytics (clicks, sources)?
4. How would you prevent abuse (infinite redirects)?

---

## Exercise 2: Design a Real-Time Notification System

### Problem Statement
Design a notification system that:
- Delivers notifications to users in real-time
- Supports multiple notification channels (push, email, SMS, in-app)
- Reaches 100M+ users reliably
- Prioritizes critical notifications (security alerts) over non-critical (marketing)

### Requirements
1. **Functional Requirements:**
   - Send notification to user
   - User can mark as read/unread
   - Retry failed deliveries
   - Support multiple channels

2. **Non-Functional Requirements:**
   - Latency: < 1 second for critical, < 10 seconds for normal
   - Reliability: 99.9% delivery rate
   - Scalability: 1M+ notifications/sec

### Design Considerations

**Notification Queue:**
- Use Kafka with multiple topics (critical, normal, low-priority)
- Different consumer groups for different channels
- Parallel processing of notifications

**Delivery Channels:**
- **Push**: Asynchronous, via APNs/GCM
- **Email**: Batch or on-demand, via SES/SendGrid
- **SMS**: Via Twilio, careful rate limiting (expensive)
- **In-App**: Database + WebSocket for real-time delivery

**Reliability:**
- Store pending notifications in database
- Mark as delivered only after confirmation from provider
- Exponential backoff for retries
- Dead-letter queue for repeated failures

### Architecture

```
┌──────────────────────────────────────┐
│    Notification API                  │
│  (receive notification requests)      │
└────────────┬─────────────────────────┘
             │
      ┌──────▼──────┐
      │    Kafka    │ (topic: notifications)
      │  (queuing)  │
      └──────┬──────┘
             │
   ┌─────────┼─────────┬──────────┐
   │         │         │          │
┌──▼─┐  ┌──▼─┐  ┌──▼──┐  ┌──▼───┐
│Push│  │Email│  │SMS  │  │In-App│
│Svc │  │Svc  │  │Svc  │  │Svc   │
└──┬─┘  └──┬─┘  └──┬──┘  └──┬───┘
   │       │       │        │
   └───────┴───────┴────────┘ (write to DB)
        Notification State DB
```

### Follow-Up Questions
1. How would you handle notification deduplication (user receives same notification twice)?
2. How would you implement notification preferences (user opts out of certain types)?
3. How would you prioritize critical notifications to skip the queue?
4. How would you measure delivery success rate?

---

## Exercise 3: Design a Rate Limiter

### Problem Statement
Design a rate limiting service that:
- Prevents single user from making too many API requests
- Supports different rate limits for different tiers (free, premium, enterprise)
- Handles distributed rate limiting across multiple servers
- Makes decision in < 10ms

### Requirements
1. **Functional Requirements:**
   - Allow N requests per time window (e.g., 100 req/min)
   - Return 429 (Too Many Requests) when exceeded
   - Support multiple tier definitions

2. **Non-Functional Requirements:**
   - Latency: < 10ms per decision
   - Scalability: 1M+ unique users
   - Accuracy: Must not allow more than limit across distributed system

### Algorithms

**Token Bucket:**
- Bucket has capacity C tokens
- Tokens refill at rate R per second
- Each request consumes 1 token
- If bucket empty, request rejected
- Allows burst (up to C tokens at once)

**Sliding Window Log:**
- Store timestamp of each request in a log
- Count requests in last time window
- If count > limit, reject
- Problem: Memory intensive, high latency

**Sliding Window Counter:**
- Divide time into windows
- Track request count per window
- For current request, interpolate across window boundary
- More memory-efficient than log

### Architecture

```
┌──────────────────────────────────┐
│      API Gateway                 │
│  (incoming request: user_id)      │
└────────────┬─────────────────────┘
             │
      ┌──────▼───────┐
      │ Rate Limiter │
      │  (check key) │
      └──────┬───────┘
             │
      ┌──────▼────────────┐
      │  Redis (Atomic)   │
      │  user_id:tokens   │
      │  (distributed)    │
      └──────┬────────────┘
             │
        ┌────▼───────┐
        │ Allow/Deny │
        └────────────┘
```

### Follow-Up Questions
1. How would you handle clock skew across servers?
2. How would you implement different limits for different endpoints?
3. How would you allow short-term burst but limit sustained traffic?
4. How would you handle failed rate limit checks (Redis down)?

---

## Exercise 4: Design a Search System

### Problem Statement
Design a search system that:
- Indexes 100M+ documents
- Returns relevant results in < 500ms
- Supports full-text search with typo correction
- Handles 10K+ queries/sec

### Requirements
1. **Functional Requirements:**
   - Full-text search across documents
   - Suggestion/autocomplete on queries
   - Ranking by relevance
   - Filters (date range, category, etc.)

2. **Non-Functional Requirements:**
   - Latency: < 500ms for search, < 100ms for suggestions
   - Scalability: 100M+ documents, 10K+ QPS

### Technologies

**Elasticsearch:**
- Distributed full-text search engine
- Built on Lucene
- Supports aggregations, filters, full-text queries
- Shards data for scalability

**Inverted Index:**
- Maps term → documents containing term
- Enables fast full-text search
- Example:
  ```
  "python" → [doc1, doc5, doc12]
  "django" → [doc1, doc7]
  ```

**BM25 Ranking Algorithm:**
- Probability ranking: how likely is document relevant to query?
- Considers: term frequency (TF), inverse document frequency (IDF), document length normalization

### Architecture

```
┌─────────────────────────────────┐
│      Search API                 │
│  (receive query)                 │
└────────────┬────────────────────┘
             │
      ┌──────▼──────────────┐
      │  Elasticsearch      │
      │  (distributed)      │
      │  - Shard 1          │
      │  - Shard 2          │
      │  - Replica          │
      └──────┬──────────────┘
             │
        ┌────▼─────────┐
        │ Results      │
        │ (ranked)     │
        └──────────────┘
```

### Follow-Up Questions
1. How would you update the index as new documents arrive?
2. How would you handle typos (Levenshtein distance)?
3. How would you implement pagination for large result sets?
4. How would you weight relevance factors (title vs. body)?

---

## Exercise 5: Design a Video Streaming Service

See the YouTube case study in `case-studies/` for a detailed example.

**Key Design Questions:**
1. How would you encode videos efficiently for different devices?
2. How would you minimize buffering?
3. How would you distribute video globally with low latency?
4. How would you handle DRM (Digital Rights Management)?

---

## Submission Guidelines

For each exercise, provide:
1. **System Architecture Diagram** (ASCII or Mermaid)
2. **Data Model** (schema, indices)
3. **API Design** (requests/responses)
4. **Scaling Analysis** (bottlenecks, solutions)
5. **Trade-offs** (consistency vs. availability, latency vs. throughput)
6. **Technology Justification** (why this tech, alternatives)

Use the 20+ case studies in `case-studies/` for references and inspiration!
