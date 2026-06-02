# Capstone Template: Global Chat Platform

A scalable, real-time messaging platform supporting millions of concurrent users across the globe.

## System Overview

```
┌──────────────────────────────────────────────────────────────┐
│              Global Chat Platform                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Web Client (WebSocket)                 Mobile App           │
│       ↓                                      ↓              │
│  ┌────────────────────────────────────────────────┐         │
│  │        Edge Gateway (Cloudflare/CDN)           │         │
│  │   (route to nearest region, load balance)      │         │
│  └────────────┬─────────────────────────┬────────┘         │
│               │                         │                  │
│  ┌────────────▼──┐            ┌────────▼── ────┐          │
│  │US-EAST Region │            │EU-WEST Region  │          │
│  │               │            │                │          │
│  │ ┌──────────┐  │            │ ┌──────────┐   │          │
│  │ │Msg Svc   │  │            │ │Msg Svc   │   │          │
│  │ │+Cache    │  │            │ │+Cache    │   │          │
│  │ └────┬─────┘  │            │ └────┬─────┘   │          │
│  │      │        │            │      │         │          │
│  │ ┌────▼─────┐  │            │ ┌────▼─────┐   │          │
│  │ │ScyllaDB  │  │            │ │ScyllaDB  │   │          │
│  │ │cluster   │  │            │ │cluster   │   │          │
│  │ └──────────┘  │            │ └──────────┘   │          │
│  └────┬──────────┘            └────┬───────────┘          │
│       │                            │                      │
│       └────────────────┬───────────┘                      │
│                        │                                 │
│                 (Kafka event stream)                     │
│                        │                                 │
│       ┌────────────────▼──────────────┐                 │
│       │  Analytics & Notification     │                 │
│       │  (message indexing, etc)      │                 │
│       └───────────────────────────────┘                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Architecture Components

### 1. Message Service
- Handles incoming messages, stores in scoped storage (per room/dm)
- WebSocket connection per user
- Loads recent messages on room join

### 2. Multi-Region Deployment
- Each region has independent message cluster (for low latency)
- Cross-region replication using Kafka (eventual consistency)
- Users always route to nearest region

### 3. Message Storage
- Time-bucketed tables (messages_2025_03_15) to prevent unbounded partition growth
- Partition key: (room_id, bucket), sort key: message_id (timestamp-ordered)
- Read replicas for historical message queries

### 4. Real-Time Synchronization
- WebSocket streams for connected users (instant delivery)
- Kafka topic for offline message delivery (users get backlog on reconnect)

### 5. Presence & Typing Indicators
- Redis with short TTL (30s) for user presence per room
- Broadcast presence changes to room subscribers
- Typing indicators via ephemeral Kafka messages

## Key Features

1. **Real-Time Messaging**: Sub-100ms message delivery for connected users
2. **Message History**: Full history searchable and retrievable
3. **Multi-Region**: Global users with local-region latency
4. **Offline Support**: Messages persisted; delivered on reconnect
5. **Notifications**: Push to mobile when offline
6. **Rich Features**: Threads, reactions, file sharing, @ mentions

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React Native (mobile), React (web) |
| Backend | Go (message service), Python (analytics) |
| Message Storage | ScyllaDB (NoSQL) |
| Real-Time | WebSockets, Kafka (event streaming) |
| Cache | Redis (presence, session) |
| Search | Elasticsearch (message search) |
| CDN | Cloudflare (edge routing) |
| Infrastructure | Kubernetes (multi-region) |

## Scaling Challenges & Solutions

**Challenge: Hot Rooms**
- Popular channels receive 10K+ messages/sec
- Single partition becomes bottleneck

*Solution:*
- Shard room by message ID (hash-based)
- Load balance reads/writes across multiple partitions

**Challenge: Presence at Scale**
- 100M users; tracking all online users in Redis is expensive

*Solution:*
- Track presence only for current user's contacts/friends (filtered set)
- Use eventual consistency (a few seconds stale OK)

**Challenge: Message Ordering**
- Ensure users see messages in chronological order despite multi-region deployments

*Solution:*
- Use Kafka for global ordering (all messages go through Kafka before storage)
- Assign monotonically increasing message IDs centrally

**Challenge: Cross-Region Consistency**
- User in US sends message, EU user should see it < 1 second

*Solution:*
- US region processes message, writes to local database
- Publishes event to Kafka
- EU region consumes, stores locally
- Acceptable latency: ~500ms

## Deliverables

1. **System Architecture** (diagram with regions, components, data flow)
2. **API Design** (send message, load history, upload file)
3. **Data Model** (messages table schema, presence storage)
4. **Consistency Strategy** (ordering, replication, failover)
5. **Scaling Analysis** (hot shards, presence, cross-region sync)
6. **Prototype** (1-1 chat, room messages, 100+ concurrent users)

## Implementation Milestones

- Week 1: WebSocket server, basic message storage
- Week 2: Message history, pagination
- Week 3: Presence and typing indicators
- Week 4: Multi-region sync (Kafka)
- Week 5: Search and analytics
- Week 6–8: Optimization, load testing, monitoring

## Further Reading

- [Discord: How We Store Trillions of Messages](https://discord.com/blog/how-discord-stores-trillions-of-messages)
- [WhatsApp: 1 Million Concurrent Users](https://www.erlang.org/doc/design_principles)
