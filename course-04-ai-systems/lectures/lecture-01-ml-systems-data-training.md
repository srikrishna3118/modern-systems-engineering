# Lecture 1: ML System Design, Data, and Training

## Overview

A model in a notebook is not a system. The system is the path from raw events to a feature value the trainer and the server agree on, plus a way to retrain when the world moves. This lecture covers that path: the shape of an ML system, the feature pipeline, and training as a batch job with a promotion decision at the end.

## Topics

### 1. ML system design

Separate the three loops. They fail differently and they scale differently.

- **The product path.** A request comes in, the service computes or fetches features, a model returns a score, the product does something with it (rank, block, recommend). Latency is on this path.
- **The training path.** Historical features and labels are joined, a job produces a new model artifact, something decides whether it is better than the current one.
- **The data path.** Events are logged, including the features the model actually saw and the outcome (a click, a chargeback, a cancel). If you do not log the features at decision time, you cannot reproduce the training row later.

```
 events ──▶ feature log ──▶ offline store ──▶ training job ──▶ model registry
                │                                      │
                └──▶ online store ──▶ serving  ◀───────┘
```

Most production pain is the two stores disagreeing. The feature computed in the nightly Spark job is not the feature computed in the request handler, and the model silently gets worse. [Shopify's ML platform](../../case-studies/shopify-ml-platform.md) treats "compute once, materialize to both stores" as the fix. Copy that unless you have a measured reason not to.

### 2. Ingestion and feature pipelines

An event log (the [Kafka lab](../../course-02-distributed-systems/labs/kafka-pipeline) is the small version) is the ingestion point. From there:

- **Offline features** are aggregations a training job can scan: counts over 7 days, the last 10 items, a ratio. They are built in batch, partitioned by time, and reproducible. Rebuilding yesterday's partition should give the same answer.
- **Online features** are the subset the request path needs, looked up by entity id (user, item, card) in a low-latency store. They are a materialization of the offline definition, not a second implementation.
- **Point-in-time correctness.** A training row for an event at time T may only use feature values that were knowable at T. Joining "the user's current state" into last year's clicks leaks the future into the model. This is the bug that makes offline metrics look wonderful and production look random.

Labels have their own delay. A fraud label may arrive weeks later. Training on "what we knew the next day" and serving "what we know now" is fine only if you are honest about it. Do not drop late labels; they are often the ones that matter.

### 3. Training at scale

Training is a batch job with expensive hardware, not a request.

- **Data-parallel training** splits a step's examples across devices and averages gradients. The [NVIDIA cluster case](../../case-studies/nvidia-ai-cluster-architecture.md) is what this costs when the model does not fit on one machine: the network between GPUs becomes the bottleneck, not the arithmetic.
- **Single-machine training is the default** for tabular models (gradient-boosted trees, linear models) that decide a large fraction of real product systems. Do not reach for a GPU cluster because the word "ML" appeared.
- **The artifact is versioned.** A registry stores the model, the data range it trained on, the feature definitions, and the metric that justified promotion. If you cannot point at those four, you cannot roll back.
- **Promotion is a decision.** A new model is not deployed because training finished. It is deployed because it beat the current model on a held-out set that was not used to tune it, and preferably because a slice of production traffic (a shadow or a small percentage) agreed.

Retrain on a schedule that matches how fast the world moves. Fraud features go stale in hours. A catalog embedding may be fine for a week. "Train once" is how a model rots.

### 4. What this course's lab is doing

The [RAG lab](../labs/rag-ai-assistant) skips training. It retrieves text and conditions an answer on that text. That is a deliberate, smaller system: the "model" is fixed, and the thing you operate is the index. The same discipline applies. The index is derived, it has a freshness lag, and a bad chunking choice is a data bug, not a prompt bug. Lecture 2 covers serving either kind of system.

## Key Takeaways

1. **Log the features the model saw,** at decision time, or you cannot train on what you served.
2. **One feature definition, two materializations** (offline for training, online for serving). Two definitions is training-serving skew.
3. **Point-in-time joins** keep the future out of the training row.
4. **Most models do not need a GPU cluster.** The registry, the metric, and the rollback do not depend on the hardware.
5. **Promote on evidence,** not because the job went green.

## Further Reading

- [Shopify ML platform](../../case-studies/shopify-ml-platform.md)
- [NVIDIA AI cluster architecture](../../case-studies/nvidia-ai-cluster-architecture.md)
- [Spotify's recommendation pipeline](../../case-studies/spotify-recommendation-pipeline.md) — retraining, bandits, and cold start.
- [Lecture 2](lecture-02-serving-mlops-monitoring.md)
