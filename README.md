# Modern Systems Engineering Curriculum

A practical, **production-focused** curriculum for learning systems engineering through real-world case studies and hands-on labs. This repository contains engineering lessons from 20+ leading tech companies building systems at scale.

## What You'll Learn

* **Distributed Systems**: Consensus, replication, fault tolerance, consistency models
* **Scale**: Horizontal and vertical scaling, sharding, caching, CDNs
* **Reliability**: High availability, disaster recovery, chaos engineering
* **Real-Time**: WebSockets, streaming, event-driven architectures
* **ML Systems**: Feature stores, serving infrastructure, model deployment
* **Financial Systems**: Idempotency, double-entry ledgers, compliance
* **Design Trade-offs**: Consistency vs. availability, latency vs. throughput

## Featured Companies

Netflix, Uber, Airbnb, AWS, Kafka, Google Spanner, YouTube, WhatsApp, Cloudflare, Pinterest, Slack, Spotify, NVIDIA, Shopify, GitHub, Discord, Stripe, Figma, and more.

**The goal is to help engineers understand how production systems actually work — not just theory, but real engineering decisions, trade-offs, and lessons learned at scale.**

---

## 🚀 Start Here

**New to this curriculum?** Read [Getting Started](GETTING_STARTED.md) for a quick-start guide and recommended learning paths.

---

## Course Roadmap

| Course | Topic | Duration | Labs | Key Topics |
|--------|-------|----------|------|-----------|
| **01** | [Engineering Foundations](course-01-engineering-foundations/syllabus.md) | 4 weeks | 2 | SOLID, APIs, reliability, version control |
| **02** | [Distributed Systems](course-02-distributed-systems/syllabus.md) | 5 weeks | 2 ([Chat](course-02-distributed-systems/labs/chat-system), [Kafka](course-02-distributed-systems/labs/kafka-pipeline)) | Consensus, replication, consistency, CAP |
| **03** | [Cloud Infrastructure](course-03-cloud-infrastructure/syllabus.md) | 4 weeks | 1 ([Kubernetes](course-03-cloud-infrastructure/labs/kubernetes-deployment)) | Containers, orchestration, multi-region |
| **04** | [AI Systems](course-04-ai-systems/syllabus.md) | 4 weeks | 1 ([RAG](course-04-ai-systems/labs/rag-ai-assistant)) | Inference, embeddings, vector DBs, serving |
| **05** | [Real-Time Systems](course-05-realtime-systems/syllabus.md) | 3 weeks | 1 ([WebSocket](course-05-realtime-systems/labs/websocket-streaming)) | Streaming, pub/sub, collaboration |
| **06** | [Financial Systems](course-06-financial-systems/syllabus.md) | 3 weeks | 1 ([Ledger](course-06-financial-systems/labs/payment-ledger)) | Idempotency, double-entry, compliance |
| **07** | [Advanced Design](course-07-advanced-system-design/syllabus.md) | 4 weeks | [5 Exercises](course-07-advanced-system-design/exercises/system-design-exercises.md) | Design trade-offs, interview prep |
| **Capstone** | [Project Guide](capstone-project/project-guide.md) | 4–6 weeks | [4 Templates](capstone-project/templates/) | Full-stack system design |

---

## Quick Navigation

**🎓 Lectures** (every course)
* Course 01: [Engineering Fundamentals](course-01-engineering-foundations/lectures/lecture-01-engineering-fundamentals.md), [Building Scalable Systems](course-01-engineering-foundations/lectures/lecture-02-building-scalable-systems.md)
* Course 02: [Distributed Fundamentals](course-02-distributed-systems/lectures/lecture-01-distributed-fundamentals.md), [Event-Driven Systems](course-02-distributed-systems/lectures/lecture-02-event-driven-systems.md), [Partitioning and Fault Tolerance](course-02-distributed-systems/lectures/lecture-03-partitioning-and-fault-tolerance.md)
* Course 03: [Cloud, Networking, and Security](course-03-cloud-infrastructure/lectures/lecture-01-cloud-networking-security.md), [IaC, Kubernetes, Serverless, and Cost](course-03-cloud-infrastructure/lectures/lecture-02-iac-kubernetes-serverless-finops.md)
* Course 04: [ML Systems, Data, and Training](course-04-ai-systems/lectures/lecture-01-ml-systems-data-training.md), [Serving, MLOps, and Monitoring](course-04-ai-systems/lectures/lecture-02-serving-mlops-monitoring.md)
* Course 05: [Events, Streams, and Windows](course-05-realtime-systems/lectures/lecture-01-events-streams-windows.md), [WebSockets, Latency, and Backpressure](course-05-realtime-systems/lectures/lecture-02-websockets-latency-backpressure.md)
* Course 06: [Payments and Idempotency](course-06-financial-systems/lectures/lecture-01-payments-idempotency-availability.md), [Compliance, Fraud, and Audit](course-06-financial-systems/lectures/lecture-02-compliance-fraud-audit.md)
* Course 07: [Scale](course-07-advanced-system-design/lectures/lecture-01-designing-for-scale.md), [Multi-region](course-07-advanced-system-design/lectures/lecture-02-global-multi-region.md), [Databases](course-07-advanced-system-design/lectures/lecture-03-database-selection.md), [Rate limiting](course-07-advanced-system-design/lectures/lecture-04-rate-limiting.md), [Zero trust](course-07-advanced-system-design/lectures/lecture-05-security-zero-trust.md), [Interview communication](course-07-advanced-system-design/lectures/lecture-06-system-design-interviews.md)

**💼 Case Studies** (production systems; index in [case-studies/README.md](case-studies/README.md))
* [All Case Studies →](case-studies/README.md)
* **Messaging Systems**: [WhatsApp](case-studies/whatsapp-messaging-system.md), [Slack](case-studies/slack-message-queue.md), [Discord](case-studies/discord-chat-infrastructure.md)
* **Search & Discovery**: [Uber](case-studies/uber-dispatch-system.md), [Airbnb](case-studies/airbnb-search-platform.md), [Pinterest](case-studies/pinterest-feed-ranking.md), [GitHub](case-studies/github-code-search.md)
* **Streaming & Media**: [Netflix](case-studies/netflix-streaming-architecture.md), [YouTube](case-studies/youtube-video-delivery.md), [Figma](case-studies/figma-realtime-collaboration.md)
* **Data & Infrastructure**: [Kafka](case-studies/kafka-event-streaming.md), [Google Spanner](case-studies/google-spanner-consistency.md), [AWS Cells](case-studies/aws-cell-architecture.md)
* **ML & Recommendations**: [Spotify](case-studies/spotify-recommendation-pipeline.md), [NVIDIA GPU](case-studies/nvidia-ai-cluster-architecture.md), [OpenAI Inference](case-studies/openai-inference-infrastructure.md)
* **Payments & Scale**: [Stripe](case-studies/stripe-payment-processing.md), [Shopify Flash Sales](case-studies/shopify-flash-sale-scaling.md), [Uber Microservices](case-studies/uber-microservices-migration.md)

**🛠️ Labs** (8 hands-on projects with starter code & solutions)
* [API Task Service](course-01-engineering-foundations/labs/api-task-service) → API contracts, validation, pagination
* [Reliability Toolkit](course-01-engineering-foundations/labs/reliability-toolkit) → Retries, backoff, circuit breaker
* [Chat System (gRPC)](course-02-distributed-systems/labs/chat-system) → Bidirectional streaming, chat rooms
* [Kafka Pipeline](course-02-distributed-systems/labs/kafka-pipeline) → Event ingestion, analytics aggregation
* [Kubernetes Deployment](course-03-cloud-infrastructure/labs/kubernetes-deployment) → Health checks, scaling, resource limits
* [WebSocket Streaming](course-05-realtime-systems/labs/websocket-streaming) → Real-time pub/sub, backpressure handling
* [RAG AI Assistant](course-04-ai-systems/labs/rag-ai-assistant) → Embeddings, semantic search, LLM generation
* [Payment Ledger](course-06-financial-systems/labs/payment-ledger) → Double-entry bookkeeping, idempotency

**🏗️ Architecture Reference**
* [Architecture Diagrams Guide](architecture-diagrams-guide.md) — 12 patterns: scaling, caching, replication, partitioning, microservices, event-driven, global distribution, search, streaming, security, monitoring

**📋 System Design Exercises** (Interview-style problems)
* [5 Advanced Exercises](course-07-advanced-system-design/exercises/system-design-exercises.md)
  * Design a URL Shortener
  * Real-Time Notification System
  * Rate Limiter (Token Bucket, Sliding Window)
  * Full-Text Search Engine
  * Video Streaming Platform

**🚀 Capstone Projects** (4 complete project templates)
* [AI Knowledge Platform](capstone-project/templates/ai-knowledge-platform.md) — RAG system with embeddings and retrieval
* [Global Chat Platform](capstone-project/templates/global-chat-platform.md) — Multi-region WebSockets with consistency
* [Payment Processing](capstone-project/templates/payment-processing-platform.md) — Double-entry ledger with idempotency
* [Feed Ranking System](capstone-project/templates/feed-ranking-system.md) — ML-based personalization with two-stage ranking
* [Complete Guide](capstone-project/project-guide.md) — Starting, scoping, and completing your capstone

---

## 📚 Reference & Support

**📖 [Glossary](GLOSSARY.md)** — 100+ key terms and concepts used throughout the curriculum (distributed systems, scaling, databases, ML systems, etc.)

**🔗 [Resources & References](RESOURCES.md)** — Curated books, blogs, papers, tools, communities, and newsletters
* Recommended books (Kleppmann, Nygard, Newman, Google SRE)
* Company engineering blogs (Netflix, Uber, Stripe, Discord, etc.)
* Essential papers (Google File System, Spanner, Cassandra, Raft)
* Tools and technologies (Docker, Kubernetes, Kafka, databases)
* Staying current (newsletters, podcasts, influencers)

## Repository Structure

```
modern-systems-engineering/
├── README.md
├── curriculum-roadmap.md
├── architecture-diagrams-guide.md         # 12 architecture patterns
│
├── case-studies/                          # 20+ production systems
│   ├── netflix-streaming-architecture.md
│   ├── uber-dispatch-system.md
│   ├── kafka-event-streaming.md
│   └── ... (15 more case studies)
│
├── course-01-engineering-foundations/
│   ├── syllabus.md
│   ├── lectures/
│   │   ├── lecture-01-engineering-fundamentals.md
│   │   └── lecture-02-building-scalable-systems.md
│   └── case-studies/
│
├── course-02-distributed-systems/
│   ├── syllabus.md
│   ├── lectures/
│   │   ├── lecture-01-distributed-fundamentals.md
│   │   ├── lecture-02-event-driven-systems.md
│   │   └── lecture-03-partitioning-and-fault-tolerance.md
│   ├── labs/
│   │   ├── chat-system/          (gRPC, bidirectional streaming)
│   │   └── kafka-pipeline/       (events, analytics aggregation)
│   └── case-studies/
│
├── course-03-cloud-infrastructure/
│   ├── syllabus.md
│   ├── lectures/
│   ├── labs/
│   │   └── kubernetes-deployment/  (Docker, K8s manifests, health probes)
│   └── case-studies/
│
├── course-04-ai-systems/
│   ├── syllabus.md
│   ├── lectures/
│   ├── labs/
│   │   └── rag-ai-assistant/    (embeddings, vector DB, LLM)
│   └── case-studies/
│
├── course-05-realtime-systems/
│   ├── syllabus.md
│   ├── lectures/
│   ├── labs/
│   │   └── websocket-streaming/  (pub/sub, backpressure)
│   └── case-studies/
│
├── course-06-financial-systems/
│   ├── syllabus.md
│   ├── lectures/
│   ├── labs/
│   │   └── payment-ledger/      (double-entry, idempotency)
│   └── case-studies/
│
├── course-07-advanced-system-design/
│   ├── syllabus.md
│   ├── lectures/                       (one lecture per syllabus topic)
│   ├── exercises/
│   │   ├── system-design-exercises.md  (index)
│   │   └── 01-url-shortener.md … 05-video-streaming.md
│   └── case-studies/
│
└── capstone-project/
    ├── project-guide.md
  └── templates/
    ├── ai-knowledge-platform.md
    ├── global-chat-platform.md
    ├── payment-processing-platform.md
    └── feed-ranking-system.md
```

---

---

## Learning Outcomes

After completing this curriculum, you will be able to:

✅ **Design scalable systems** — horizontal scaling, sharding, caching, load balancing
✅ **Build distributed systems** — consensus algorithms, replication, consistency models, fault tolerance
✅ **Deploy cloud infrastructure** — containerization, orchestration, multi-region deployment
✅ **Handle real-time data** — streaming, pub/sub, WebSockets, event-driven architecture
✅ **Serve ML models** — embeddings, vector databases, inference optimization, serving infrastructure
✅ **Build financial systems** — idempotency, double-entry ledgers, compliance, auditability
✅ **Solve system design problems** — make trade-offs, estimate capacity, architect for failures
✅ **Learn from production systems** — understand how Netflix, Uber, Stripe, and others achieve massive scale

---

## How to Use This Repository

### 👥 For Self-Study
1. **Start**: Read [curriculum-roadmap.md](curriculum-roadmap.md) and pick a course
2. **Learn the theory**: Read the lectures linked from that course's syllabus, then the case studies
3. **Get hands-on**: Complete the lab with starter code (try it yourself first!)
4. **Reference solution**: Compare your solution with the provided one
5. **Reinforce**: Study the case study architectures related to that course
6. **Advance**: Move to the next course

### 👨‍🏫 For Instructors
* Use **lectures** as base content for classroom instruction
* Use **case studies** as real-world examples during lectures
* Assign **labs** as homework or in-class exercises
* Reference **system design exercises** for assessment
* Guide capstone projects using provided templates

### 🎯 For Interviews
* Study [Advanced System Design Exercises](course-07-advanced-system-design/exercises/system-design-exercises.md) for interview prep
* Review [case studies](case-studies/) for architectural knowledge
* Reference [Architecture Diagrams Guide](architecture-diagrams-guide.md) to explain trade-offs
* Practice back-of-envelope calculations from labs

### 🚀 For Building Real Products
* Start with **case studies** related to your domain
* Implement a **lab** in your tech stack to understand patterns
* Use **capstone templates** as starting points for your architecture
* Reference **architecture diagrams** when designing systems

---

## Key Features

* **20+ Production Case Studies** — Real systems from Netflix, Uber, Stripe, GitHub, Discord, etc.
* **8 Hands-On Labs** — Progressive difficulty with starter code and complete solutions
* **Lectures for all 7 courses** — one file per major topic, in the same notes style throughout
* **System Design Exercises** — 5 interview-style problems with worked solutions (estimates, mermaid diagrams, trade-offs)
* **4 Capstone Templates** — Complete architectures you can build
* **Architecture Reference Guide** — 12 common patterns with ASCII diagrams
* **Code Examples** — Python, Go, SQL, YAML for cloud-native development

---

## Technology Stack Overview

**Languages**: Python, Go, Node.js, Java
**Databases**: PostgreSQL, MySQL, Cassandra, DynamoDB, MongoDB, Redis, Elasticsearch
**Message Queues**: Kafka, RabbitMQ, Redis Streams  
**Infrastructure**: Kubernetes, Docker, AWS, GCP, Azure
**ML/AI**: Embeddings, Vector Databases (Pinecone/Weaviate), LLMs
**Protocols**: HTTP/REST, gRPC, WebSockets

---

## What's New (Recent Additions)

✨ **20+ Case Studies** — Real production architectures from leading companies
✨ **Labs** — 8 hands-on labs with starter code and reference solutions, each with a run path in its README
✨ **Lecture Notes** — Written lectures for every course, including all six Course 07 topics
✨ **System Design Exercises** — 5 interview-style problems with worked solutions in `course-07-advanced-system-design/exercises/`
✨ **4 Capstone Templates** — Production-ready architecture templates across 4 domains
✨ **Architecture Diagrams Guide** — 12 patterns with ASCII diagrams for quick reference
