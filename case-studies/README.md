# Case studies

Canonical write-ups live in this folder. Course folders keep short pointer files so a course can list its reading without copying the text. When a study and a course disagree, this folder is the one to fix.

Each study uses the same skeleton: overview, key challenges, architecture, technology stack, lessons learned, and further reading. Studies assigned by a course also have a "Where this fits in the curriculum" section.

`stripe-payment-processing.md` is a shorter companion to `stripe-payment-system.md`. The courses assign the longer file.

## By course

| Course | Assigned studies |
|--------|------------------|
| [01 Foundations](../course-01-engineering-foundations/syllabus.md) | [AWS cells](aws-cell-architecture.md), [Uber microservices](uber-microservices-migration.md) |
| [02 Distributed systems](../course-02-distributed-systems/syllabus.md) | [Netflix streaming](netflix-streaming-architecture.md), [Uber dispatch](uber-dispatch-system.md), [Kafka](kafka-event-streaming.md), [Spanner](google-spanner-consistency.md), [Discord chat](discord-chat-infrastructure.md) |
| [03 Cloud](../course-03-cloud-infrastructure/syllabus.md) | [Kubernetes](kubernetes-orchestration.md), [AWS cells](aws-cell-architecture.md), [Aurora](aws-aurora.md) |
| [04 AI systems](../course-04-ai-systems/syllabus.md) | [Shopify ML](shopify-ml-platform.md), [OpenAI inference](openai-inference-infrastructure.md), [NVIDIA clusters](nvidia-ai-cluster-architecture.md), [Spotify](spotify-recommendation-pipeline.md) |
| [05 Real-time](../course-05-realtime-systems/syllabus.md) | [Figma](figma-realtime-collaboration.md), [Discord chat](discord-chat-infrastructure.md), [WhatsApp](whatsapp-messaging-system.md) |
| [06 Financial](../course-06-financial-systems/syllabus.md) | [Stripe](stripe-payment-system.md) |
| [07 Advanced design](../course-07-advanced-system-design/syllabus.md) | [Cloudflare](cloudflare-ddos-defense.md), [GitHub code search](github-code-search.md), [Shopify flash sales](shopify-flash-sale-scaling.md), [YouTube](youtube-video-delivery.md), [Netflix streaming](netflix-streaming-architecture.md) |

## All studies

**Messaging.** [WhatsApp](whatsapp-messaging-system.md), [Slack](slack-message-queue.md), [Discord chat](discord-chat-infrastructure.md), [Discord message storage](discord-message-storage.md), [Figma](figma-realtime-collaboration.md)

**Search and discovery.** [Uber dispatch](uber-dispatch-system.md), [Airbnb](airbnb-search-platform.md), [Pinterest](pinterest-feed-ranking.md), [GitHub code search](github-code-search.md), [GitHub code review](github-code-review.md)

**Streaming and media.** [Netflix streaming](netflix-streaming-architecture.md), [Netflix CDN](netflix-cdn.md), [YouTube](youtube-video-delivery.md), [Spotify](spotify-recommendation-pipeline.md)

**Data and infrastructure.** [Kafka](kafka-event-streaming.md), [Spanner](google-spanner-consistency.md), [AWS cells](aws-cell-architecture.md), [Aurora](aws-aurora.md), [Kubernetes](kubernetes-orchestration.md), [NVIDIA](nvidia-ai-cluster-architecture.md)

**ML serving.** [OpenAI inference](openai-inference-infrastructure.md), [OpenAI GPT inference](openai-gpt-inference.md), [Shopify ML](shopify-ml-platform.md)

**Payments and scale.** [Stripe](stripe-payment-system.md) ([shorter note](stripe-payment-processing.md)), [Shopify flash sales](shopify-flash-sale-scaling.md), [Uber microservices](uber-microservices-migration.md)

**Edge and abuse.** [Cloudflare](cloudflare-ddos-defense.md)
