# Lab: Kafka Pipeline – Event Streaming Architecture

## Overview
Build an end-to-end event streaming pipeline using Apache Kafka. This lab covers producer/consumer patterns, topic partitioning, and stream processing with real-time data.

## Architecture

```
Data Source --> Kafka Producer --> Kafka Topic --> Stream Processor --> Consumer / Dashboard
```

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
   cd starter-code
   docker compose up -d zookeeper kafka kafka-ui
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Review the producer and consumer stubs and implement `TODO`s.
4. Run the producer to publish events:
   ```bash
   python producer.py
   ```
5. Run the consumer to process events:
   ```bash
   python consumer.py
   ```

## Validation

- Confirm events are visible in Kafka UI at `http://localhost:8080`.
- Confirm the consumer prints a summary every ~100 events.

## Experiment

1. Change the partition key (user_id vs product_id) and observe ordering differences.
2. Run two consumers in the same group and confirm work is split by partition.

## Deliverables
- A working Kafka pipeline that ingests, processes, and outputs events.
- A short document describing your partition strategy and consumer group design.

## Solution
See the `solution/` directory for a reference implementation.
