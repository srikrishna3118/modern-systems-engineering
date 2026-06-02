# Case Study: Uber Dispatch System – Real-Time Matching at Scale

## Overview

Uber's dispatch system matches millions of riders with drivers in real-time across hundreds of cities, handling over 7 million trips per day. The system must solve a complex optimization problem (matching supply to demand) in sub-second latency with 99.99% availability.

## Key Challenges

- **Scale**: Sub-second decisions for millions of concurrent users globally
- **Latency**: Matching must complete in < 500ms from request to acceptance
- **Geography**: Efficiently index and query millions of driver locations
- **Fairness**: Balance driver earnings and rider wait times while maintaining utilization

## Architecture Highlights

- **Geospatial Indexing**: Google S2 geometry library (later H3 hexagonal cells) partitions the globe into hierarchical cells
- **Supply/Demand Demand Modeling**: Predictive models forecast driver shortages and route drivers proactively
- **Dispatch Engine**: In-memory matching service that ranks compatible driver-rider pairs using ML-trained scoring functions
- **Event-Driven**: Kafka-based event bus decouples matching logic from notifications and analytics

## Technology Stack

- Go (dispatch service), Python (ML models)
- Cassandra (rider/driver data), Redis (caching)
- H3 library (geospatial), Kafka (events), multi-region AWS

## Lessons Learned

1. **Hierarchical geospatial indexing is foundational** — H3 hexagons scale from global to building-level precision
2. **Proactive repositioning beats reactive matching** — Predicting demand and moving drivers early reduces wait times
3. **Event-driven decoupling enables independent teams** — Matching, notifications, and analytics iterate separately
4. **Machine learning for matching, not just ranking** — ML models learn pickup locations, surge pricing, and driver acceptance probability

## Further Reading

- [Uber Engineering: H3 — Uber's Hexagonal Hierarchical Spatial Index](https://eng.uber.com/h3/)
- [Ringpop: Helping Hundreds of Services Do Efficient Peer Discovery](https://eng.uber.com/ringpop/)
