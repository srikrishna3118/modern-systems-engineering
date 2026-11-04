# Course 04 – AI Systems

**Duration:** 4 weeks. **Prerequisite:** Course 02. Course 03 helps for the serving infrastructure and is not required to start.

## Overview

This course covers the design and operation of AI and machine learning systems, including data pipelines, model training, and MLOps.

## Topics

- ML system design and architecture — [Lecture 1](lectures/lecture-01-ml-systems-data-training.md)
- Data ingestion and feature engineering pipelines — Lecture 1
- Model training at scale — Lecture 1
- Model serving and inference optimization — [Lecture 2](lectures/lecture-02-serving-mlops-monitoring.md)
- MLOps: CI/CD for ML systems — Lecture 2
- Monitoring and observability for AI systems — Lecture 2

## Learning Objectives

- Design end-to-end machine learning systems.
- Build and operate ML pipelines in production.
- Apply MLOps practices to maintain model quality over time.

## How to complete this course

1. Read Lecture 1 before thinking about serving.
2. Do the RAG lab. The index is a derived store; treat chunking and top-k as the experiment, not as boilerplate.
3. Read Lecture 2 and then the serving case studies. Compare what they measure.

## Lectures

- [Lecture 1: ML System Design, Data, and Training](lectures/lecture-01-ml-systems-data-training.md)
- [Lecture 2: Serving, MLOps, and Monitoring](lectures/lecture-02-serving-mlops-monitoring.md)

## Labs

- [RAG AI Assistant](labs/rag-ai-assistant) — chunking, a local index, grounded answers

## Case studies

Canonical copies live in [`../case-studies/`](../case-studies/). Course-local files are pointers.

- [Shopify ML platform](../case-studies/shopify-ml-platform.md)
- [OpenAI inference infrastructure](../case-studies/openai-inference-infrastructure.md)
- [NVIDIA AI cluster architecture](../case-studies/nvidia-ai-cluster-architecture.md)
- [Spotify recommendation pipeline](../case-studies/spotify-recommendation-pipeline.md)
