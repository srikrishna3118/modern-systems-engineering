# Case Study: Netflix CDN – Open Connect

## Overview
Netflix delivers billions of hours of video per month to subscribers in over 190 countries. To handle this scale, Netflix built its own Content Delivery Network (CDN) called Open Connect, which places servers (appliances) directly inside Internet Service Provider (ISP) networks. This case study examines the distributed systems challenges behind global video delivery at scale.

## Key Challenges
- **Global scale**: Delivering HD and 4K video to 200M+ concurrent viewers.
- **Bandwidth costs**: Minimizing expensive transit bandwidth between data centers and ISPs.
- **Cache efficiency**: Ensuring popular content is pre-positioned close to viewers before peak hours.
- **Fault tolerance**: Failing over gracefully when appliances or network paths are unavailable.

## Architecture Highlights

### Open Connect Appliances (OCAs)
Netflix places physical servers inside ISP networks. These servers cache popular titles and stream directly to subscribers within the same network, dramatically reducing the distance data travels.

### Proactive Caching (Filling)
Each night during off-peak hours, Netflix's central systems analyze global viewing patterns and pre-position (fill) the most likely-to-be-watched content on each OCA. This is called "proactive caching" and it ensures cache hit rates exceed 95% during peak hours.

### Steering Layer
The Netflix client uses a steering API to determine the best OCA to connect to for a given title and viewer location. The steering service considers OCA health, network distance, and current load.

### Adaptive Bitrate Streaming
Netflix uses DASH (Dynamic Adaptive Streaming over HTTP) to serve multiple bitrate versions of each title. The client dynamically selects the appropriate quality based on available bandwidth.

## Technology Stack
- **Appliance OS**: FreeBSD, custom-tuned for high-throughput video serving
- **Encoding**: Multiple bitrate/resolution variants per title (AV1, H.264, H.265)
- **Steering service**: Java, deployed on AWS
- **Monitoring**: Atlas (Netflix's internal time-series metrics system)

## Lessons Learned
1. Moving compute and data closer to users (edge caching) is the most effective way to reduce latency and bandwidth cost.
2. Proactive caching based on predicted demand is far more effective than purely reactive caching.
3. Operational visibility into thousands of globally distributed nodes requires a purpose-built monitoring platform.
4. Partnering with ISPs (by placing hardware in their networks) creates win-win outcomes on network costs.

## Further Reading
- [Netflix Tech Blog – How Netflix Works: The Highly Simplified Complex Stuff](https://netflixtechblog.com/how-netflix-works-the-highly-simplified-complex-stuff-that-happens-every-time-you-hit-play-3a40c9be254b)
- [Netflix Tech Blog – Open Connect Overview](https://openconnect.netflix.com/en/)
