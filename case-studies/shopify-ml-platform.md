# Case Study: Shopify ML Platform – Production Machine Learning at Scale

## Overview

Shopify powers millions of merchants and processes billions of dollars in commerce. Its ML platform supports hundreds of models in production — from product recommendations and fraud detection to inventory forecasting and search ranking. This case study examines how Shopify built a platform that enables hundreds of data scientists to deploy and maintain ML models reliably.

## Key Challenges

- **Model Diversity**: Models range from simple gradient-boosted trees to large neural networks, each with different serving requirements
- **Freshness**: Fraud detection models must retrain on hourly data; recommendation models need daily refreshes
- **Reliability**: ML predictions power checkout fraud screening — false negatives cost merchants money, false positives lose customers
- **Developer Velocity**: 200+ data scientists need to deploy models without deep infrastructure knowledge
- **Feature Consistency**: Training/serving skew (features computed differently in training vs. production) causes silent model degradation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Merlin (ML Platform)                       │
│                                                               │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Feature    │  │ Training     │  │ Model Registry        │ │
│  │ Store      │  │ Pipeline     │  │ (versioned models,    │ │
│  │ (online +  │  │ (Spark +     │  │  metadata, lineage)   │ │
│  └──────┬─────┘  └──────┬───────┘  └──────────┬───────────┘ │
│         │               │                      │              │
│  ┌──────▼───────────────▼──────────────────────▼───────────┐ │
│  │            Model Serving Layer                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────────┐  │ │
│  │  │ Real-time   │  │ Batch       │  │ Edge (WASM)    │  │ │
│  │  │ Serving     │  │ Prediction  │  │ Serving        │  │ │
│  │  │ (gRPC, <10ms│  │ (Spark)     │  │ (storefront)   │  │ │
│  │  └─────────────┘  └─────────────┘  └────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │         Monitoring & Observability                        ││
│  │  Data drift detection │ Prediction logging │ A/B testing  ││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Feature Store (Online + Offline)**
   - **Offline**: Features computed via Spark on data lake, stored for training
   - **Online**: Same features served at low latency (< 5ms) via Redis/DynamoDB for inference
   - **Consistency guarantee**: Features are computed once in the offline pipeline, then materialized to the online store — eliminating training/serving skew

2. **Training Pipeline**
   - Declarative training configs (YAML) specifying model type, features, hyperparameters
   - Automated retraining on schedule (hourly, daily, weekly)
   - Training jobs run on Kubernetes with GPU autoscaling
   - Shadow evaluation: new model versions are scored against production data before promotion

3. **Model Serving**
   - **Real-time**: gRPC serving layer with model hot-swapping (< 10ms p99 latency)
   - **Batch**: Spark-based batch prediction for non-latency-sensitive use cases
   - **Edge**: WebAssembly-compiled models running on Shopify's CDN for storefront personalization
   - Canary deployments: new model versions serve 1% → 10% → 100% of traffic

4. **Monitoring**
   - **Data drift detection**: Statistical tests comparing current feature distributions against training data
   - **Prediction monitoring**: Tracking prediction distributions, latency, and error rates
   - **Business metric correlation**: Linking model changes to merchant revenue impact

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Feature Engineering | Apache Spark, dbt |
| Feature Store | Redis (online), Trino/S3 (offline) |
| Training | PyTorch, XGBoost, Kubernetes GPU nodes |
| Model Format | ONNX, TorchScript, native |
| Serving | Custom gRPC server (Go), Triton Inference Server |
| Orchestration | Airflow (batch), Argo Workflows (training) |
| Monitoring | Prometheus, Grafana, custom drift detectors |

## Lessons Learned

1. **Feature stores solve the training/serving skew problem** — Computing features once and materializing to both offline (training) and online (serving) stores eliminates the #1 source of silent model failures.

2. **Platform abstractions accelerate ML adoption** — Data scientists write YAML configs and Python model code; the platform handles infrastructure, deployment, monitoring, and rollbacks.

3. **Shadow scoring before deployment catches regressions** — Running new models against production data in shadow mode before promotion prevents bad models from reaching production.

4. **Edge inference unlocks new use cases** — Compiling models to WebAssembly and running them on the CDN enables sub-millisecond personalization on storefronts without round-trips to a serving cluster.

5. **Monitoring ML models requires domain-specific tooling** — Standard APM (latency, error rate) is insufficient. Data drift detection, prediction distribution monitoring, and business metric correlation are essential.

## Further Reading

- [Shopify Engineering Blog – Machine Learning](https://shopify.engineering/topics/data-science-engineering)
- [The ML Platform Behind Shopify's Products](https://shopify.engineering/merlin-shopify-machine-learning-platform)
- [Building Smarter Search with ML at Shopify](https://shopify.engineering/building-smarter-search)
