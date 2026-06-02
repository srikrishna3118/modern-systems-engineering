# Case Study: Google Spanner – Globally Distributed Database with Strong Consistency

## Overview

Google Spanner is a globally distributed relational database that provides strong consistency and external consistency (ordering of transactions across the globe) without relying on a single leader. Spanner powers critical Google services including Adwords, Photos, and Gmail.

## Key Challenges

- **Global Consistency**: Maintain ACID properties across data replicated in multiple continents
- **Availability**: Tolerate data center failures without sacrificing consistency
- **Latency**: Low-latency reads/writes despite global replication
- **Schema Evolution**: Change schemas on live databases serving billions of users

## Architecture Highlights

- **Paxos Replication**: Each shard is replicated across data centers using Paxos consensus. The Paxos leader handles writes; followers can serve reads
- **TrueTime**: GPS + atomic clocks provide globally synchronized time with bounded error. Commit timestamps are assigned based on TrueTime, enabling external consistency
- **Two-Phase Commit**: Distributed transactions across shards use 2PC; prepared reads are timestamp-ordered
- **Shard Management**: Splits/merges automatically as data grows/shrinks; no manual resharding

## Technology Stack

- C++ (database engine), custom Paxos implementation
- TrueTime API (GPS + atomic clocks), custom RPC
- Colossus (distributed storage), BigTable-inspired schema

## Lessons Learned

1. **TrueTime solves external consistency** — Bounded-error global clocks enable globally consistent transactions without complex ordering logic
2. **Paxos replicas can serve reads** — Followers can serve read-only transactions without becoming stale; enables read scaling
3. **Two-phase commit is feasible at scale** — Spanner proves 2PC works globally if latency requirements are realistic (10s of ms)
4. **Consistency is not the bottleneck; availability is** — Modern globally distributed systems should default to strong consistency when it doesn't compromise availability

## Further Reading

- [Spanner: Google's Globally-Distributed Database (OSDI 2012)](https://research.google/publications/spanner-googles-globally-distributed-database/)
- [Spanner, TrueTime & The CAP Theorem (Google Cloud Blog)](https://cloud.google.com/blog/)
