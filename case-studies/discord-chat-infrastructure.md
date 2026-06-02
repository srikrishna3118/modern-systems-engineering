# Case Study: Discord Message Storage – From MongoDB to ScyllaDB

## Overview

Discord delivers billions of messages daily to 200M+ monthly active users. Its message storage system must handle extreme write volumes, low-latency reads, and a massive variance in access patterns — from small private DMs to public servers with millions of members.

## Key Challenges

- **Write Volume**: Billions of messages per day with spiky traffic patterns
- **Read Patterns**: Hot channels (recent messages read frequently) vs. cold data (historical search)
- **Data Growth**: Trillions of messages stored, growing at petabytes per year
- **Latency**: Messages must appear in under 100ms for real-time chat experience
- **Availability**: 99.99%+ uptime for a communication platform

## Architecture Evolution

### Phase 1: MongoDB (2015)
Early MongoDB implementation hit scaling limits:
- Document-level locking caused write contention
- Memory-mapped storage struggled with large working sets

### Phase 2: Cassandra (2016–2022)
Migrated to Cassandra for write scalability:
- Linear scalability with cluster size
- Write-optimized LSM-tree storage
- Problems: Compaction latency spikes, uneven load distribution

### Phase 3: ScyllaDB (2022+)
Migrated to ScyllaDB (C++ rewrite of Cassandra):
- **Shard-per-core architecture**: Each CPU core owns data partition; eliminates cross-core contention
- **No garbage collection**: C++ avoids JVM GC pauses
- **Request coalescing**: Multiple concurrent reads for the same key deduplicate; reduces database load by 90%+
- **Data Services Layer**: Rust-based intermediary coalescing requests

## Technology Stack

- Elixir (WebSocket gateway), Rust (message service)
- ScyllaDB (NoSQL, C++), Elasticsearch (search)
- Memcached (in-process and networked caching)

## Lessons Learned

1. **The right database changes as you scale** — MongoDB → Cassandra → ScyllaDB; each transition driven by concrete bottlenecks
2. **Request coalescing is powerful** — Deduplicating concurrent reads reduces database load dramatically
3. **GC-free languages matter at scale** — JVM GC pauses were Discord's primary p99 latency issue
4. **Language migrations pay off** — Python → Rust in message service reduced memory usage by 10x
5. **Time-bucketed partitions prevent unbounded growth** — Partitions stay constant size; unbounded growth causes hotspots

## Further Reading

- [How Discord Stores Trillions of Messages](https://discord.com/blog/how-discord-stores-trillions-of-messages)
- [Why Discord is Switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)
