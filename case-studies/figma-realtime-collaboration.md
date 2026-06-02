# Case Study: Figma Real-Time Collaboration – Operational Transformation at Scale

## Overview

Figma enables thousands of designers to collaborate on the same file simultaneously with near-real-time updates. The system must handle concurrent editing, conflict resolution, and fast rendering of large design files.

## Key Challenges

- **Consistency**: Ensure all users see the same document state despite concurrent edits
- **Latency**: Changes must appear instantly (<100ms) for interactive feel
- **Scalability**: Support hundreds of concurrent editors on a single file
- **Persistence**: Save state frequently; recover from failures without data loss

## Architecture Highlights

- **Multiplayer Server**: WebSocket hub that maintains in-memory document state and streams updates to clients
- **Operational Transformation (OT)**: Client sends operations (insert character, move shape) relative to its local state; server transforms operations for consistency
- **State Synchronization**: Clients receive snapshot on connect, then incremental delta operations
- **LiveGraph**: Reactive rendering engine that recomputes only changed parts; enables smooth rendering of large files
- **Persistent Log**: Append-only log of operations; enables undo/redo and recovery

## Technology Stack

- TypeScript + WebAssembly (client), C++ (multiplayer server)
- WebSockets (real-time communication), PostgreSQL (persistence)
- In-memory document model with copy-on-write for snapshots

## Lessons Learned

1. **Operational Transformation is simpler than CRDT** — OT's transformation logic is complex but easier to implement correctly than CRDT's merge algorithm
2. **Centralized server simplifies consistency** — Client-side CRDTs avoid a server, but centralized OT server guarantees consistency more simply
3. **WebSockets are essential** — HTTP polling adds unacceptable latency; persistent WebSocket connections are necessary for real-time feel
4. **Reactive rendering is critical** — Large design files have thousands of objects; recomputing entire scene on each frame is too slow
5. **Separating multiplayer server from API** — Stateful multiplayer service (C++) is separate from stateless API (node/Python); enables independent scaling

## Further Reading

- [Figma Blog: Multiplayer Technology](https://figma.com/blog/)
- [How Figma's Multiplayer Technology Works](https://figma.com/blog/how-figmas-multiplayer-technology-works/)
