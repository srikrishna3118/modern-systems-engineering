# Lecture 1: Engineering Fundamentals

## Overview

This lecture covers the foundational principles of software engineering that underpin all system design.

## Topics

### 1. Design Principles (SOLID)

**Single Responsibility Principle (SRP)**: Each class/module should have one reason to change.
- Example: A User class should handle user data, not database persistence. That's the UserRepository's job.

**Open/Closed Principle (OCP)**: Software entities should be open for extension, closed for modification.
- Example: Use interfaces/abstract classes to extend functionality without changing existing code.

**Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types.
- Example: A `PaymentProcessor` subclass must work anywhere `PaymentProcessor` is expected.

**Interface Segregation Principle (ISP)**: Clients should not depend on interfaces they don't use.
- Example: Don't force a "ReportWriter" class to implement a `send()` method if it only generates reports.

**Dependency Inversion Principle (DIP)**: Depend on abstractions, not concrete implementations.
- Example: Inject a `Logger` interface, not a specific `FileLogger` implementation.

### 2. Systems Thinking

Large systems have emergent properties that can't be predicted from individual components.

**Feedback Loops:**
- **Positive feedback**: Actions amplify effects (e.g., viral growth, cascading failures)
- **Negative feedback**: Actions dampen effects (e.g., load balancing, error correction)

**Cascading Failures**: One failure triggers others. Mitigation:
- Isolation (bulkheads)
- Graceful degradation
- Circuit breakers

### 3. Reliability Principles

**MTBF (Mean Time Between Failures)**: How often failures occur.
**MTTR (Mean Time To Recover)**: How quickly systems recover.

Availability = MTBF / (MTBF + MTTR)

**Fault Tolerance**: System continues operating despite component failures.
- Replication (redundancy)
- Failover mechanisms

**Resilience**: System's ability to recover from failures.
- Exponential backoff
- Bulkhead isolation
- Timeouts

### 4. API Design

**REST Principles:**
- **Resources** are the nouns (users, orders, products)
- **HTTP verbs** are the operations (GET, POST, PUT, DELETE)
- **Stateless**: Each request contains all necessary context
- **Cacheable**: Responses should indicate cacheability

**Example:**
```
GET /users/123             # Fetch user
POST /users                # Create user
PUT /users/123             # Update user
DELETE /users/123          # Delete user
```

**Versioning:** Use `/v1/`, `/v2/` in URL to support multiple versions.

### 5. Version Control Best Practices

**Branching Strategy (Git Flow):**
- `main`: Production-ready code; always deployable
- `develop`: Integration branch; staging code
- `feature/xyz`: Feature branches; write commits here

**Commit Messages:** Clear, atomic commits that explain "why", not just "what".
```
Good: "Add user authentication via JWT tokens"
Bad: "fix bug"
```

## Key Takeaways

1. **SOLID principles** reduce coupling and improve maintainability
2. **Systems thinking** prevents cascading failures
3. **Reliability is a feature**, not an afterthought
4. **APIs** are contracts; version carefully
5. **Version control** discipline enables safe collaboration

## Further Reading

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*.
- Newman, S. (2015). *Building Microservices*.
- Fowler, M., & Beck, K. (2006). *Refactoring: Improving the Design of Existing Code*.
