# Lecture 2: WebSockets, Low Latency, and Backpressure

## Overview

Some clients are waiting on a socket, not polling a database. This lecture covers how to push updates to them, where latency actually goes, and what to do when a client or a downstream system cannot keep up. The [WebSocket lab](../labs/websocket-streaming) is the small version of the push path.

## Topics

### 1. WebSockets and server-sent events

HTTP is a request and a response. Two patterns keep a channel open:

- **Server-sent events** are a one-way stream over ordinary HTTP: the server writes, the client reads, and the browser reconnects with the last id it saw. Use them for notifications and feeds, where the client does not need to send much. They work through proxies that already understand HTTP.
- **WebSockets** are two-way. The client subscribes, sends messages, and receives a stream. Use them for chat, presence, collaborative editing, and live prices. They are a long-lived connection that a load balancer must be willing to hold, and they do not traverse every corporate proxy cleanly. Plan a fallback (SSE or long polling) if the user base includes those networks.

The connection is not the source of truth. A client that reconnects must be able to catch up from a stored log or a snapshot, because you will drop connections constantly (phones, deploys, load balancer idle timeouts). [Figma](../../case-studies/figma-realtime-collaboration.md) and [Discord](../../case-studies/discord-chat-infrastructure.md) both treat the socket as a delivery optimization on top of a stored document or message log. The [chat lab](../../course-02-distributed-systems/labs/chat-system) stores messages for the same reason.

```
 client ──subscribe──▶ gateway ──▶ connection table (this user, this node)
                         │
                         ▲
        log / pubsub ────┘  publish to the node that holds the socket
```

A publish has to find the node holding that user's socket. A connection table (user → node), or a pub/sub topic per user that every gateway consumes and ignores if the user is not local, both work. The table is less wasted bandwidth. The topic is less state. Pick based on fan-out.

### 2. Fan-out

- **One user, a few devices.** Write to each of the user's open sockets. Easy.
- **A room of hundreds.** One publish becomes hundreds of writes. Do it on the gateway that already has those sockets, not by looping across a data center.
- **A room of millions** (a livestream chat). Do not fan out per message per socket from one process. Shard the room, or have clients pull a short-lived segment, or accept that not every viewer gets every message instantly. [YouTube-scale delivery](../../case-studies/youtube-video-delivery.md) does not push video bytes down a WebSocket at all. The socket, if there is one, carries control. The bytes come from a CDN.

Presence ("who is online") is a lease, not a flag. The client refreshes it. If the refresh stops, the user is offline, even if you never received a close frame. Close frames get lost.

### 3. Low-latency design

Latency budgets are a sum. Write the sum down.

- **Queueing** dominates once a machine is busy. A process at 80% CPU has a worse tail than the same process at 40%, often by more than the difference in average. Headroom is a latency feature.
- **Cross-region round trips** are tens or hundreds of milliseconds and you cannot code your way out of them. Put the gateway near the user. Put the authoritative write where the data lives, and do not make the keystroke wait for a far replica unless the product is consistency.
- **Payloads.** Send the delta, not the document, once the client has a snapshot. [Figma](../../case-studies/figma-realtime-collaboration.md) sends operations. A full-state push on every change will not survive a large document.
- **Tail latency** is what users call "jank." Measure p99 of the push path (accept event → bytes on the socket), not the average. A lock, a synchronous disk write, or a log line that sometimes blocks will own that p99.
- **Deployment.** Restarting a gateway drops every socket on it. Drain: stop accepting new connections, wait for clients to migrate, then exit. Clients must reconnect anyway; do not make a deploy reconnect all of them in the same second.

### 4. Backpressure and flow control

Backpressure is what a system does when the consumer is slower than the producer. Without it, buffers grow until a process is killed, and the kill takes the fast consumers with the slow one.

Options, in the order you should prefer them:

1. **Bound the buffer.** A per-client queue with a maximum length. When it is full, drop the oldest update for that client, or disconnect that client. Do not block the producer. The lab implements this: a slow subscriber loses updates and everyone else keeps receiving.
2. **Slow the producer** when the *downstream system* is the bottleneck and every message matters (a database writer, a billing consumer). This is flow control. The producer blocks or defers, and the lag is visible as queue age. It is the right choice when dropping is worse than delaying. It is the wrong choice on a fan-out socket, because one slow client would stall the room.
3. **Shed load.** If the whole system is behind, drop the cheapest work first (presence updates, typing indicators) and keep the work users will notice missing (the message itself). Say the order in advance.
4. **Scale the consumer** by partition, from [Lecture 1](lecture-01-events-streams-windows.md). Scaling does not help a single hot key. A hot key needs its own partition or a smaller payload.

A signal you can alert on: queue depth, or age of the oldest item, per stage. CPU will look fine while you are minutes behind.

### 5. Collaboration, briefly

Operational transformation and CRDTs let two editors change a document without a lock. The hard part is not the socket. It is the meaning of "merge" for your data. If the product can tolerate last-write-wins on a whole field, do that and move on. If two people can edit the same sentence, you need a real merge function and a server that orders operations. Read the Figma case for what that server is responsible for, and do not invent a consensus protocol for a cursor position.

## Key Takeaways

1. **The socket is a delivery path.** The log or the document is the source of truth, because clients reconnect.
2. **SSE for one-way feeds, WebSockets for two-way sessions,** with a catch-up on reconnect.
3. **Fan-out from the machine that already holds the sockets.** A viral room is a sharding problem, not a loop.
4. **Latency is queueing, distance, and payload size.** Measure the p99 of the push, and drain connections on deploy.
5. **Bound per-client buffers and drop or disconnect the slow client.** Reserve "slow the producer" for work you cannot lose.

## Further Reading

- [WebSocket lab](../labs/websocket-streaming)
- [Figma real-time collaboration](../../case-studies/figma-realtime-collaboration.md)
- [Discord chat infrastructure](../../case-studies/discord-chat-infrastructure.md)
- [WhatsApp](../../case-studies/whatsapp-messaging-system.md) — connection count as the scaling dimension.
