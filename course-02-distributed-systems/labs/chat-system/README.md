# Lab: Chat System – gRPC Microservice Architecture

## Overview
Build a distributed chat system using gRPC for inter-service communication. This lab demonstrates service-to-service messaging, bidirectional streaming, and basic service discovery.

## Architecture

```
Client --> API Gateway --> Chat Service --> Message Service
                                       --> User Service
```

See `architecture.png` for a detailed component diagram.

## Learning Objectives
- Define gRPC service contracts using Protocol Buffers.
- Implement bidirectional streaming for real-time messaging.
- Register and discover services using a lightweight registry.

## Prerequisites
- Familiarity with Go or Python.
- Docker installed locally.
- Basic understanding of RPC concepts.

## Getting Started

1. Clone or copy the `starter-code/` directory.
2. Review the `proto/chat.proto` file to understand the service definition.
3. Implement the missing server and client handlers as guided by the inline `TODO` comments.
4. Run the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```
5. Send a test message:
   ```bash
   grpcurl -plaintext localhost:50051 chat.ChatService/SendMessage
   ```

## Deliverables
- Working gRPC chat service with at least two connected microservices.
- A brief write-up explaining your service discovery approach.

## Solution
See the `solution/` directory for a reference implementation.
