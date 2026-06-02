# Case Study: Uber Microservices Migration – Breaking the Monolith

## Overview

Uber's transition from a monolithic Python codebase to microservices is a canonical example of migrating a large system while maintaining velocity. The company moved from a single Rails/Python application to 1000+ microservices without downtime.

## Key Challenges

- **Continuous Deployment**: Thousands of developers deploying changes daily; avoid breaking deployments
- **Backward Compatibility**: Microservices must coexist with the monolith during transition; maintain API compatibility
- **Service Discovery**: Dynamically locate services as they scale and move
- **Distributed Debugging**: Track requests across hundreds of services for observability

## Architecture Highlights

- **Strangler Pattern**: New services wrap monolith functionality; requests route to either service or monolith based on feature flags
- **Schemaless RPC (uRPC)**: Custom RPC framework with versioning and backward compatibility
- **Eureka Service Discovery**: Each service registers itself; clients discover services dynamically
- **Distributed Tracing**: Jaeger/X-Ray tracing across service boundaries for debugging

```
┌─────────────────────────────────────────┐
│         API Gateway                      │
├─────────────────────────────────────────┤
│    Feature Flags (route to old/new)     │
├─────┬─────────────────────────────┬─────┤
│     │                             │     │
│  Old Monolith              New Microservices
│  (Python)                  (Go/Java/Node)
│                            ↓
│                    Service Discovery
│                    (Eureka)
└─────────────────────────────────────────┘
```

## Technology Stack

- uRPC (Uber's RPC framework), Eureka (Netflix's service registry)
- Feature flags (Uber's A/B testing), Jaeger (distributed tracing)
- Kafka (event bus for eventual consistency between services)

## Lessons Learned

1. **Feature flags enable gradual transition** — Route requests to old or new implementation based on flags; no big bang cutover
2. **Backward compatibility in RPC is essential** — Old and new services must interoperate; versioning in protocols is critical
3. **Service discovery is non-negotiable** — Manual configuration doesn't scale; dynamic discovery is necessary
4. **Distributed tracing prevents microservices chaos** — Without tracing, debugging failures across hundreds of services is impossible
5. **Ownership model changes with microservices** — Small teams own services end-to-end (not separated by function)

## Further Reading

- [Uber Engineering: Towards Operationalizing Machine Learning](https://uber.com/en-US/blog/engineering/)
- [From Monolith to Microservices (Hailo Case Study)](https://www.infoq.com/presentations/hailo-migration-microservices/)
