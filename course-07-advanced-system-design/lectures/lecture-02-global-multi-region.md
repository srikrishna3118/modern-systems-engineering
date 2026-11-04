# Lecture 2: Global System Design and Multi-Region Architectures

## Overview

A single region fails. A second region introduces split brain, replication lag, and data-residency rules. This lecture covers when to leave one region, how to place data, and how to fail over without corrupting state.

## Topics

### 1. Why leave one region

Move to multiple regions for one of these reasons, and name which one you are solving:

- **Latency.** A user in Frankfurt should not round-trip to Virginia for every click. Speed of light is about 1 ms per 100 km, and real paths are worse.
- **Availability.** A region-level outage (power, network, control-plane bug) should not take the product down.
- **Durability and compliance.** Some data must stay in-country, or must survive the loss of a whole site.

These goals pull in different directions. Low latency wants the write to land near the user. Strong consistency wants one writer. Compliance wants a fixed region. Write the goal down before picking an active-active design you do not need.

### 2. Deployment shapes

**Active-passive.** One region serves traffic. Another holds a replica and takes over on failure.

- Failover time is the detection interval plus DNS or load-balancer cutover, often minutes unless you automate it.
- Replication is usually asynchronous, so failover can lose the last seconds of writes. For a ledger, that is unacceptable. For a feed, it is often fine.
- Operationally the simplest multi-region design.

**Active-active, partitioned.** Each region owns a slice of the keyspace (users pinned to a home region). Writes for a user stay in that region. Other regions can serve stale reads or proxy writes home.

- Avoids cross-region write conflicts.
- A user who travels, or data that must be global (a unique username), still needs a plan.

**Active-active, shared.** Any region accepts writes for any key. Conflicts are resolved by last-writer-wins, CRDTs, or a global consensus layer.

- Best latency for writes.
- Highest application complexity. Use it only when the data model can merge conflicts safely.

```
   users in EU                         users in US
        │                                   │
        ▼                                   ▼
 ┌─────────────┐                     ┌─────────────┐
 │  EU region  │──── async replica ─▶│  US region  │
 │  home: eu-* │◀─── async replica ──│  home: us-* │
 └─────────────┘                     └─────────────┘
        writes for eu-* stay in EU
```

### 3. Replication and the user-visible lag

Asynchronous replication means a read in another region can miss the latest write. Handle it explicitly:

- **Read-your-writes.** After a user writes, route that user's reads to the primary (or pass a token the replica must catch up to) for a short window.
- **Monotonic reads.** Pin a session to one replica so time does not appear to go backwards.
- **Critical reads.** Account balance, inventory count, and permission checks read from the leader. Profiles and feeds can be stale.

Synchronous cross-region replication gives you a stronger story and a latency floor of a full inter-region round trip on every write. Google Spanner pays that cost, with TrueTime, because the product promise is external consistency. Most products should not.

### 4. Failover without split brain

Two regions that both think they are primary will accept conflicting writes. Prevent that:

- **Fencing.** A failed primary must be unable to write after a new primary is promoted. A generation number or a lease checked on every write does this.
- **Quorum.** Promote only with agreement from a majority of regions or an outside witness. A witness in a third region breaks ties.
- **DNS is not a lock.** TTLs and caches mean both regions receive traffic during cutover. The data layer has to tolerate that overlap.

Practice failover. A region you have never failed into is a backup in name only.

### 5. Cells, not just regions

A region is still one large failure domain if every customer shares one database and one deploy. **Cells** (or shards of the whole stack) limit the blast radius: one bad migration takes out a slice of tenants, not all of them. See [AWS Cell Architecture](../../case-studies/aws-cell-architecture.md).

Cell routing sits at the edge. A customer is pinned to a cell. Global features (login, billing identity) stay in a thin control plane that is harder to change and easier to keep available.

### 6. What to put at the edge

Bytes that are large and cacheable (video, images, static JS) belong in a CDN close to the user. Bytes that are small and authoritative (payments, inventory) belong in the home region. Mixing them is how teams accidentally serve personalized data from a shared cache.

[Netflix Open Connect](../../case-studies/netflix-cdn.md) and [YouTube video delivery](../../case-studies/youtube-video-delivery.md) are edge-distribution designs. [Cloudflare's anycast network](../../case-studies/cloudflare-ddos-defense.md) is the same idea applied to attack traffic: spread load across points of presence, decide locally, coordinate globally.

## Key Takeaways

1. **Name the reason** for a second region: latency, availability, or residency. The shape follows from that.
2. **Pin writers to a home region** unless the data model can merge conflicts.
3. **Asynchronous replication loses recent writes on failover.** Say so, and fence the old primary.
4. **Cells bound blast radius** inside a region as well as across regions.
5. **Cacheable bytes go to the edge.** Authoritative bytes stay home.

## Further Reading

- [Google Spanner](../../case-studies/google-spanner-consistency.md) — global consistency and what it costs.
- [AWS Cell Architecture](../../case-studies/aws-cell-architecture.md) — isolation as an availability strategy.
- [Lecture 1: Distributed Systems Fundamentals](../../course-02-distributed-systems/lectures/lecture-01-distributed-fundamentals.md) — CAP, replication, and consensus.
