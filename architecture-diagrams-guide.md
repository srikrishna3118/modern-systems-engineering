# System Architecture Diagrams Guide

This guide covers common architectural patterns and how to design diagrams for system design problems.

## 1. Basic Architecture Pattern

**Typical Flow:**
```
┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│   Clients    │─────▶│  Load Balancer  │─────▶│   Services   │
│  (Web, App)  │      │  (API Gateway)  │      │  (Backend)   │
└──────────────┘      └─────────────────┘      └──────┬───────┘
                                                      │
                           ┌──────────────────────────┘
                           │
                  ┌────────▼─────────┐
                  │  Data Storage    │
                  │  (DB/Cache/etc)  │
                  └──────────────────┘
```

**Components:**
- **Clients**: Web browsers, mobile apps, third-party APIs
- **Load Balancer**: Distributes traffic across multiple servers
- **Services**: Stateless backend servers (scalable)
- **Database**: Stateful storage (single instance or replicated)

---

## 2. Scaling Patterns

### Horizontal Scaling (Multiple Servers)
```
┌────────────────┐
│ Load Balancer  │
├────┬───────┬──┤
│    │       │  │
▼    ▼       ▼  ▼
┌──┐┌──┐┌──┐┌──┐
│S1││S2││S3││SN│  (Stateless Servers)
└──┘└──┘└──┘└──┘
  │   │   │   │
  └───┴───┴───┘
      │
      ▼
  ┌────────┐
  │Database│
  └────────┘
```

### Vertical Scaling (Bigger Server)
```
┌────────────────────┐
│  Server (larger)   │
│  - More CPU        │
│  - More RAM        │
│  - Bigger storage  │
└────────────────────┘
```

---

## 3. Database Replication

### Master-Replica (Read Scaling)
```
        ┌──────────┐
        │ Primary  │ (Accepts writes)
        └──────┬───┘
               │ Replication log
    ┌──────────┴──────────┐
    ▼                     ▼
┌────────┐           ┌────────┐
│Replica1│ (read)    │Replica2│ (read)
└────────┘           └────────┘
```

### Multi-Master (Write Scaling)
```
    ┌──────────┐         ┌──────────┐
    │ Master 1 │◀───────▶│ Master 2 │
    └──────────┘         └──────────┘
                              │
                              │ Bidirectional
                              │ replication
```

### Quorum-Based (Consistency)
```
   Write requires 2/3 replicas
   Read requires 2/3 replicas

┌────────┐  ┌────────┐  ┌────────┐
│Replica1│  │Replica2│  │Replica3│
└────────┘  └────────┘  └────────┘
     ▲            ▲           ▲
     └────┬───────┼───────────┘
          │ Quorum acknowledgment
          ▼
       (Client)
```

---

## 4. Caching Patterns

### Cache-Aside (Look-Aside)
```
┌────────┐
│Request │
└───┬────┘
    │
    ▼ Check cache
┌─────────┐
│  Cache  │ ─── Hit─┐
└────┬────┘         │
     │ Miss         │
     ▼              │
┌────────────┐      │
│ Database   │      │
└────┬───────┘      │
     │              │
     └──┬───────────┘
        ▼ Return
    Response
```

### Write-Through
```
   Write
     │
     ├────▶ Update Cache
     └────▶ Write to DB (waits)
```

### Write-Behind (Async)
```
   Write
     │
     ├────▶ Update Cache (return immediately)
     │
     └────▶ Write to DB (background async)
                (risks data loss if cache fails)
```

---

## 5. Data Partitioning (Sharding)

### Range-Based
```
Shard 1: Users A-M
Shard 2: Users N-Z

hash_func(user_id) → "range" → lookup shard
```

### Hash-Based
```
Shard = hash(user_id) % num_shards

┌────────────────────────────────┐
│ hash("alice") % 3 = 0 → Shard 1│
│ hash("bob") % 3 = 2   → Shard 3│
│ hash("carol") % 3 = 1 → Shard 2│
└────────────────────────────────┘
```

### Consistent Hashing (Avoids resharding on growth)
```
Nodes on a ring; data hashes to nearest node.
New node added: only some keys rehash.
```

---

## 6. Microservices Architecture

```
┌─────────────────────────────────────────────────┐
│                 API Gateway                     │
│           (Rate limit, Auth, Route)            │
└────┬──────────┬──────────┬─────────────────────┘
     │          │          │
     ▼          ▼          ▼
  ┌────┐    ┌──────┐    ┌────────┐
  │User│    │Order │    │Payment │
  │Svc │    │Svc   │    │Svc     │
  └───┬┘    └──┬───┘    └───┬────┘
      │        │            │
      ├────────┼────────────┤
      │        │            │
      ▼        ▼            ▼
   ┌──────────────────────────┐
   │   Message Bus (Kafka)    │
   │   (async communication)  │
   └────────────────────────┬─┘
                             │
            ┌────────────────┼────────────┐
            ▼                ▼            ▼
      ┌────────────┐  ┌──────────┐  ┌─────────┐
      │Analytics   │  │Logging   │  │Metrics  │
      └────────────┘  └──────────┘  └─────────┘
```

---

## 7. Event-Driven Architecture

```
┌─────────────┐
│   Producer  │ (e.g., user signup)
└──────┬──────┘
       │ Event: { user_id, email, timestamp }
       ▼
┌──────────────────────┐
│   Event Broker       │
│   (Kafka/RabbitMQ)   │
└──────┬───────┬───────┐
       │       │       │
       ▼       ▼       ▼
   Consumer1  Consumer2  Consumer3
   (email)    (analytics)(notification)
```

---

## 8. Global Distribution

### Multi-Region with Replication
```
┌─────────────────────────────────┐
│         US-EAST Region          │
│  ┌─────────────────────────┐    │
│  │ Users → API → Database  │    │
│  └────────────┬────────────┘    │
└────────────────┼─────────────────┘
                 │ Replication
┌────────────────┼─────────────────┐
│    EU-WEST Region              │
│  ┌─────────────────────────┐    │
│  │ Users → API → Database  │    │
│  └─────────────────────────┘    │
└─────────────────────────────────┘
```

### CDN for Static Content
```
┌──────────────────────────────────┐
│      Content Delivery Network     │
│  (Cloudflare, CloudFront, etc)   │
│  - PoP in US                     │
│  - PoP in EU                     │
│  - PoP in APAC                   │
└──────────────────────────────────┘
         ▲
         │
    User requests
```

---

## 9. Search Architecture

```
┌────────────┐
│  Indexer   │ (Batch job)
│  (Spark)   │
└─────┬──────┘
      │ Index
      ▼
┌──────────────────────┐
│   Search Index       │
│   (Elasticsearch)    │
│   - Shard 1          │
│   - Shard 2          │
│   - Replica          │
└─────┬────────────────┘
      │
      ▼
   Query Parser
      │
      ▼
   Ranker (ML)
      │
      ▼
   Results
```

---

## 10. Real-Time Streaming

```
┌─────────────┐
│   Producer  │ (data source)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Stream Broker  │
│  (Kafka, Redis) │
│  - 1000s events │
└─┬───┬───┬───┬───┘
  │   │   │   │
  ▼   ▼   ▼   ▼
┌─ Stream Processing Engines ─┐
│ (Spark Streaming, Faust, etc)│
│ - Aggregate                   │
│ - Filter                      │
│ - Join                        │
└──────────┬────────────────────┘
           │
        ┌──┴──┐
        ▼     ▼
    Analytics Dashboard
    Real-time Alerts
```

---

## 11. Security & Authentication

```
┌─────────┐
│  Client │
└────┬────┘
     │ Username/Password
     ▼
┌────────────┐
│  Auth Svc  │
│  (validate)│
└─────┬──────┘
      │ JWT Token
      ▼
┌──────────────┐
│   Client     │ (stores token)
│   (includes  │
│    token in  │
│   requests)  │
└──────┬───────┘
       │ token: Authorization header
       ▼
┌──────────────┐
│  API Gateway │
│  (verify)    │
└──────┬───────┘
       │ ✓ Valid
       ▼
   Protected Resource
```

---

## 12. Monitoring & Observability Stack

```
┌──────────────────────────────────┐
│        Application               │
│  (emit metrics, logs, traces)    │
└────┬─────────┬────────────┬──────┘
     │         │            │
     ▼         ▼            ▼
┌────────┐┌──────┐┌────────┐
│Metrics ││ Logs ││ Traces │
│(prometh)│(ELK) │(Jaeger) │
└──┬─────┘└──┬───┘└───┬────┘
   │         │        │
   ▼         ▼        ▼
┌──────────────────────────┐
│   Visualization          │
│   (Grafana, Kibana)      │
│                          │
│ - Dashboards            │
│ - Alerts                │
│ - Error tracking        │
└──────────────────────────┘
```

---

## Tips for Drawing Architecture Diagrams

1. **Use consistent symbols**: Boxes for services, cylinders for databases, clouds for external
2. **Show data flow**: Arrows with labels (read, write, replicate, aggregate)
3. **Indicate scale**: Notation like "N servers", "10M items/day"
4. **Layer by concern**: Present tier (API), business logic (services), data (DB)
5. **Highlight bottlenecks**: Underline or star the critical path
6. **Include fallbacks**: Show redundancy, failover, and retry paths
7. **Keep it simple**: Don't over-complicate; omit internal details if not relevant
8. **Use text annotations**: Label with technology (PostgreSQL, Kafka, Redis, etc.)

---

## Further Reading

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications (Kleppmann)](https://dataintensive.net/)
- [Lucidchart Architecture Diagramming](https://www.lucidchart.com/)
