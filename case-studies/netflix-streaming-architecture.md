# Case Study: Netflix Streaming Architecture – Global Video Delivery at Scale

## Overview

Netflix delivers billions of hours of video per month to 250+ million subscribers across the globe. Its streaming architecture spans content delivery, adaptive bitrate encoding, personalization, and global infrastructure orchestration.

## Key Challenges

- **Global Distribution**: Deliver video with < 5s startup latency from 190+ countries
- **Bandwidth Costs**: Video is the most bandwidth-intensive application; transmission efficiency is paramount
- **Device Fragmentation**: Support 2000+ device types with varying bandwidth and computational capabilities
- **Personalization at Scale**: Recommend content to millions of users simultaneously while maintaining freshness

## Architecture Highlights

- **Open Connect CDN**: Netflix-built CDN with appliances placed directly inside ISP networks, eliminating backbone traffic
- **Adaptive Bitrate Encoding**: Encodes each title in 50+ bitrates/formats (AV1, VP9, H.265, H.264) to optimize for device and network
- **Zuul API Gateway**: Rate limiting, request routing, and authentication at the edge
- **Personalization Service**: Real-time recommendations using collaborative filtering and deep learning

## Technology Stack

- Java, Node.js (microservices), Cassandra (content metadata), Kafka (analytics)
- EVP (Encoded Video Processing) for transcoding, RocksDB (client-side caching)
- Custom telemetry for quality monitoring

## Lessons Learned

1. **Own your CDN at scale** — ISP partnerships and custom appliances reduce costs and latency far more than commercial CDNs
2. **Adaptive bitrate encoding trades off compute cost for bandwidth savings** — Encoding cost is negligible compared to transmission savings
3. **Observability at the edge** — Client-side metrics reveal more about quality than server-side metrics alone
4. **Chaos engineering for streaming** — Netflix intentionally breaks systems to improve fault tolerance

## Where this fits in the curriculum

- [Course 07, Exercise 5: Video streaming](../course-07-advanced-system-design/exercises/05-video-streaming.md).
- [Course 02 roadmap](../curriculum-roadmap.md) also assigns this study for CDN and personalization context.
- Course pointer: [course 07 wrapper](../course-07-advanced-system-design/case-studies/netflix-streaming-architecture.md).

## Further Reading

- [Netflix Technology Blog](https://netflixtechblog.com/)
- [Building a Distributed Encoder Service](https://netflixtechblog.com/building-a-distributed-encoder-service-b0beb3f6b9d5)
