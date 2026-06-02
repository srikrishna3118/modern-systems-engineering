# Lecture 2: Building Scalable Systems

## Overview

As systems grow, initial designs break. This lecture covers the architectural patterns and trade-offs needed to scale.

## Topics

### 1. Vertical vs. Horizontal Scaling

**Vertical Scaling (Scale Up):**
- Add more CPU, RAM, disk to a single machine
- Pros: Simple, no coordination needed
- Cons: Hardware limits, single point of failure
- When to use: Early stage, specific bottleneck (e.g., in-process cache)

**Horizontal Scaling (Scale Out):**
- Add more machines to a cluster
- Pros: No limit to scale, high availability
- Cons: Distributed system complexity, consistency challenges
- When to use: Beyond vertical limits, seeking high availability

### 2. Caching Strategies

**Architecture:**
```
┌─────────┐      ┌────────┐      ┌──────────┐
│ Client  │─────▶│ Cache  │─────▶│ Database │
└─────────┘      └────────┘      └──────────┘
   read              hit?           source of truth
```

**Cache Types:**
- **Look-Aside (Lazy)**: Check cache first; if miss, fetch from source
- **Write-Through**: Update cache and database together
- **Write-Behind**: Update cache first; write to database asynchronously (risks data loss)

**Cache Invalidation**: "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

Strategies:
- **TTL (Time To Live)**: Expire entries after X seconds
- **LRU (Least Recently Used)**: Evict oldest entries when full
- **Explicit Invalidation**: Clear on data changes
- **Event-Driven**: Subscribe to data change events

### 3. Partitioning (Sharding)

**Why Partition?**
- Single database can't scale memory and throughput indefinitely
- Partition data to distribute load

**Strategies:**
- **Range Partitioning**: By value range (e.g., users A-M on shard 1, N-Z on shard 2). Problem: uneven distribution
- **Hash Partitioning**: hash(key) % num_shards. Problem: resharding on growth
- **Directory-Based**: Lookup table maps keys to shards (flexible, adds lookup overhead)

**Hot Partitions**: Some shards receive more traffic. Mitigations:
- Monitor and rebalance
- Use copartitioning (related data on same shard)

### 4. Replication for Availability

**Master-Worker Replication:**
```
┌──────────────┐        ┌──────────────┐
│  Master (RW) │───────▶│  Worker (RO) │ (read replica)
└──────────────┘        └──────────────┘
   Write-ahead log
```

**Replication Lag**: Workers lag behind master. Mitigations:
- Read from master for critical reads
- Accept eventual consistency for non-critical reads

**Failover**: If master fails, promote a worker:
- Manual: DBA promotes (safe, slow)
- Automatic: Consensus algorithm (fast, can cause split-brain)

### 5. Consistency Models

**Strong Consistency:** All reads return latest write.
- Example: Banks (money never disappears)
- Cost: Higher latency, lower availability

**Eventual Consistency:** Reads may be stale, but all replicas converge over time.
- Example: YouTube view counts (slight delays OK)
- Benefit: Higher availability, lower latency

**Causal Consistency:** If B causes C, all readers see B before C.
- Example: Social media comments (if I like your post, you should see the like)

### 6. Load Balancing

**Strategies:**
- **Round-Robin**: Distribute requests equally (simplest, ignores server capacity)
- **Least Connections**: Route to server with fewest active connections
- **Weighted**: Route based on server capacity
- **Hash-Based**: Route based on key (ensures same key goes to same server for stateful sessions)

**Health Checks**: Periodically verify servers are healthy; remove failed ones.

## Key Takeaways

1. **Vertical scaling** is simpler but hits limits; **horizontal scaling** is necessary at scale
2. **Caching** is powerful but invalidation is hard
3. **Sharding** distributes load but introduces complexity
4. **Replication** enables availability; manage consistency trade-offs
5. **Load balancing** distributes traffic but adds latency

## Further Reading

- Kleppmann, M. (2017). *Designing Data-Intensive Applications*.
- Coulouris, G., Dollimore, J., Kindberg, T., & Blair, G. (2011). *Distributed Systems: Concepts and Design*.
