# Case Study: YouTube Video Delivery – Billion-User Content Distribution

## Overview

YouTube serves billions of hours of video per month to 2+ billion users, making it the world's largest video sharing platform. Its architecture spans video encoding, storage, recommendation, and edge caching.

## Key Challenges

- **Scale**: 500+ hours of video uploaded per minute; billions of views daily
- **Encoding Cost**: Video encoding consumes massive amounts of compute; efficiency is critical
- **Edge Delivery**: Serve video with minimal latency globally while reducing backbone bandwidth
- **Recommendation at Scale**: Recommend videos to billions of users; balance personalization CPU cost with recommendation quality

## Architecture Highlights

- **Colossus**: Google's distributed file system (successor to GFS) stores video files with 3-way replication
- **GCP-based Encoding**: Videos encoded in multiple formats/codecs on Compute Engine using spot VMs (cost optimization)
- **Bigtable**: Powers feature extraction for recommendation; stores user watch history and features
- **Edge Caching**: Cache popular videos on Google's global CDN; most views served from edge

```
┌─────────────────────────────────────────┐
│   YouTube Architecture Overview          │
├─────────────────────────────────────────┤
│                                          │
│  Upload → Encoding (GCP) → Colossus      │
│                 ↓                        │
│  User Watch → Bigtable → Recommendation  │
│      ↓                                   │
│   CDN/Edge Cache ← Serve                 │
└─────────────────────────────────────────┘
```

## Technology Stack

- Google Cloud Platform (Compute Engine, Cloud Storage)
- Colossus (distributed file system), Bigtable (NoSQL)
- Custom encoding pipeline (VP9, AV1 codecs), memcached (caching)
- TensorFlow (recommendation models)

## Lessons Learned

1. **Spot VMs reduce encoding costs dramatically** — Tolerating interruptions enables 70–80% cost savings on encoding workloads
2. **Edge caching is critical for video delivery** — Even at YouTube's scale, caching popular content at CDN edges is essential
3. **Recommendation is a learned problem** — Simple algorithms (collaborative filtering) give way to neural networks at scale
4. **Separation of concerns** — Upload/encode/serve are distinct systems; failures in one don't affect others

## Further Reading

- [YouTube Scalability Talk](https://www.youtube.com/watch?v=jZkHpNj9KZ8)
- [Google Cloud & YouTube Engineering](https://cloud.google.com/blog/topics/systems-and-infrastructure)
