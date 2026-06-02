# Case Study: Kubernetes – Container Orchestration at Scale

## Overview

Kubernetes (k8s) is the de facto standard for container orchestration, managing millions of containers across thousands of organizations. Originally developed at Google based on lessons from Borg and Omega, Kubernetes automates deployment, scaling, and operations of containerized applications. This case study examines its architecture and the engineering decisions that enable it to scale.

## Key Challenges

- **Declarative State Management**: Reconciling desired state with actual state across thousands of nodes
- **Scheduling**: Bin-packing containers efficiently across heterogeneous hardware
- **Networking**: Providing every pod a unique IP and enabling service discovery without NAT
- **Extensibility**: Supporting diverse workloads (stateless, stateful, batch, ML) without a monolithic design
- **Fault Tolerance**: Maintaining cluster operation during node failures, network partitions, and control plane outages

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Control Plane                          │
│                                                          │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  API      │  │  etcd         │  │  Scheduler        │  │
│  │  Server   │◄─┤  (Raft        │  │  (bin-packing,    │  │
│  │  (REST)   │  │   consensus)  │  │   affinity,       │  │
│  └─────┬─────┘  └──────────────┘  │   constraints)     │  │
│        │                          └───────────────────┘  │
│  ┌─────▼──────────────────────────────────────────────┐  │
│  │  Controller Manager                                 │  │
│  │  (Deployment, ReplicaSet, StatefulSet, Job, etc.)   │  │
│  │  ── Reconciliation Loops ──                         │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────┘
                         │ Watch / API calls
         ┌───────────────▼──────────────────┐
         │           Worker Nodes            │
         │                                   │
         │  ┌──────────┐  ┌──────────────┐  │
         │  │  kubelet  │  │  kube-proxy  │  │
         │  │  (node    │  │  (iptables / │  │
         │  │   agent)  │  │   IPVS rules)│  │
         │  └─────┬─────┘  └──────────────┘  │
         │        │                          │
         │  ┌─────▼──────────────────────┐   │
         │  │  Container Runtime          │   │
         │  │  (containerd / CRI-O)       │   │
         │  │                             │   │
         │  │  ┌─Pod──────┐ ┌─Pod──────┐ │   │
         │  │  │Container │ │Container │ │   │
         │  │  │Container │ │          │ │   │
         │  │  └──────────┘ └──────────┘ │   │
         │  └────────────────────────────┘   │
         └───────────────────────────────────┘
```

### Key Design Patterns

1. **Declarative Configuration + Reconciliation Loops**: Users declare desired state (e.g., "3 replicas of web server"). Controllers continuously compare actual state to desired state and take corrective action. This pattern is robust to transient failures — the system self-heals by re-reconciling.

2. **Watch-Based Architecture**: Components use long-lived HTTP/2 watch streams against the API server to receive real-time state change notifications. This avoids polling and enables reactive, event-driven behavior.

3. **etcd as Single Source of Truth**: All cluster state is stored in etcd (a distributed key-value store using Raft consensus). The API server is the only component that communicates with etcd directly, providing a consistent access layer.

4. **Level-Triggered vs. Edge-Triggered**: Kubernetes controllers are level-triggered — they react to the current state, not to events. If a controller misses an event, it will still correct the state on the next reconciliation pass. This makes the system more reliable than edge-triggered approaches.

## Scaling Considerations

| Dimension | Kubernetes Limit (tested) |
|-----------|--------------------------|
| Nodes | 5,000 per cluster |
| Pods | 150,000 per cluster |
| Pods per node | 110 (default) |
| Services | 10,000 per cluster |
| API server latency | < 1s for single-object, < 30s for list |

### Scaling Bottlenecks
- **etcd**: At scale, etcd becomes the bottleneck. Mitigations: compaction, defragmentation, separating events from core state into a separate etcd cluster.
- **API Server**: List operations are expensive. Mitigations: API priority and fairness, watch bookmarks, pagination.
- **Scheduler**: At 5,000 nodes, the scheduler processes ~100 pods/sec. Mitigations: scheduling profiles, preemption, gang scheduling.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Go |
| State Store | etcd (Raft consensus) |
| Networking | CNI plugins (Calico, Cilium, Flannel) |
| Service Mesh | Istio, Linkerd (optional) |
| Container Runtime | containerd, CRI-O |
| API | REST + protobuf, OpenAPI schema |

## Lessons Learned

1. **Declarative > Imperative at scale** — Reconciliation loops make the system self-healing. Rather than scripting "do A then B then C", you declare the end state and controllers converge toward it.

2. **The API server is the chokepoint by design** — Funneling all state access through a single API (with RBAC, admission control, and audit logging) provides a single enforcement point for policy and security.

3. **Level-triggered design prevents lost-event bugs** — By reacting to current state rather than individual events, controllers handle missed events, restarts, and partial failures gracefully.

4. **Extensibility requires stable APIs** — CRDs (Custom Resource Definitions) and the Operator pattern allow anyone to extend Kubernetes without modifying core code. This extensibility drove ecosystem adoption.

5. **etcd is the Achilles' heel** — Cluster health depends critically on etcd performance. Dedicated SSDs, careful compaction schedules, and separate etcd clusters for events are essential at scale.

## Further Reading

- [Kubernetes Design and Architecture](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture/architecture.md)
- [Large-Scale Cluster Management at Google with Borg (EuroSys 2015)](https://research.google/pubs/pub43438/)
- [Scaling Kubernetes to 7,500 Nodes](https://openai.com/research/scaling-kubernetes-to-7500-nodes)
