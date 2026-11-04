# Lecture 2: Serving, MLOps, and Monitoring Models

## Overview

Serving is a latency budget with a model artifact behind it. MLOps is how that artifact gets replaced without a hero. Monitoring is how you notice the model is wrong before the product metric is. This lecture takes the system from [Lecture 1](lecture-01-ml-systems-data-training.md) and operates it.

## Topics

### 1. Model serving

The request path is: authenticate, fetch features, score, return. Everything you add to it is latency.

- **Batch serving** scores a pile of entities ahead of time and stores the result (recommendations computed nightly, risk scores refreshed hourly). The request path is a lookup. Use this whenever the decision can be a few minutes old.
- **Online serving** scores the request in front of the user. Budget the feature fetch and the model separately. A 5 ms model behind a 40 ms feature join is a feature-store problem.
- **The model is data, not code.** Load it from the registry by version. The process should be able to swap versions without a rebuild. Keep the previous version loaded, or loadable in seconds, so a rollback is a config change.
- **Batch the GPU.** A GPU wants a pile of requests at once. Continuous batching (assemble a batch from whatever is waiting, for a few milliseconds) is how LLM serving reaches decent utilization. The [OpenAI inference](../../case-studies/openai-inference-infrastructure.md) and [GPT inference](../../case-studies/openai-gpt-inference.md) cases are this idea at the expensive end: memory for the attention cache dominates, and the schedule of the batch is the product.

For retrieval systems such as the [RAG lab](../labs/rag-ai-assistant), "serving" is the index plus an optional generator. Measure retrieval quality (did the right passage come back) separately from generation quality. If retrieval is wrong, a larger model will say the wrong thing more fluently.

### 2. Inference optimizations you should be able to name

You do not have to build them. You have to know which lever matches which bottleneck.

- **Quantization** stores weights in fewer bits. It buys memory and speed and spends some accuracy. Measure the accuracy; do not assume it is free.
- **Distillation and smaller models** on the easy fraction of traffic, with a larger model on the rest. Route by difficulty or by user tier.
- **Caching** of repeated prompts or repeated feature vectors. Say what the cache key is, and how stale a cached score is allowed to be.
- **Speculative decoding** for generation: a small model drafts tokens, a large model checks them. It helps when the draft is usually right.

### 3. MLOps: CI/CD for models

A model change is a production change. Treat it like one, with extra steps because the tests are statistical.

1. Training code is reviewed and tested like any other code. Feature definitions are code.
2. A training run is reproducible: same code, same data snapshot, same result within the noise you have measured.
3. The candidate is evaluated offline against the champion, including on the slices that matter (new users, a country, a high-value merchant), not only on average accuracy.
4. Deployment is progressive: shadow (score, do not act), then a small percentage, then the rest. Each step has an automatic rollback if the live metric or the error rate moves the wrong way.
5. The registry records who promoted what, and the serving layer records which version answered each request. Without that, an incident is a guess.

Pipelines (Airflow, or a cloud scheduler) run the boring version of this nightly. A human looks at the promotion when the metric is close or the slice is sensitive. A human does not copy a weights file to a server by hand.

### 4. Monitoring

Infrastructure metrics are necessary and not sufficient. A model can return `200` and be useless.

- **Operational:** latency, error rate, saturation of the feature store and the GPU, fraction of requests served by each version.
- **Data:** the distribution of input features compared to the training window. A feature that is suddenly always zero is a pipeline break, not a trend.
- **Predictions:** the distribution of scores. A fraud model that used to flag 1% and today flags 15% has changed the product, whether or not the pipeline is "up."
- **Outcomes:** the delayed label. Click-through, chargeback rate, refund rate, joined back to the model version. This is the number that justifies the system, and it arrives late, so it cannot be your only alarm.

Alert on data and prediction movement the same day. Review outcome metrics on the cadence the labels actually arrive. Do not page a human on a metric that is noise at that timescale; do page on "the feature store is empty."

### 5. Failure

- **Feature store down.** Decide explicitly: fail the request, or score with defaults. Defaults for a fraud model are a policy decision (usually fail closed). Defaults for a ranking model can be a non-personalized fallback.
- **Bad deploy.** Roll back to the previous registry version. This only works if the previous version is still compatible with the current features. Coordinate feature changes the way you coordinate schema changes: add, migrate, then remove.
- **Training job green, model worse.** The offline metric was the wrong proxy. Keep the champion. Write down which live metric you will believe next time.

## Key Takeaways

1. **Batch the decision if it can be slightly stale.** Online serving is for the rest.
2. **A model artifact is versioned data.** Rollback is a config change to the previous version.
3. **Ship with shadow, then a percentage, then the rest.** Average offline accuracy is not a deploy plan.
4. **Monitor inputs and score distributions,** not only HTTP success. The labels arrive too late to be the only signal.
5. **Write down the fallback** for a missing feature store before it happens.

## Further Reading

- [OpenAI inference infrastructure](../../case-studies/openai-inference-infrastructure.md)
- [Shopify ML platform](../../case-studies/shopify-ml-platform.md)
- [Pinterest feed ranking](../../case-studies/pinterest-feed-ranking.md) — two-stage retrieval and ranking, which is serving architecture.
- [RAG lab](../labs/rag-ai-assistant)
