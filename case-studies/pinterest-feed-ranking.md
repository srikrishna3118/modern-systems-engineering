# Case Study: Pinterest Feed Ranking – Personalized Content at 400M Users

## Overview

Pinterest's home feed is a personalized infinite scroll of content prioritized by ML models. The system ranks billions of items for hundreds of millions of users, balancing freshness, relevance, diversity, and engagement.

## Key Challenges

- **Ranking Latency**: Fetch and rank 1000s of candidate pins in < 100ms
- **Personalization**: Learn implicit user preferences from limited interactions (pins, saves)
- **Diversity**: Avoid monotonous feeds; recommend varied content (different creators, topics)
- **Freshness**: New pins should be visible quickly; don't over-optimize for historical data

## Architecture Highlights

- **Two-Stage Ranking**:
  - **Retrieval (Candidate Generation)**: Fast approximate nearest neighbor search using embeddings
  - **Ranking**: Pointwise ranking model (XGBoost) to score and sort candidates
- **Graph Learning**: Represent users/pins/topics as a graph; use GNNs to learn embeddings
- **Feature Store**: Real-time feature computation for user preferences, pin properties, contextual information
- **Online Embeddings**: Continuously updated embeddings for users and pins; capture latest trends

## Technology Stack

- Python (ML models), Spark (batch processing), Kafka (real-time events)
- Elasticsearch (approximate NN search), Redis (caching)
- TensorFlow/PyTorch (embeddings, GNNs), custom ML infrastructure

## Lessons Learned

1. **Two-stage ranking is essential** — Pointwise ranking of all candidates is too slow; two-stage (candidate generation + ranking) is necessary
2. **Graph structure is signal** — User-pin-topic graphs provide richer signal than user-item matrices alone
3. **Embedding updates matter** — Static embeddings become stale; continuously refreshing embeddings captures new pins and trends
4. **Diversity is a learned objective** — Simple diversity heuristics (don't show 2 pins from same creator) are inferior to learning diversity preferences
5. **A/B testing is critical for feed ranking** — Small changes in ranking logic significantly impact engagement; rigorous testing is essential

## Further Reading

- [Pinterest Economy of Feed Ranking](https://medium.com/pinterest-engineering)
- [Graph Convolutional Networks for Learning with Few Labeled Nodes](https://medium.com/pinterest-engineering)
