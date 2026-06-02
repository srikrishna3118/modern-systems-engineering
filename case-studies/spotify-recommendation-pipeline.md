# Case Study: Spotify Recommendation Pipeline – ML Recommendations for 500M Users

## Overview

Spotify's recommendation system delivers personalized music playlists and songs to 500M+ users daily. The system runs thousands of ML models in real-time, balancing discovery (recommending new music) with satisfaction (recommending known favorites).

## Key Challenges

- **Cold Start**: New users have no history; must recommend without data
- **Discovery vs. Satisfaction**: Balance introducing new music with recommending proven favorites
- **Real-Time Personalization**: Generate playlists in < 500ms for interactive use cases
- **Catalog Size**: Catalog of 100M+ songs; not all songs are relevant for all users

## Architecture Highlights

- **Contextual Bandits**: Multi-armed bandit algorithms balance exploration (new songs) vs. exploitation (favorites)
- **Collaborative Filtering**: Learn implicit preferences from listening history (plays, skips, saves)
- **Model Ensemble**: Combine outputs of dozens of models (collaborative, content-based, contextual)
- **Real-Time Feature Computation**: User/track features computed on-the-fly using a feature service

```
┌──────────────────────────────────────────┐
│      Spotify Recommendation System        │
├──────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐              │
│  │Candidate │  │Ranking   │              │
│  │Generation│  │Models    │              │
│  │(Collab,  │  │(Ensemble)│              │
│  │Content)  │  │          │              │
│  └────┬─────┘  └────┬─────┘              │
│       │             │                    │
│       └──────┬──────┘                    │
│              │                           │
│         Contextual Bandit                │
│      (exploration/exploitation)          │
│              │                           │
│        Final Playlist                    │
└──────────────────────────────────────────┘
```

## Technology Stack

- Python (model training), Spark (batch processing)
- TensorFlow/PyTorch (neural networks), scikit-learn (classical ML)
- Kafka (event stream), feature store (real-time features)

## Lessons Learned

1. **Exploration is essential** — Overfitting to known preferences leads to stagnant music; contextual bandits balance this
2. **Implicit feedback is stronger signal than explicit** — Listening behavior (plays vs. skips) is more predictive than explicit ratings
3. **Context matters** — Same user has different preferences (gym vs. sleep); context-aware models outperform user-only models
4. **Model diversity improves recommendations** — Ensemble of diverse models (collaborative, content, contextual) outperforms any single model
5. **A/B testing is essential for music recommendations** — Subtle changes in diversity/freshness have large impact on user satisfaction

## Further Reading

- [Spotify Engineering for Discovery](https://research.spotify.com/)
- [Personalizing Spotify Home with Contextual Bandits](https://research.spotify.com/)
