# Curriculum Roadmap

A structured learning path from engineering fundamentals to advanced system design. Each course builds on previous knowledge through lectures, case studies, labs, and capstone projects.

---

## 📚 Course Sequence & Content

### **Course 01: Engineering Foundations** (4 weeks)
**Prerequisite**: None | **Time Investment**: 40 hours

Learn the bedrock principles of software systems engineering—how professional engineers think about problems, design solutions, and build reliable systems.

* **Syllabus**: [course-01-engineering-foundations/syllabus.md](course-01-engineering-foundations/syllabus.md)
* **Lectures**:
  * [Engineering Fundamentals](course-01-engineering-foundations/lectures/lecture-01-engineering-fundamentals.md) — SOLID principles, systems thinking, reliability, API design
  * [Building Scalable Systems](course-01-engineering-foundations/lectures/lecture-02-building-scalable-systems.md) — Scaling strategies, caching, partitioning, replication
* **Related Case Studies**:
  * [AWS Cell Architecture](case-studies/aws-cell-architecture.md) — How AWS isolates systems for reliability
  * [Uber's Microservices Migration](case-studies/uber-microservices-migration.md) — Building systems that scale
* **Labs**:
  * [API Task Service](course-01-engineering-foundations/labs/api-task-service) — contracts, validation, pagination
  * [Reliability Toolkit](course-01-engineering-foundations/labs/reliability-toolkit) — retries, backoff, circuit breaker
* **Time**: Reading (6–8 hrs) + Labs (8–12 hrs)

---

### **Course 02: Distributed Systems** (5 weeks)
**Prerequisite**: Course 01 | **Time Investment**: 50 hours

Master the concepts and patterns required to build systems across multiple computers. Covers consensus, replication, consistency, and real-world architectures.

* **Syllabus**: [course-02-distributed-systems/syllabus.md](course-02-distributed-systems/syllabus.md)
* **Lectures**:
  * [Distributed Fundamentals](course-02-distributed-systems/lectures/lecture-01-distributed-fundamentals.md) — CAP theorem, consensus (Raft), replication, fault tolerance, RPC patterns
  * [Event-Driven Systems](course-02-distributed-systems/lectures/lecture-02-event-driven-systems.md) — commands vs events, the log, idempotent consumers
  * [Partitioning and Fault Tolerance](course-02-distributed-systems/lectures/lecture-03-partitioning-and-fault-tolerance.md) — shard keys, timeouts, retries, fencing
* **Case Studies**:
  * [Netflix Streaming Architecture](case-studies/netflix-streaming-architecture.md) — How Netflix delivers billions of hours of video
  * [Uber Dispatch System](case-studies/uber-dispatch-system.md) — Real-time supply/demand matching at global scale
  * [Kafka Event Streaming](case-studies/kafka-event-streaming.md) — Append-only logs and distributed event processing
  * [Google Spanner](case-studies/google-spanner-consistency.md) — Global consistency without a leader
  * [Discord Chat Infrastructure](case-studies/discord-chat-infrastructure.md) — Scaling from MongoDB to Cassandra to ScyllaDB
* **Labs**:
  * [Chat System (gRPC)](course-02-distributed-systems/labs/chat-system) — Build a scalable chat server with bidirectional streaming
  * [Kafka Pipeline](course-02-distributed-systems/labs/kafka-pipeline) — Event ingestion, partitioning, and real-time analytics
* **Time**: Lectures (8–10 hrs) + Case Studies (8–10 hrs) + Labs (12–16 hrs)

---

### **Course 03: Cloud Infrastructure** (4 weeks)
**Prerequisite**: Course 02 | **Time Investment**: 40 hours

Learn to deploy and operate systems at scale using containers, orchestration platforms, and cloud services.

* **Syllabus**: [course-03-cloud-infrastructure/syllabus.md](course-03-cloud-infrastructure/syllabus.md)
* **Lectures**:
  * [Cloud Foundations, Networking, and Security](course-03-cloud-infrastructure/lectures/lecture-01-cloud-networking-security.md)
  * [IaC, Kubernetes, Serverless, and Cost](course-03-cloud-infrastructure/lectures/lecture-02-iac-kubernetes-serverless-finops.md)
* **Case Studies**:
  * [Kubernetes orchestration](case-studies/kubernetes-orchestration.md) — what the control plane is actually for
  * [AWS Cell Architecture](case-studies/aws-cell-architecture.md) — Distributed system isolation
  * [AWS Aurora](case-studies/aws-aurora.md) — a managed database instead of state on the cluster
* **Labs**:
  * [Kubernetes Deployment](course-03-cloud-infrastructure/labs/kubernetes-deployment) — Deploy containerized apps with health checks, resource limits, scaling
* **Resources**:
  * [Architecture Diagrams Guide](architecture-diagrams-guide.md) — Reference patterns for containers, orchestration, monitoring
* **Time**: Reading (6–8 hrs) + Lab (10–14 hrs)

---

### **Course 04: AI Systems** (4 weeks)
**Prerequisite**: Course 02 | **Time Investment**: 40 hours

Design systems for training, serving, and distributing machine learning models. Covers feature engineering, inference optimization, and production ML pipelines.

* **Syllabus**: [course-04-ai-systems/syllabus.md](course-04-ai-systems/syllabus.md)
* **Lectures**:
  * [ML Systems, Data, and Training](course-04-ai-systems/lectures/lecture-01-ml-systems-data-training.md)
  * [Serving, MLOps, and Monitoring](course-04-ai-systems/lectures/lecture-02-serving-mlops-monitoring.md)
* **Case Studies**:
  * [NVIDIA AI Cluster Architecture](case-studies/nvidia-ai-cluster-architecture.md) — GPU fabric, all-reduce optimization, thermal management
  * [OpenAI Inference Infrastructure](case-studies/openai-inference-infrastructure.md) — Batching, PagedAttention, speculative decoding for LLM serving
  * [Spotify Recommendation Pipeline](case-studies/spotify-recommendation-pipeline.md) — Contextual bandits, ensemble models, cold-start strategies
* **Labs**:
  * [RAG AI Assistant](course-04-ai-systems/labs/rag-ai-assistant) — Semantic search with embeddings, vector databases, LLM generation
* **Time**: Reading (6–8 hrs) + Case Studies (6–8 hrs) + Labs (10–14 hrs)

---

### **Course 05: Real-Time Systems** (3 weeks)
**Prerequisite**: Course 02 | **Time Investment**: 30 hours

Build systems that process and respond to data in near real-time. Covers WebSockets, pub/sub patterns, streaming architectures, and collaboration features.

* **Syllabus**: [course-05-realtime-systems/syllabus.md](course-05-realtime-systems/syllabus.md)
* **Lectures**:
  * [Events, Streams, and Windows](course-05-realtime-systems/lectures/lecture-01-events-streams-windows.md)
  * [WebSockets, Latency, and Backpressure](course-05-realtime-systems/lectures/lecture-02-websockets-latency-backpressure.md)
* **Case Studies**:
  * [Figma Real-Time Collaboration](case-studies/figma-realtime-collaboration.md) — Operational transformation, conflict resolution, real-time sync
  * [Discord Chat Infrastructure](case-studies/discord-chat-infrastructure.md) — Presence, typing indicators, message ordering at scale
  * [WhatsApp Messaging System](case-studies/whatsapp-messaging-system.md) — Erlang/OTP, minimal infrastructure, 100M concurrent users
* **Labs**:
  * [WebSocket Streaming](course-05-realtime-systems/labs/websocket-streaming) — Pub/sub server with backpressure, broadcast patterns, client sync
* **Time**: Reading (4–6 hrs) + Case Studies (4–6 hrs) + Labs (8–10 hrs)

---

### **Course 06: Financial Systems** (3 weeks)
**Prerequisite**: Course 02 | **Time Investment**: 30 hours

Design systems for payments, ledgers, and financial transactions. Covers idempotency, consistency, compliance, and fraud detection.

* **Syllabus**: [course-06-financial-systems/syllabus.md](course-06-financial-systems/syllabus.md)
* **Lectures**:
  * [Payments, Idempotency, and Availability](course-06-financial-systems/lectures/lecture-01-payments-idempotency-availability.md)
  * [Compliance, Fraud, and the Audit Log](course-06-financial-systems/lectures/lecture-02-compliance-fraud-audit.md)
* **Case Studies**:
  * [Stripe Payment Processing](case-studies/stripe-payment-processing.md) — Idempotency keys, ledger architecture, tokenization, compliance
* **Labs**:
  * [Payment Ledger](course-06-financial-systems/labs/payment-ledger) — Double-entry bookkeeping, debit/credit pairs, reconciliation
* **Time**: Reading (4–6 hrs) + Case Studies (4–6 hrs) + Labs (8–10 hrs)

---

### **Course 07: Advanced System Design** (4 weeks)
**Prerequisite**: Courses 02, 03, 05 | **Time Investment**: 40 hours

Apply knowledge across courses to solve complex large-scale system design problems. Prepare for system design interviews.

* **Syllabus**: [course-07-advanced-system-design/syllabus.md](course-07-advanced-system-design/syllabus.md)
* **Lectures**: one per syllabus topic, linked from the [syllabus](course-07-advanced-system-design/syllabus.md) (scale, multi-region, databases, rate limiting, zero trust, interview communication)
* **Case Studies**:
  * [Cloudflare DDoS Defense](case-studies/cloudflare-ddos-defense.md) — Anycast, eBPF, layered filtering
  * [GitHub Code Search](case-studies/github-code-search.md) — code-oriented index, blob dedup, query tier separate from ingestion
  * [Shopify Flash Sale Scaling](case-studies/shopify-flash-sale-scaling.md) — Pre-warming, optimistic locking, inventory sharding
* **Exercises**:
  * [System Design Exercises](course-07-advanced-system-design/exercises/system-design-exercises.md) — 5 worked problems (requirements, estimates, mermaid diagram, trade-offs):
    1. [URL Shortener](course-07-advanced-system-design/exercises/01-url-shortener.md) — id allocation, cache, read-heavy path
    2. [Real-Time Notifications](course-07-advanced-system-design/exercises/02-notification-system.md) — priority isolation, idempotent delivery
    3. [Rate Limiter](course-07-advanced-system-design/exercises/03-rate-limiter.md) — token bucket, one atomic check
    4. [Full-Text Search](course-07-advanced-system-design/exercises/04-full-text-search.md) — derived index, tenant fan-out
    5. [Video Streaming](course-07-advanced-system-design/exercises/05-video-streaming.md) — transcode offline, bytes from a CDN
* **Resources**:
  * [Architecture Diagrams Guide](architecture-diagrams-guide.md) — 12 patterns for trade-off analysis
* **Time**: Reading (6–8 hrs) + Exercises (12–16 hrs) + Practice (8–12 hrs)

---

## 🎓 Capstone Project (4–6 weeks)

Integrate and apply everything you've learned by building a complete production-grade system.

* **Project Guide**: [capstone-project/project-guide.md](capstone-project/project-guide.md)
* **Templates**: [capstone-project/templates/](capstone-project/templates/)
  1. **AI Knowledge Platform** — RAG system with embeddings, vector DB, LLM generation, retrieval ranking
  2. **Global Chat Platform** — Multi-region messaging, WebSockets, presence, offline support, cross-region consistency
  3. **Payment Processing Platform** — Double-entry ledger, idempotency, fraud detection, webhooks
  4. **Feed Ranking System** — ML-based personalization, two-stage ranking, online feature serving, model updates

**Choose one template and:**
* Implement core APIs and data models
* Design distributed system components
* Set up infrastructure (Kubernetes or cloud provider)
* Deploy and demonstrate at scale
* Write architectural documentation

---

## 📊 Learning Path Summary

| Weeks | Course | Topics | Prerequisites |
|-------|--------|--------|---------------|
| 1–4 | **Course 01** | SOLID, APIs, Reliability, Scaling | None |
| 5–9 | **Course 02** | Consensus, Replication, CAP | Course 01 |
| 10–13 | **Course 03** | Containers, K8s, Cloud | Course 02 |
| 14–17 | **Course 04** | ML Systems, Serving, Embeddings | Course 02 |
| 18–20 | **Course 05** | Real-Time, WebSockets, Streaming | Course 02 |
| 21–23 | **Course 06** | Payments, Ledgers, Compliance | Course 02 |
| 24–27 | **Course 07** | Design Trade-offs, Interviews | Courses 02, 03, 05 |
| 28–33 | **Capstone** | Full-Stack System Design | All courses |

**Total Duration**: 33–38 weeks (~8–9 months) | **Total Hours**: ~340–400 hours

---

## 🗺️ All Case Studies

The library is indexed in [case-studies/README.md](case-studies/README.md). Grouped:

**Messaging & Communication** (4)
* [WhatsApp Messaging System](case-studies/whatsapp-messaging-system.md) — Erlang, minimal infra, 100M concurrent users
* [Slack Message Queue](case-studies/slack-message-queue.md) — Consumer groups, ordering, durability
* [Discord Chat Infrastructure](case-studies/discord-chat-infrastructure.md) — Storage evolution, request coalescing, Cassandra to ScyllaDB
* [Figma Real-Time Collaboration](case-studies/figma-realtime-collaboration.md) — Operational transformation, WebSockets, conflict resolution

**Search & Discovery** (4)
* [Uber Dispatch System](case-studies/uber-dispatch-system.md) — H3 geohashing, supply/demand, event-driven dispatch
* [Airbnb Search Platform](case-studies/airbnb-search-platform.md) — ML ranking, feature store, A/B testing
* [Pinterest Feed Ranking](case-studies/pinterest-feed-ranking.md) — Two-stage ranking, graph learning, diversity
* [GitHub Code Search](case-studies/github-code-search.md) — code-oriented index, identical blobs indexed once, rebuildable shards

**Streaming & Media** (3)
* [Netflix Streaming Architecture](case-studies/netflix-streaming-architecture.md) — Open Connect CDN, adaptive bitrate, personalization
* [YouTube Video Delivery](case-studies/youtube-video-delivery.md) — Colossus storage, spot encoding, edge caching
* [Spotify Recommendation Pipeline](case-studies/spotify-recommendation-pipeline.md) — Bandits, ensemble models, cold-start

**Data & Infrastructure** (4)
* [Kafka Event Streaming](case-studies/kafka-event-streaming.md) — Append-only logs, replication, exactly-once
* [Google Spanner Consistency](case-studies/google-spanner-consistency.md) — TrueTime, Paxos, global consistency
* [AWS Cell Architecture](case-studies/aws-cell-architecture.md) — Cell isolation, eventual consistency, graceful degradation
* [NVIDIA AI Cluster Architecture](case-studies/nvidia-ai-cluster-architecture.md) — NVLink fabric, all-reduce, thermal management

**Payments & Scale** (3)
* [Stripe Payment Processing](case-studies/stripe-payment-processing.md) — Idempotent APIs, double-entry ledger, tokenization
* [Shopify Flash Sale Scaling](case-studies/shopify-flash-sale-scaling.md) — Pre-warming, optimistic locking, inventory sharding
* [OpenAI Inference Infrastructure](case-studies/openai-inference-infrastructure.md) — Continuous batching, PagedAttention, speculative decoding
* [Uber Microservices Migration](case-studies/uber-microservices-migration.md) — Strangler pattern, service discovery, distributed tracing

**Security & Optimization** (1)
* [Cloudflare DDoS Defense](case-studies/cloudflare-ddos-defense.md) — Anycast network, eBPF/XDP, layered defense

---

## 🛠️ All Hands-On Labs

**8 progressive labs** with starter code, TODOs, and complete solutions:

1. [API Task Service](course-01-engineering-foundations/labs/api-task-service) — API contracts, validation, pagination
2. [Reliability Toolkit](course-01-engineering-foundations/labs/reliability-toolkit) — Retries, backoff, circuit breaker
3. [Chat System (gRPC)](course-02-distributed-systems/labs/chat-system) — Bidirectional streaming, room management
4. [Kafka Pipeline](course-02-distributed-systems/labs/kafka-pipeline) — Event ingestion, real-time analytics aggregation
5. [Kubernetes Deployment](course-03-cloud-infrastructure/labs/kubernetes-deployment) — Health checks, scaling, resource limits
6. [RAG AI Assistant](course-04-ai-systems/labs/rag-ai-assistant) — Embeddings, semantic search, LLM generation
7. [WebSocket Streaming](course-05-realtime-systems/labs/websocket-streaming) — Pub/sub, broadcast, backpressure handling
8. [Payment Ledger](course-06-financial-systems/labs/payment-ledger) — Double-entry bookkeeping, reconciliation, idempotency

---

## 📖 Recommended Reading Order

**For Beginners** (Start from scratch)
1. Course 01: Engineering Foundations
2. Course 02: Distributed Systems (with Case Studies)
3. Course 03: Cloud Infrastructure
4. Choose your path: AI Systems, Real-Time, or Financial Systems
5. Course 07: Advanced System Design + Capstone

**For Experienced Engineers** (Refresh/Deepen)
1. Review Course 02: Distributed Systems
2. Jump to Course 07: Advanced System Design
3. Deep-dive into relevant case studies by domain
4. Build a capstone project in your area of interest

**For Interview Prep**
1. Course 02: Distributed Systems (core concepts)
2. [System Design Exercises](course-07-advanced-system-design/exercises/system-design-exercises.md)
3. Review case studies in your target domain
4. Reference [Architecture Diagrams Guide](architecture-diagrams-guide.md) for patterns and trade-offs

---

## 💡 How to Navigate This Curriculum

* **Read the syllabus** first for each course to understand goals and prerequisites
* **Read the lectures** linked from the course syllabus and take notes on key concepts
* **Study case studies** to see how real companies solve problems
* **Complete labs** by reading starter code, identifying TODOs, and implementing solutions
* **Reference diagrams** when stuck on architecture questions
* **Compare your solution** with the provided one and understand the differences
* **Discuss and debate** design trade-offs with peers
* **Build the capstone** to integrate everything and create a portfolio project

---

## 🎯 Learning Objectives by Course

**Course 01**: Understand SOLID principles, reliability metrics, API design patterns, and systems thinking
**Course 02**: Master distributed systems concepts, consensus algorithms, and consistency models
**Course 03**: Deploy applications using containers and orchestration platforms
**Course 04**: Design ML pipelines and optimize inference at scale
**Course 05**: Build real-time systems with WebSockets and event streaming
**Course 06**: Design payment and financial infrastructure with strong consistency guarantees
**Course 07**: Apply knowledge to complex system design problems and prepare for interviews
**Capstone**: Build a production-grade system integrating multiple courses

---

## 🚀 Next Steps

1. **Choose your starting point** based on your experience level
2. **Clone or fork** this repository
3. **Set up your development environment** with the recommended tools
4. **Start with Course 01** or jump to a relevant course
5. **Complete labs** and document your learning
6. **Share your capstone project** on GitHub for feedback
7. **Continue learning** from recommended resources and blogs

---

See [README.md](README.md) for quick links and repository overview.

---

## Additional Resources

For deeper learning beyond the curriculum:

* **[Glossary](GLOSSARY.md)** — Reference guide for 100+ key terms (distributed systems, scaling, databases, ML, security, etc.)
* **[Resources & References](RESOURCES.md)** — Curated books, blogs, papers, tools, courses, and communities for continued learning
