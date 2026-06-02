# Case Study: AWS Aurora – Cloud-Native Relational Database

## Overview

Amazon Aurora is a MySQL- and PostgreSQL-compatible relational database built for the cloud. It decouples compute from storage, replicates data 6 ways across 3 Availability Zones, and delivers up to 5x the throughput of standard MySQL. Aurora serves as the backbone for thousands of production workloads on AWS, from startups to enterprises.

## Key Challenges

- **Durability**: Database corruption or data loss is unacceptable — even during AZ failures
- **Performance**: Traditional MySQL replication creates write amplification (data, redo log, binlog, double-write buffer)
- **Scaling Reads**: Read replicas in traditional MySQL lag behind the primary by seconds
- **Failover Speed**: Traditional RDS failover takes 60–120 seconds; applications need sub-30s recovery
- **Storage Management**: DBAs should not need to manage disk provisioning, RAID, or volume expansion

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
└────────────┬────────────────────────────┬───────────────┘
             │ Writes                     │ Reads
     ┌───────▼────────┐          ┌───────▼────────┐
     │  Primary (RW)  │          │ Read Replicas   │
     │  MySQL/PG      │          │ (up to 15)      │
     │  Compute Node  │          │  Compute Nodes  │
     └───────┬────────┘          └───────┬─────────┘
             │ Redo Log Records          │ Shared Storage
             │ (only!)                   │ (direct read)
     ┌───────▼──────────────────────────▼──────────────┐
     │          Aurora Storage Service                   │
     │                                                   │
     │  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
     │  │ AZ-1    │  │ AZ-2    │  │ AZ-3    │          │
     │  │ Copy 1  │  │ Copy 3  │  │ Copy 5  │          │
     │  │ Copy 2  │  │ Copy 4  │  │ Copy 6  │          │
     │  └─────────┘  └─────────┘  └─────────┘          │
     │                                                   │
     │  • 6 copies across 3 AZs                         │
     │  • 4/6 write quorum, 3/6 read quorum             │
     │  • 10 GB segments, independently repairable       │
     │  • Continuous backup to S3                         │
     └──────────────────────────────────────────────────┘
```

### The Log-Is-The-Database Insight

Traditional databases write data pages, redo logs, binary logs, and double-write buffers — amplifying every write by 4–6x across the network. Aurora's key insight: **only ship the redo log records to storage**. The storage layer applies redo log records to data pages asynchronously.

This reduces network I/O by **~46x** compared to mirrored MySQL:

| Write Type | Traditional MySQL | Aurora |
|-----------|------------------|--------|
| Data pages | ✅ (network) | ❌ (generated in storage) |
| Redo log | ✅ (network) | ✅ (network) |
| Binary log | ✅ (network) | ❌ |
| Double-write buffer | ✅ (network) | ❌ |
| FRM files | ✅ (network) | ❌ |

### Quorum Model

Aurora uses a **4/6 write quorum** and **3/6 read quorum** across 6 copies in 3 AZs:

- **Tolerates losing an entire AZ** (2 copies) without losing write availability
- **Tolerates losing an AZ + 1 additional node** without losing read availability
- Each storage volume is divided into **10 GB segments** — failure detection and repair happens at the segment level, not the volume level
- Mean Time to Repair (MTTR) for a 10 GB segment: ~10 seconds

### Read Replicas

Aurora read replicas share the same storage volume as the primary — no replication lag from data copying. Replicas receive a stream of redo log records and apply them to their in-memory buffer cache. Typical replication lag: **< 20ms**.

### Failover

Aurora failover promotes a read replica to primary in **< 30 seconds** (typically ~15s). Since storage is shared, the new primary does not need to replay a transaction log from scratch — it only needs to process any redo log records not yet applied to its cache.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Compute | Modified MySQL/PostgreSQL engines |
| Storage | Custom distributed storage (C++), SSD-backed |
| Replication | Redo log shipping (asynchronous to replicas) |
| Backup | Continuous to S3, point-in-time restore |
| Networking | AWS proprietary (25Gbps between compute and storage) |

## Design Decisions

### Why Quorum over Consensus?
Aurora uses quorum-based writes (4/6) rather than a Raft/Paxos consensus protocol. This allows writes to proceed as long as 4 of 6 storage nodes acknowledge — without a leader election protocol at the storage layer. The database compute node acts as the single writer, simplifying conflict resolution.

### Why 10 GB Segments?
Segment size is chosen so that a failed segment can be re-replicated in ~10 seconds over a 10 Gbps network link. This keeps the window of vulnerability (time with reduced redundancy) extremely small.

### Separation of Compute and Storage
By decoupling compute from storage, Aurora enables:
- Instant read replica creation (no data copy)
- Independent scaling of compute (instance size) and storage (auto-grows to 128 TB)
- Storage-level replication instead of statement/row-based replication

## Lessons Learned

1. **"The log is the database"** — Shipping only redo logs over the network, and materializing pages in storage, dramatically reduces write amplification and network I/O.

2. **Quorum systems with small segments enable fast repair** — 10 GB segments mean repairs complete in seconds, keeping the probability of data loss vanishingly small (< 10⁻²⁰ annual probability for a 2/6 failure).

3. **Shared storage eliminates replica lag** — When replicas read from the same storage, replication lag drops from seconds (MySQL binlog replication) to milliseconds.

4. **Segment-level fault isolation beats volume-level** — Failures are isolated to 10 GB units, not entire volumes. This enables parallel repair across thousands of segments.

5. **Cloud-native means rethinking, not just migrating** — Aurora is not MySQL deployed on VMs. It is a fundamental rearchitecture for the cloud, keeping MySQL compatibility at the SQL layer while replacing the storage engine entirely.

## Further Reading

- [Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases (SIGMOD 2017)](https://www.amazon.science/publications/amazon-aurora-design-considerations-for-high-throughput-cloud-native-relational-databases)
- [Amazon Aurora: On Avoiding Distributed Consensus for I/Os, Commits, and Membership Changes (SIGMOD 2018)](https://www.amazon.science/publications/amazon-aurora-on-avoiding-distributed-consensus-for-i-os-commits-and-membership-changes)
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/)
