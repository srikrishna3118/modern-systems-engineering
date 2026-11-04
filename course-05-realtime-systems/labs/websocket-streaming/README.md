# Lab: WebSocket Streaming – Real-Time Data Pipeline

Build a real-time data streaming pipeline using WebSockets. Covers event-driven architecture, backpressure handling, and low-latency data delivery.

**Architecture:** Data Source → Event Producer → WebSocket Server → Subscribers

**Learning Objectives:**
- Implement WebSocket server for real-time bidirectional communication
- Handle concurrent client connections efficiently
- Implement backpressure and flow control
- Build producer-consumer patterns for real-time data

**Prerequisites:** Python 3.10+, asyncio knowledge, WebSocket basics

## Getting Started

1. Move into the starter implementation:
	```bash
	cd starter-code
	pip install -r requirements.txt
	```
2. Implement TODO sections in `server.py` (subscription management, broadcast).
3. Run the server:
	```bash
	python server.py
	```
4. Open `client.html` in a browser and subscribe to a stream.

## Validation

- Open two browser tabs and confirm both receive updates.
- Simulate a slow client (throttle tab) and confirm it doesn’t block other clients.

## Experiment

1. Add per-topic buffering limits and drop policy for slow clients.
2. Add server-side metrics (messages/sec) and observe behavior under load.

**Deliverables:**
- Working WebSocket server with pub/sub pattern
- Backpressure handling (slow clients don't block fast producers)
- Write-up on latency vs. throughput trade-offs

## Solution

```bash
cd solution
pip install -r requirements.txt
python smoke_client.py          # two subscribers, plus a slow-client drop check
python server.py                # ws://localhost:8765
# then open client.html
```

`docker compose up` in `solution/` runs the same server with `BIND_HOST=0.0.0.0`.

Each client has a bounded outbound queue. A full queue drops that client's update and leaves every other subscriber moving. The queue length is the backpressure limit (`max_backlog`).
