# Case Study: OpenAI Inference Infrastructure – LLM Serving at Scale

## Overview

OpenAI serves billions of API requests for GPT models, handling inference at unprecedented scale while maintaining low latency. The system optimally utilizes some of the world's most expensive hardware (GPU clusters) to serve diverse workloads from real-time chat to batch processing.

## Key Challenges

- **GPU Utilization**: H100 GPUs cost $2–3/hour; even 10% idle time represents millions of dollars annually
- **Latency vs. Throughput**: Chat requires low time-to-first-token (< 500ms); batch jobs need high throughput
- **Model Sizes**: Large models require tensor parallelism across multiple GPUs
- **Token Generation**: Autoregressive decoding is sequentially dependent; token-by-token inference is memory-bandwidth-bound
- **Request Heterogeneity**: Request lengths range from 10 to 100K+ tokens; batching is complex

## Architecture Highlights

- **Continuous Batching**: New requests join in-progress batches at each decode step (not traditional static batching)
- **PagedAttention (vLLM)**: Manages KV cache with virtual memory semantics; reduces memory fragmentation by 60–80%
- **Speculative Decoding**: Draft model generates candidates; target model verifies in parallel; achieves 2–3x speedup
- **Two-Phase Scheduling**:
  - **Prefill**: Process input tokens (compute-bound); amortize cost across sequence
  - **Decode**: Generate output tokens (memory-bandwidth-bound); each token incurs separate latency
- **Distributed Inference**: Tensor parallelism (layers split across GPUs) + pipeline parallelism (different layers on different GPUs)

## Technology Stack

- NVIDIA H100 GPUs, custom inference engine (based on Triton, vLLM concepts)
- NCCL (collective communications), vLLM (open-source inference library)
- Kubernetes orchestration, Azure cloud infrastructure

## Performance Metrics

| Metric | Target |
|--------|--------|
| Time to First Token (TTFT) | < 500ms |
| Inter-Token Latency | < 30ms |
| Throughput | 1000s of tokens/sec/GPU |
| GPU Utilization | > 90% |

## Lessons Learned

1. **Memory is the bottleneck, not compute** — KV cache memory limits concurrent requests more than GPU compute; PagedAttention unlocks 2–4x concurrency
2. **Continuous batching transforms economics** — Filling every decode step with work doubles effective throughput
3. **The prefill/decode split is fundamental** — Prefill is compute-bound; decode is memory-bandwidth-bound; optimize separately
4. **Quantization enables larger batch sizes** — FP8/INT8 quantization halves memory requirements; enables larger batches at no quality cost
5. **Speculative decoding changes latency** — For models where good draft models exist, 2–3x latency improvement is achievable

## Further Reading

- [vLLM: Easy, Fast, and Cheap LLM Serving](https://github.com/vllm-project/vllm)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention (SOSP 2023)](https://arxiv.org/abs/2309.06180)
- [Orca: Distributed Serving System for Transformer-Based Generative Models (OSDI 2022)](https://www.usenix.org/conference/osdi22/presentation/yu)
