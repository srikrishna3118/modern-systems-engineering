# Course 07 – Advanced System Design

**Duration:** 4 weeks. **Prerequisite:** Courses 02, 03, and 05. Course 06 helps for anything that moves money, and is not required to start.

## Overview

This course is the synthesis. You already have the mechanisms (replication, containers, streams). Here you practice the judgment: estimate the bottleneck, pick a design, and say what you gave up. It is also the interview-prep course. The five exercises are the practice set a later video course can be recorded against.

## Topics

- Designing for scale: horizontal vs. vertical scaling — [Lecture 1](lectures/lecture-01-designing-for-scale.md)
- Global system design and multi-region architectures — [Lecture 2](lectures/lecture-02-global-multi-region.md)
- Database selection and schema design trade-offs — [Lecture 3](lectures/lecture-03-database-selection.md)
- Rate limiting, throttling, and quotas — [Lecture 4](lectures/lecture-04-rate-limiting.md)
- Security architecture and zero-trust design — [Lecture 5](lectures/lecture-05-security-zero-trust.md)
- System design interviews and communication — [Lecture 6](lectures/lecture-06-system-design-interviews.md)

## Learning Objectives

- Turn a vague product prompt into requirements and a capacity estimate.
- Choose a scaling, data, and regional shape, and name the alternative you rejected.
- Design rate limiting and trust boundaries as part of the system, not as a footnote.
- Present a design in one diagram, one data model, and one deep dive.

## How to complete this course

1. Read Lectures 1–5. Lecture 6 is the method for the exercises; read it before the first one.
2. For each exercise, attempt it closed-book, then read the worked solution and the linked case study.
3. Write the trade-off in your own words. The point is the decision, not the diagram.

## Lectures

- [Lecture 1: Designing for Scale](lectures/lecture-01-designing-for-scale.md)
- [Lecture 2: Global and Multi-Region Design](lectures/lecture-02-global-multi-region.md)
- [Lecture 3: Database Selection and Schema Design](lectures/lecture-03-database-selection.md)
- [Lecture 4: Rate Limiting, Throttling, and Quotas](lectures/lecture-04-rate-limiting.md)
- [Lecture 5: Security Architecture and Zero Trust](lectures/lecture-05-security-zero-trust.md)
- [Lecture 6: System Design Interviews](lectures/lecture-06-system-design-interviews.md)

## Exercises

- [Exercise index](exercises/system-design-exercises.md)
- [1. URL shortener](exercises/01-url-shortener.md)
- [2. Real-time notifications](exercises/02-notification-system.md)
- [3. Rate limiter](exercises/03-rate-limiter.md)
- [4. Full-text search](exercises/04-full-text-search.md)
- [5. Video streaming](exercises/05-video-streaming.md)

## Case studies

Canonical copies live in [`../case-studies/`](../case-studies/). The files in [`case-studies/`](case-studies/) are pointers, so this course does not drift from the library. Map: [case-studies/README.md](case-studies/README.md).

Required:

- [Cloudflare DDoS defense](../case-studies/cloudflare-ddos-defense.md) — edge filtering, with Lectures 4 and 5.
- [GitHub code search](../case-studies/github-code-search.md) — with Exercise 4.
- [Shopify flash-sale scaling](../case-studies/shopify-flash-sale-scaling.md) — with Lectures 1 and 4.
- [YouTube video delivery](../case-studies/youtube-video-delivery.md) and [Netflix streaming](../case-studies/netflix-streaming-architecture.md) — with Exercise 5.

Supporting, linked from the lectures when a mechanism needs a production example:

- [AWS cell architecture](../case-studies/aws-cell-architecture.md)
- [Google Spanner](../case-studies/google-spanner-consistency.md)
- [Kafka](../case-studies/kafka-event-streaming.md), [Slack's queue](../case-studies/slack-message-queue.md), [WhatsApp](../case-studies/whatsapp-messaging-system.md)
- [Stripe](../case-studies/stripe-payment-system.md)
- [Airbnb search](../case-studies/airbnb-search-platform.md)

## Resources

- [Architecture Diagrams Guide](../architecture-diagrams-guide.md)
