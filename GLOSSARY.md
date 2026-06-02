# Systems Engineering Glossary

A reference guide for key concepts, patterns, and terminology used throughout the curriculum.

---

## Distributed Systems Concepts

**CAP Theorem**: States that a distributed system can guarantee at most 2 of 3 properties: Consistency (all nodes see the same data), Availability (system remains operational), and Partition Tolerance (system continues despite network failures).

**Consensus**: Agreement among distributed nodes on a value or state, even when some nodes fail. Algorithms like Raft and Paxos solve this.

**Consistency Models**:
* **Strong Consistency**: All reads return the most recent write
* **Eventual Consistency**: Reads eventually reflect all writes
* **Causal Consistency**: Causally-related operations are ordered consistently
* **Session Consistency**: Reads/writes within a session are consistent

**Distributed Tracing**: End-to-end tracking of a request as it flows through multiple services, used for debugging and optimization.

**Fault Tolerance**: System's ability to continue operating despite component failures. Measured by MTBF (Mean Time Between Failures) and MTTR (Mean Time To Repair).

**Idempotency**: An operation produces the same result whether executed once or multiple times. Critical for payment systems and retries.

**Quorum**: Minimum number of nodes (typically majority) that must agree for a decision. Ensures consistency under failures.

**Replication**: Maintaining copies of data on multiple nodes for availability and fault tolerance. Types: master-replica, multi-master, peer-to-peer.

**Sharding/Partitioning**: Dividing data across multiple nodes by a key, enabling horizontal scaling. Hash sharding distributes uniformly; range sharding keeps similar data together.

---

## Scaling Patterns

**Horizontal Scaling**: Adding more machines/nodes to distribute load and increase capacity.

**Vertical Scaling**: Increasing resources (CPU, RAM) of existing machines.

**Caching**: Storing frequently-accessed data in fast, temporary storage (in-memory). Patterns:
* **Look-Aside**: Client checks cache first, fetches from DB if miss
* **Write-Through**: Write to cache and DB together
* **Write-Behind**: Write to cache first, async flush to DB

**Load Balancing**: Distributing requests across multiple servers. Strategies:
* **Round-Robin**: Send to each server in turn
* **Least Connections**: Send to server with fewest active connections
* **Hash-Based**: Route to same server based on request hash
* **Geographic**: Route based on location

**Read Replicas**: Secondary copies of data for reads, keeping primary for writes. Enables read scaling without write scaling limitations.

---

## Data Systems

**ACID**: Properties ensuring reliable database transactions:
* **Atomicity**: Transaction fully succeeds or fully fails
* **Consistency**: Database stays in valid state
* **Isolation**: Concurrent transactions don't interfere
* **Durability**: Committed data persists despite failures

**BASE**: Weaker consistency for distributed systems:
* **Basically Available**: System responds to all requests
* **Soft State**: State may change without updates
* **Eventually Consistent**: Consistency achieved over time

**Transactions**: Grouped operations treated as atomic unit. Serial, snapshot isolation, or other levels prevent anomalies.

**MVCC (Multi-Version Concurrency Control)**: Maintains multiple versions of data to allow concurrent reads and writes without locking.

**Bloom Filter**: Space-efficient probabilistic data structure to test set membership with possible false positives, never false negatives.

**Inverted Index**: Index from content words to document locations, used for full-text search.

---

## Architecture Patterns

**API Gateway**: Single entry point routing requests to different backend services. Handles authentication, rate limiting, request transformation.

**Circuit Breaker**: Prevents cascading failures by stopping requests to a failing service temporarily. States: closed (normal), open (failing), half-open (testing).

**Event-Driven Architecture**: Systems communicate via asynchronous events rather than direct calls. Decouples services and improves resilience.

**Microservices**: Breaking monolithic application into small, independent services. Each owns its data and APIs.

**Message Queue**: Decouples producers and consumers. Producer writes to queue; consumer processes asynchronously. Enables backpressure and reliability.

**Pub/Sub**: Many publishers send messages to a topic; many subscribers receive copies. Enables many-to-many communication.

**RPC (Remote Procedure Call)**: Calling a function on a remote machine as if local. gRPC, Thrift, JSONRPC are implementations.

**Service Discovery**: Finding location of services in a distributed system. Approaches: DNS, registry (Consul, etcd), load balancer.

**Strangler Pattern**: Gradually replacing a monolith with microservices by intercepting calls and routing to new implementation incrementally.

---

## Real-Time & Streaming

**Backpressure**: Limiting producer rate when consumer can't keep up, preventing buffer overflow and memory issues.

**Exactly-Once Semantics**: Guarantee each message is processed and state updated exactly once, even with failures or retries.

**Lag**: Delay between message production and processing. Stream lag = producer position - consumer position.

**Streaming**: Continuous processing of unbounded data streams (vs batch processing of bounded datasets).

**WebSocket**: Full-duplex communication protocol over TCP. Enables real-time bidirectional communication with lower overhead than HTTP polling.

---

## Machine Learning Systems

**Cold Start**: Challenge of making good recommendations for new users/items with no historical data. Solutions: collaborative filtering on similar users, content-based features, exploration.

**Embedding**: Learned vector representation of data (users, items, documents). Maps high-dimensional data to lower-dimensional space preserving similarity.

**Feature Store**: Centralized system managing feature computation, storage, and serving for ML. Ensures consistent features in training and serving.

**Inference**: Making predictions with a trained model. Requires fast serving infrastructure (typically <100ms p99 latency).

**Online Learning**: ML system updating continuously with new data, not in batch batches. Useful for recommendation systems.

**Two-Stage Ranking**: Candidate generation (large, fast retrieval of candidates) → Ranking (smaller, slower scoring of candidates). Balances recall and precision.

---

## Financial Systems

**Debit/Credit**: Double-entry bookkeeping entries. Debit decreases liabilities, credit increases them (or vice versa for assets). Every transaction has matching debit/credit.

**Double-Entry Ledger**: Every financial transaction recorded twice: once as a debit, once as a credit. Ensures accounting equation: assets = liabilities + equity.

**Idempotency Key**: Unique identifier for a request, allowing safe retries. Server uses it to detect and prevent duplicate processing.

**Reconciliation**: Process of verifying that recorded transactions match actual money movements. Catches discrepancies and fraud.

**Settlement**: Final transfer of money between parties, different from authorization.

**Tokenization**: Replacing sensitive payment data (credit card) with unique token, reducing PCI compliance scope.

---

## Cloud & Infrastructure

**Containers**: Lightweight isolated environments bundling code, dependencies, and runtime. Docker is popular implementation.

**Infrastructure as Code (IaC)**: Defining infrastructure (servers, networks, storage) in version-controlled code (Terraform, CloudFormation, Kubernetes manifests).

**Kubernetes**: Container orchestration platform automating deployment, scaling, and management. Scheduling, self-healing, resource management.

**Multi-Tenancy**: Single instance serving multiple customers/users. Requires isolation of data and compute resources.

**Multi-Region**: Deploying systems across geographic regions for availability and latency. Adds complexity: consistency, replication, failover.

**Service Mesh**: Infrastructure layer managing service-to-service communication. Examples: Istio, Linkerd. Provides observability, security, traffic management.

---

## Reliability & Operations

**Availability**: Percentage of time system is operational. "Five nines" = 99.999% uptime = 26 seconds downtime/year.

**Chaos Engineering**: Intentionally introducing failures in production to find weaknesses and verify resilience.

**Graceful Degradation**: System continues serving reduced functionality during failures instead of complete outage.

**Health Checks**: Periodic tests verifying service is healthy. Used for load balancing and auto-recovery.

**Monitoring/Observability**: Systems for collecting metrics, logs, traces to understand system health and debug issues.

**Rate Limiting**: Restricting number of requests per user/IP. Protects against abuse and ensures fair resource sharing. Algorithms: token bucket, sliding window, fixed window.

**Resilience**: System's ability to recover from failures and adapt to changes.

**SLA (Service Level Agreement)**: Contractual commitment on uptime and performance (e.g., 99.9% uptime).

**SLO (Service Level Objective)**: Internal goal for reliability (usually more stringent than SLA).

**SLI (Service Level Indicator)**: Measurable metric tracking SLO compliance (e.g., p99 latency).

---

## Security & Compliance

**Authentication**: Verifying identity (who are you?). Methods: passwords, tokens, certificates, biometrics.

**Authorization**: Verifying permissions (what can you do?). Role-based (RBAC), attribute-based (ABAC), access control lists.

**Encryption**: Converting data to unreadable form using cryptographic keys:
* **In Transit**: Between systems (TLS)
* **At Rest**: Stored on disk
* **In Use**: While processing

**OAuth 2.0**: Standard authorization protocol allowing users to grant third-party apps access without sharing passwords.

**PCI-DSS**: Payment Card Industry compliance standard requiring encryption, access control, monitoring when handling credit cards.

**Rate Limiting**: Preventing abuse by limiting requests per user/IP during time window.

**SSL/TLS**: Cryptographic protocols securing communication over networks. TLS 1.3 is current standard.

---

## Performance Optimization

**Batch Processing**: Grouping multiple requests together for efficiency. Trade-off: latency vs throughput.

**Compression**: Reducing data size for transmission or storage. Algorithms: gzip, brotli, snappy.

**Connection Pooling**: Reusing database/network connections instead of opening new ones each time. Reduces overhead.

**Lazy Loading**: Deferring computation/loading until actually needed, saving resources upfront.

**Memoization**: Caching function results based on inputs to avoid recomputation.

**Pagination**: Breaking large result sets into pages for efficient retrieval and memory usage.

---

## Algorithm & Data Structures

**Consistent Hashing**: Hash-based distribution minimizing redistribution when nodes added/removed. Used in distributed caches and sharding.

**Hash Functions**: Functions mapping data to fixed-size hash, used for indexing, checksums, crypto. Desirable: deterministic, uniform distribution, avalanche effect.

**Merkle Trees**: Tree where parents hash their children. Used in distributed systems to efficiently detect differences.

**Trie**: Tree data structure for storing sequences efficiently, used for autocomplete and IP routing.

---

## Metrics & Math

**Latency**: Time for request to be processed. Measured: p50, p95, p99 percentiles rather than average.

**Throughput**: Requests processed per second. Capacity planning critical for scaling.

**QPS (Queries Per Second)**: Requests per second a system handles.

**Amdahl's Law**: Speedup from parallelization is limited by non-parallelizable portion: speedup = 1 / ((1-P) + P/N) where P is parallelizable fraction, N is processors.

**Little's Law**: Average number of items in system = arrival rate × average time in system. Useful for capacity planning.

---

## Common Acronyms

- **API**: Application Programming Interface
- **CRUD**: Create Read Update Delete
- **DNS**: Domain Name System
- **ER Model**: Entity-Relationship Model
- **ETL**: Extract Transform Load
- **FIFO**: First In First Out
- **LIFO**: Last In First Out
- **NoSQL**: Non-relational databases
- **ORM**: Object-Relational Mapping
- **P2P**: Peer-to-Peer
- **QoS**: Quality of Service
- **REST**: Representational State Transfer
- **SQL**: Structured Query Language
- **TTFB**: Time To First Byte
- **VCS**: Version Control System

---

## References for Deeper Learning

* [Designing Data-Intensive Applications](https://dataintensive.net/) by Martin Kleppmann
* [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/) by Michael Nygard
* [The Art of Computer Systems Performance Analysis](https://www.amazon.com/Art-Computer-Systems-Performance-Analysis/dp/0471503363/) by Raj Jain
* [Building Microservices](https://learning.oreilly.com/library/view/building-microservices/9781491950340/) by Sam Newman

---

See [README.md](README.md) for curriculum overview and [curriculum-roadmap.md](curriculum-roadmap.md) for learning path.
