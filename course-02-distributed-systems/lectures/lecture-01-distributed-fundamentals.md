# Lecture 1: Distributed Systems Fundamentals

## Overview

Distributed systems power the internet. This lecture covers the fundamental challenges and patterns that emerge when systems span multiple machines.

## Topics

### 1. The Two Generals Problem

Two armies want to coordinate an attack. They can only communicate via unreliable message (might be lost).

**Key Insight:** Without a perfect communication channel, there's no protocol that guarantees both generals know the other has received the message.

**Real-World Impact:** Distributed systems can never guarantee that all nodes have synchronized state in the presence of network failures.

### 2. CAP Theorem

Any distributed system can guarantee **at most two** of the three properties:

- **Consistency**: All nodes see the same data
- **Availability**: System continues to operate despite failures
- **Partition Tolerance**: System survives network partitions

**In Practice:**
- You can't avoid partitions (networks fail), so you choose **AP** or **CP**
- **CP (Consistency + Partition)**: Wait for consensus; some requests fail (e.g., Google Spanner)
- **AP (Availability + Partition)**: Respond immediately; accept eventual consistency (e.g., DynamoDB, Cassandra)

### 3. Consensus Algorithms

Multiple nodes must agree on a value despite failures.

**Raft Consensus:**
1. One node becomes **leader** (elected by majority)
2. Leader proposes values; followers acknowledge
3. Once majority acknowledges, value is committed
4. Followers apply committed values to their state

**Properties:**
- Tolerates up to (N-1)/2 failures with N nodes
- External consistency: Total ordering of commits
- Election: New leader if old leader fails (few seconds latency)

**Visual:**
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Master  │────▶│ Follower│     │Follower │
│ (Leader)│     └─────────┘     └─────────┘
└─────────┘            ▲              ▲
                       └──────┬───────┘
              (acknowledge commit)
```

### 4. Replication Strategies

**Primary-Secondary (Master-Worker):**
- One primary receives all writes
- Secondaries replicate asynchronously
- Pros: Simple, low write latency
- Cons: Replication lag, failover complexity

**Multi-Master Replication:**
- Multiple nodes accept writes
- Changes propagate to other nodes
- Pros: High availability, low latency
- Cons: Conflict resolution complexity, potential for inconsistency

**Quorum-Based:**
- Reads and writes require quorum acknowledgment
- Example: 3 replicas, read from 2, write to 2
- Pros: Balanced latency and consistency
- Cons: More complex, requires enough replicas

### 5. Failure Modes

**Crash Failures:** Node stops responding (easiest to detect and handle)

**Byzantine Failures:** Node behaves arbitrarily (sends incorrect data, lies). Requires Byzantine Fault Tolerant (BFT) algorithms; 3F+1 nodes needed to tolerate F failures.

**Network Failures:** Messages lost, delayed, or reordered.
- Mitigation: Timeouts, retries, idempotency

### 6. Service Discovery

**Static Configuration:** Hard-coded server addresses (breaks on scale)

**DNS:** Domain-name lookup, but has caching issues (stale entries)

**Service Registry (Dynamic):** Central registry of available services
- Services register/deregister on startup/shutdown
- Clients query registry for available instances
- Examples: Consul, etcd, Eureka

**Health Checks:** Periodically verify services are healthy; remove unhealthy ones

### 7. RPC (Remote Procedure Call)

**Goal:** Make calling a remote function feel like a local call.

**Challenges:**
- **Network failures:** Call might have succeeded but response lost (idempotency required)
- **Latency:** Remote calls are 100–1000x slower than local function calls
- **Partial failures:** Some nodes might be down; client must handle gracefully

**Patterns:**
- **Timeout:** Declare call failed after X milliseconds
- **Retry:** Resubmit request; requires idempotency
- **Circuit Breaker:** Stop sending requests if service is down; retry periodically

## Key Takeaways

1. **Distribution is hard**: The Two Generals Problem shows fundamental limits
2. **CAP theorem**: Choose two of three; network partitions are inevitable
3. **Consensus** (Raft) enables strong consistency in distributed systems
4. **Replication** provides availability; choose strategy based on latency/consistency needs
5. **Service discovery** is essential for dynamic systems
6. **Resilience patterns** (timeout, retry, circuit breaker) prevent cascading failures

## Further Reading

- Lamport, L. (1998). *The Part-Time Parliament* (Paxos)
- Ongaro, D., & Ousterhout, J. (2014). *In Search of an Understandable Consensus Algorithm (Raft)*
- Brewer, E. (2000). *Towards Robust Distributed Systems (CAP Theorem)*
