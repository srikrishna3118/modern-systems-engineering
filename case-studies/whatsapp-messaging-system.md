# Case Study: WhatsApp Messaging System – Reliable Messaging for 100+ Million Concurrent Users

## Overview

WhatsApp delivers billions of messages per day to 2+ billion users with an architecture designed for reliability and minimal infrastructure. The platform achieves remarkable efficiency: 50 engineers support 100M concurrent users — a testament to its architecture.

## Key Challenges

- **Reliability**: Messages must be delivered reliably; offline users must receive messages upon reconnection
- **Efficiency**: Serve 100M concurrent users with minimal server resources (50 engineers)
- **Scalability**: Handle billions of messages/day without proportionally growing infrastructure
- **Battery Life**: Minimize battery drain on mobile devices through efficient protocols

## Architecture Highlights

- **Erlang**: Messaging and notification servers written in Erlang/OTP for concurrency and fault tolerance
- **Mnesia**: Embedded replicated database (Erlang) for message queuing and delivery receipts
- **Push Notifications**: GCM/APNS for offline messages; avoids persistent connections for offline users
- **Vertical Scaling**: Minimize number of nodes; heavily optimize performance per-node rather than scaling horizontally

```
┌──────────────────────────────────────┐
│    WhatsApp Server (Erlang)          │
├──────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────────┐  │
│  │ Mnesia   │  │ Message Queue    │  │
│  │ (Embedded│  │ (for offline     │  │
│  │ DB)      │  │  users)          │  │
│  └──────────┘  └──────────────────┘  │
│       ↓               ↓                │
│  [Online Users] [Offline → Push]      │
└──────────────────────────────────────┘
```

## Technology Stack

- Erlang/OTP (server), Mnesia (database), custom binary protocol
- GCM/APNS (push notifications), minimal external dependencies

## Lessons Learned

1. **Vertical scaling beats horizontal ** — Highly optimized Erlang code scales to 100M concurrent users on fewer nodes than less efficient horizontal architectures
2. **Embedded replicated databases work at scale** — Mnesia replication across 2–3 nodes eliminates external dependencies
3. **Minimize moving parts** — Fewer external services (no separate message queue, cache, etc.) means fewer failure modes
4. **Protocol design matters** — Custom binary protocol is far more efficient than JSON for bandwidth-constrained mobile
5. **Push notifications solve the offline problem** — Avoiding persistent reconnections for offline users saves massive bandwidth

## Further Reading

- [WhatsApp Engineering](https://www.whatsapp.com/research/)
- [Scaling to 100 Million Concurrent Connections (WhatsApp Engineering)](https://www.erlang.org/doc/design_principles)
