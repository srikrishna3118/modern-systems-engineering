# Case Study: Figma Real-Time Collaboration

## Overview
Figma allows thousands of designers to collaborate on the same design file simultaneously, with changes appearing in near real time for all participants. This case study examines how Figma engineered its collaborative editing system and the distributed systems challenges it solved.

## Key Challenges
- **Operational Transformation / CRDT**: Ensuring that concurrent edits from multiple users converge to a consistent state.
- **Latency**: Propagating changes to all connected clients within milliseconds.
- **Scale**: Supporting files with hundreds of simultaneous editors.
- **Persistence**: Persisting a continuous stream of incremental changes without losing data.

## Architecture Highlights

### Multiplayer Server
Figma's multiplayer server acts as the central hub for a design session. All clients connect to the server via WebSockets. The server receives operations from each client, applies them to a shared in-memory document state, and fans out the changes to all other connected clients.

### Conflict Resolution with Operational Transformation
Rather than using CRDTs (which Figma evaluated but found overly complex for their use case), Figma uses a form of Operational Transformation (OT). Each operation is tagged with a version vector. The server serializes concurrent operations and transforms them against each other to ensure convergence.

### State Synchronization
When a new user joins a session, the server sends the full current document snapshot, after which the client receives only incremental deltas. Figma stores these deltas in a persistent log so that the document can be reconstructed at any point in time.

### LiveGraph
Figma's rendering engine (LiveGraph) is a reactive dependency graph that efficiently re-renders only the parts of the canvas affected by an incoming operation, keeping the UI responsive even under heavy collaborative load.

## Technology Stack
- **Client**: TypeScript + WebAssembly (custom rendering engine)
- **Multiplayer Server**: C++ (for performance-critical session management)
- **Transport**: WebSockets over TLS
- **Persistence**: PostgreSQL for document metadata; custom binary delta log for operation history
- **Infrastructure**: AWS, with regional session affinity

## Lessons Learned
1. Choosing a simpler consistency model (OT over CRDT) reduced implementation complexity while meeting product requirements.
2. WebSockets provide the low-latency, full-duplex channel needed for real-time collaboration; HTTP polling is unsuitable at scale.
3. Separating the multiplayer session server (in C++) from the stateless API backend allows independent scaling.
4. LiveGraph's reactive rendering model is critical — naive full re-renders would make large files unusable.

## Further Reading
- [Figma Engineering Blog – How Figma's Multiplayer Technology Works](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)
- [Figma Engineering Blog – LiveGraph: Real-time Data Fetching at Figma](https://www.figma.com/blog/livegraph-real-time-data-fetching-at-figma/)
