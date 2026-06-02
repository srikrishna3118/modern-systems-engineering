# Capstone Template: Personalized Feed Ranking System

A high-engagement content recommendation engine for billions of users, balancing discovery, satisfaction, and platform goals.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│         Personalized Feed Ranking System                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User App (scrolling feed)                                  │
│       ↓                                                     │
│  ┌──────────────────────────────────────┐                 │
│  │   Feed API                           │                 │
│  │  (GET /feed?user_id=X)               │                 │
│  └────┬───────────────────────────────┘                  │
│       │                                                    │
│  ┌────▼────────────────────────┐                          │
│  │ Candidate Generation         │                          │
│  │ (collaborative filtering,    │                          │
│  │  content-based)              │                          │
│  │ Returns 1000 candidates      │                          │
│  └────┬────────────────────────┘                          │
│       │                                                    │
│  ┌────▼────────────────────────┐                          │
│  │  Ranking Models              │                          │
│  │  (ML ensemble)               │                          │
│  │  - CTR model                 │                          │
│  │  - Engagement model          │                          │
│  │  - Diversity penalty         │                          │
│  │  Outputs: score for each     │                          │
│  └────┬────────────────────────┘                          │
│       │                                                    │
│  ┌────▼────────────────────────┐                          │
│  │  Re-ranking & Filtering      │                          │
│  │  - Apply policy constraints  │                          │
│  │  - Add context freshness     │                          │
│  │  - Apply diversity penalty   │                          │
│  └────┬────────────────────────┘                          │
│       │                                                    │
│  ┌────▼────────────────────────┐                          │
│  │   Return top 10 items        │                          │
│  │   (Personalized order)       │                          │
│  └──────────────────────────────┘                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Architecture Components

### 1. Candidate Generation (Retrieval Phase)
Two approaches, often combined:

**Collaborative Filtering:** "Users like you liked these items"
- Represent user as embedding (learned from interactions)
- Find users with similar embeddings
- Retrieve items those users engaged with
- Fast approximate nearest neighbor search (ANN)

**Content-Based:** "Items similar to your saved items"
- Represent item as embedding (metadata, image, text)
- Find items similar to user's history
- Return diverse set of candidates

**Output:** ~1000 candidates (reduced from millions)

### 2. Ranking Models
Pointwise scoring of candidates (score = probability user will engage).

**Multi-Task Learning Model:**
- Predict: Click-through rate (CTR), watch time, bookmarks, shares
- Loss: Weighted sum of task losses
- Output: Combined score for ranking

**Example Features:**
- User features: age, location, past engagement
- Item features: creator, view count, engagement rate
- Context features: time of day, device, network condition

### 3. Re-ranking / Post-processing
Apply policy constraints and diversity:

**Freshness:** Boost new content slightly (discovery)
**Diversity:** Penalize items from same creator if already shown recently
**Policy:** Don't show unsuitable content (age-gated, banned creators)

### 4. Feedback Loop
- Track user engagement: clicks, watch time, bounce rate
- Train models on real-time labels (user behavior = ground truth)
- A/B test new models before deployment

## Key Features

1. **Personalization**: Each user gets different feed order
2. **Discovery**: Balance user's known preferences with new content
3. **Engagement**: Optimize for watch time / clicks (monetization)
4. **Fairness**: Avoid creator monopolies; small creators get visibility
5. **Freshness**: New content gets exposure; don't always serve stale hits

## Technology Stack

| Component | Technology |
|-----------|-----------|
| API | GO (low-latency, stateless) |
| Candidate Gen | Elasticsearch (collaborative), Redis (nearest neighbor graphs) |
| ML Models | PyTorch / TensorFlow (training), ONNX Runtime (serving) |
| Feature Store | Spark (batch), Feature store (online) |
| Embedding Store | Redis / Milvus (ANN search) |
| Training | Spark, MLflow |
| A/B Testing | Custom (Prophet for analysis) |
| Infrastructure | Kubernetes |

## Design Decisions

### Two-Stage Ranking
- **Why two stages?** Can't rank all 1B items per user (too slow). Candidate generation filters to ~1K, ranking model scores those.
- **Trade-off:** Second stage uses more expensive features; first stage uses approximate methods.

### Multi-Task Learning vs. Single-Task
- **Single-task**: CTR only. Simple, fast. Misses other engagement signals.
- **Multi-task**: CTR + watch time + bookmarks. Richer signal, captures nuance. Slightly slower inference.

### Diversity Penalty
- **Why?** Without penalty, model ranks same creator repeatedly (high engagement).
- **Penalty:** Reduce score if last 5 items are from same creator.
- **Trade-off:** Slightly lower short-term engagement, better long-term user satisfaction.

## Scaling Challenges

**Challenge: Candidate Generation Latency**
- Collaborative filtering requires finding similar users: ~100ms

*Solution:*
- Pre-compute user embeddings batch (offline)
- Cache user embeddings in Redis
- Use approximate nearest neighbor search (locality-sensitive hashing)

**Challenge: Feature Computation**
- Computing 100+ features for ranking is expensive

*Solution:*
- Feature store pre-computes and caches common features
- Only compute expensive features for top candidates
- Online feature fetch from Redis (< 10ms)

**Challenge: Model Inference Latency**
- Neural network inference: ~50ms

*Solution:*
- Quantize model (FP32 → INT8; 4x faster)
- Compile model to ONNX Runtime (optimized inference)
- Use model distillation (smaller model trained on large model's outputs)

## Deliverables

1. **System Architecture** (candidate generation → ranking → re-ranking)
2. **Data Model** (users, items, engagements table schema)
3. **ML Pipeline** (feature engineering, training, evaluation)
4. **Ranking Model Spec** (input features, output score)
5. **A/B Testing Framework** (how to safely test new models)
6. **Diversity Strategy** (how to balance discovery vs. satisfaction)
7. **Prototype** (serve personalized feed to 100+ users)

## Implementation Milestones

- Week 1: Set up Elasticsearch, collaborative filtering baseline
- Week 2: Feature store, compute user/item embeddings
- Week 3: Simple ranking model (logistic regression)
- Week 4: Neural ranking model (multi-task learning)
- Week 5: Re-ranking, diversity, freshness
- Week 6: A/B testing infrastructure
- Week 7–8: Load testing, optimization, monitoring

## Metrics to Track

| Metric | Why It Matters |
|--------|---|
| Click-Through Rate (CTR) | User engagement |
| Watch Time | Content consumption |
| Bounce Rate | Session quality |
| Creator Diversity | Fairness, platform health |
| Cold Start Performance | New user experience |
| Model Latency (p50, p99) | User experience |

## Further Reading

- [Twitter: Ranked Feed at Scale](https://blog.twitter.com/)
- [Pinterest: Graph Learning for Recs](https://medium.com/pinterest-engineering)
- [Netflix: Bandit Algorithms for Exploration](https://research.netflix.com/)
