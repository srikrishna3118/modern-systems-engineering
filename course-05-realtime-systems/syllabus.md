# Course 05 – Real-Time Systems

**Duration:** 3 weeks. **Prerequisite:** Course 02.

## Overview

This course focuses on event-driven architectures, stream processing, and low-latency system design used in modern real-time applications.

## Topics

- Event-driven architecture patterns — [Lecture 1](lectures/lecture-01-events-streams-windows.md)
- Stream processing with Apache Kafka — Lecture 1
- Time-series data and windowing — Lecture 1
- WebSockets and server-sent events — [Lecture 2](lectures/lecture-02-websockets-latency-backpressure.md)
- Low-latency system design — Lecture 2
- Backpressure and flow control — Lecture 2

## Learning Objectives

- Design event-driven systems using messaging and streaming technologies.
- Build low-latency data pipelines with stream processing frameworks.
- Handle backpressure and flow control in high-throughput systems.

## How to complete this course

1. Read Lecture 1. If the Kafka lab from Course 02 is unfinished, do it now.
2. Read Lecture 2 and do the WebSocket lab, including the slow-client experiment.
3. Read the case studies and note which of them use the socket as the source of truth (none of them should).

## Lectures

- [Lecture 1: Events, Streams, and Windows](lectures/lecture-01-events-streams-windows.md)
- [Lecture 2: WebSockets, Latency, and Backpressure](lectures/lecture-02-websockets-latency-backpressure.md)

## Labs

- [WebSocket Streaming](labs/websocket-streaming) — pub/sub, per-client queues, backpressure

## Case studies

Canonical copies live in [`../case-studies/`](../case-studies/). The course-local file is a pointer.

- [Figma real-time collaboration](../case-studies/figma-realtime-collaboration.md)
- [Discord chat infrastructure](../case-studies/discord-chat-infrastructure.md)
- [WhatsApp messaging](../case-studies/whatsapp-messaging-system.md)
