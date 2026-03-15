# Lab: Kafka Pipeline – Event Streaming Architecture

## Overview
Build an end-to-end event streaming pipeline using Apache Kafka. This lab covers producer/consumer patterns, topic partitioning, and stream processing with real-time data.

## Architecture

```
Data Source --> Kafka Producer --> Kafka Topic --> Stream Processor --> Consumer / Dashboard
```

See `architecture.png` for a detailed component diagram.

## Learning Objectives
- Produce and consume messages using the Kafka client API.
- Design topics with appropriate partition and replication settings.
- Implement a stream processing job with Kafka Streams or Faust.

## Prerequisites
- Python or Java/Kotlin.
- Docker and Docker Compose installed locally.
- Basic understanding of pub/sub messaging.

## Getting Started

1. Start the Kafka cluster:
   ```bash
   docker-compose up -d zookeeper kafka
   ```
2. Copy the `starter-code/` directory and review the producer and consumer stubs.
3. Implement the missing logic (marked with `TODO`) in both the producer and consumer.
4. Run the producer to publish events:
   ```bash
   python producer.py
   ```
5. Run the consumer to process events:
   ```bash
   python consumer.py
   ```

## Deliverables
- A working Kafka pipeline that ingests, processes, and outputs events.
- A short document describing your partition strategy and consumer group design.

## Solution
See the `solution/` directory for a reference implementation.
