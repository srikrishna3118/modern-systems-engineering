# Case Study: Discord's Message Storage Architecture

## Overview

Discord delivers billions of messages daily to over 200 million monthly active users across millions of servers. Its message storage system must handle extreme write volumes, low-latency reads, and a massive variance in access patterns — from small private DMs to servers with millions of members.

## Key Challenges

- **Write Volume**: Billions of messages per day with spiky traffic patterns (game launches, events)
- **Read Patterns**: Hot channels (recent messages read frequently) vs. cold data (historical search)
- **Data Growth**: Trillions of messages stored, growing at petabytes per year
- **Latency**: Messages must appear in under 100ms for real-time chat experience
- **Availability**: Users expect 99.99%+ uptime for a communication platform

## Architecture Evolution

### Phase 1: MongoDB (2015)
Discord initially stored messages in MongoDB with a single replica set. This worked for early traffic but hit scaling limits:
- Document-level locking caused write contention
- Memory-mapped storage engine struggled with working set size
- Sharding was complex and operationally costly

### Phase 2: Cassandra (2016–2022)
Discord migrated to Apache Cassandra for its write-optimized, linearly-scalable design:

```
┌──────────────┐     ┌──────────────────────────┐
│  API Gateway │────▶│  Message Service (Elixir) │
└──────────────┘     └──────────┬───────────────┘
                                │
                    ┌───────────▼────────────┐
                    │  Cassandra Cluster      │
                    │  (channel_id, msg_id)   │
                    │  Partition Key: channel  │
                    │  Clustering: message_id  │
                    │  (Snowflake, time-sorted)│
                    └────────────────────────┘
```

**Data Model:**
- Partition key: `channel_id` + time bucket
- Clustering key: `message_id` (Snowflake ID — time-ordered)
- Time bucketing prevents unbounded partition growth

**Problems at Scale:**
- Cassandra's LSM-tree compaction caused latency spikes during garbage collection
- Hot partitions (popular channels) created uneven load distribution
- Read-before-write patterns for message editing were anti-patterns for Cassandra
- Cluster maintenance (repairs, compactions) became increasingly disruptive

### Phase 3: ScyllaDB (2022+)
Discord migrated to ScyllaDB, a C++ rewrite of Cassandra:

```
┌──────────────┐     ┌──────────────────────────┐
│  API Gateway │────▶│  Message Service (Rust)   │
└──────────────┘     └──────────┬───────────────┘
                                │
              ┌─────────────────▼──────────────────┐
              │       Data Services Layer           │
              │  (Rust, request coalescing,         │
              │   hot-partition routing)             │
              └─────────────────┬──────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │  ScyllaDB Cluster       │
                    │  (Same data model,      │
                    │   shard-per-core,        │
                    │   no GC pauses)          │
                    └────────────────────────┘
```

**Key Improvements:**
- **Shard-per-core architecture**: Each CPU core owns a subset of data, eliminating cross-core coordination
- **No garbage collection**: C++ eliminates JVM GC pauses that plagued Cassandra
- **Data Services Layer**: A Rust-based intermediary that coalesces concurrent reads for the same partition, reducing redundant database queries by 90%+
- **Request Coalescing**: When thousands of users load the same channel simultaneously, only one database query is executed; all concurrent requests wait on the same future

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Gateway | Elixir (WebSocket connections) |
| Message Service | Rust (rewritten from Python) |
| Database | ScyllaDB (migrated from Cassandra) |
| Caching | Memcached, in-process caches |
| Message IDs | Snowflake (custom Twitter-like ID generator) |
| Search | Elasticsearch |

## Data Model

```
messages (
    channel_id   bigint,
    bucket        int,         -- time bucket to bound partition size
    message_id   bigint,       -- Snowflake ID (timestamp + worker + sequence)
    author_id    bigint,
    content      text,
    attachments  list<frozen<attachment>>,
    PRIMARY KEY ((channel_id, bucket), message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

## Lessons Learned

1. **The right database changes as you scale** — MongoDB → Cassandra → ScyllaDB. Each transition was driven by concrete scaling bottlenecks, not technology trends.

2. **Request coalescing is a superpower for hot partitions** — A single data services layer that deduplicates concurrent requests to the same key can reduce database load by orders of magnitude.

3. **GC-free datastores matter at scale** — JVM garbage collection pauses were the #1 source of p99 latency spikes in Cassandra. ScyllaDB's C++ engine eliminated this entirely.

4. **Language migrations pay off for hot paths** — Rewriting the message service from Python to Rust reduced memory usage by 10x and improved throughput significantly.

5. **Time-bucketed partitions prevent unbounded growth** — Without time buckets, a channel with years of history would create a single massive partition. Bucketing ensures predictable partition sizes.

## Further Reading

- [How Discord Stores Trillions of Messages](https://discord.com/blog/how-discord-stores-trillions-of-messages)
- [How Discord Indexes Billions of Messages](https://discord.com/blog/how-discord-indexes-billions-of-messages)
- [Why Discord is Switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)
