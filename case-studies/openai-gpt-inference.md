# Case Study: OpenAI GPT Inference Infrastructure

## Overview

OpenAI serves billions of API requests for GPT models, handling inference at unprecedented scale. The system must deliver low-latency responses for real-time chat, support massive throughput for batch workloads, and efficiently utilize some of the world's most expensive hardware (GPU clusters). This case study examines the engineering behind large language model (LLM) serving infrastructure.

## Key Challenges

- **GPU Utilization**: A100/H100 GPUs cost $2–$3/hour each. Even 10% idle time represents millions of dollars annually
- **Latency vs. Throughput**: Chat applications require low time-to-first-token (< 500ms); batch applications need high throughput
- **Model Size**: GPT-4 class models require multiple GPUs per instance (tensor parallelism) and multiple instances per request (expert parallelism for MoE)
- **Token Generation**: Autoregressive generation is inherently sequential — each token depends on all previous tokens
- **Scaling**: Handling millions of concurrent users with highly variable request lengths (10 tokens to 100K+ tokens)

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       API Gateway                             │
│            (Rate limiting, auth, routing)                      │
└────────────┬──────────────────────────────────┬──────────────┘
             │                                  │
    ┌────────▼─────────┐              ┌────────▼─────────────┐
    │  Request Router   │              │  Batch Queue         │
    │  (latency-        │              │  (throughput-         │
    │   optimized)      │              │   optimized)          │
    └────────┬─────────┘              └────────┬─────────────┘
             │                                  │
    ┌────────▼──────────────────────────────────▼──────────────┐
    │                  Inference Scheduler                       │
    │         (Continuous batching, priority queues)             │
    └────────────────────────┬─────────────────────────────────┘
                             │
    ┌────────────────────────▼─────────────────────────────────┐
    │                   GPU Cluster                              │
    │                                                            │
    │  ┌─ Instance ──────────────────────────────────────────┐  │
    │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │  │
    │  │  │GPU 0 │ │GPU 1 │ │GPU 2 │ │GPU 3 │ │GPU N │     │  │
    │  │  │      │ │      │ │      │ │      │ │      │     │  │
    │  │  │Model │ │Model │ │Model │ │Model │ │Model │     │  │
    │  │  │Shard │ │Shard │ │Shard │ │Shard │ │Shard │     │  │
    │  │  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘     │  │
    │  │     └────NVLink/NVSwitch All-to-All──────┘         │  │
    │  └─────────────────────────────────────────────────────┘  │
    │                                                            │
    │  ┌─ KV Cache Store ─────────────────────────────────────┐ │
    │  │  PagedAttention (vLLM) / RadixAttention              │ │
    │  │  Virtual memory management for KV cache              │ │
    │  └──────────────────────────────────────────────────────┘ │
    └──────────────────────────────────────────────────────────┘
```

### Key Optimization Techniques

#### 1. Continuous Batching
Traditional batching waits for a fixed number of requests, then processes them together. **Continuous batching** (iteration-level scheduling) allows new requests to join an in-progress batch at each decoding step:

```
Traditional Batching:
  Request A: [████████████████ idle idle idle]
  Request B: [████████████████████████████████]
  Request C: [████████████████████████ idle   ]
  GPU Util:   ████████████████████████████████

Continuous Batching:
  Request A: [████████████████]
  Request D:                   [███████████████]  ← joins immediately
  Request B: [████████████████████████████████]
  Request C: [████████████████████████]
  GPU Util:   ████████████████████████████████  (no idle slots)
```

#### 2. PagedAttention (KV Cache Management)
The key-value cache for attention grows with sequence length and consumes most GPU memory. **PagedAttention** (from the vLLM project) manages KV cache like virtual memory:
- KV cache is divided into fixed-size **pages** (blocks)
- Pages are allocated on demand, not pre-allocated for max sequence length
- This reduces memory waste by 60–80%, enabling 2–4x more concurrent requests

#### 3. Speculative Decoding
A small "draft" model generates N candidate tokens in parallel. The large "target" model verifies them in a single forward pass. If the draft matches, all N tokens are accepted, achieving near N× speedup for those tokens:

```
Without Speculative Decoding:  1 token per forward pass
With Speculative Decoding:     3-5 tokens accepted per verification pass
```

#### 4. Tensor Parallelism + Pipeline Parallelism
Large models are split across GPUs:
- **Tensor Parallelism**: Each layer's weight matrix is split across GPUs (requires fast interconnect — NVLink)
- **Pipeline Parallelism**: Different layers are placed on different GPUs (works across slower interconnects)
- **Expert Parallelism**: For Mixture-of-Experts (MoE) models, different experts run on different GPUs

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Inference Engine | Custom (based on Triton, vLLM concepts) |
| GPU Hardware | NVIDIA H100, A100 (NVLink/NVSwitch interconnect) |
| Networking | InfiniBand (400Gbps), RoCE |
| Orchestration | Kubernetes on Azure |
| Model Format | Safetensors, custom quantized formats (INT8, FP8) |
| Monitoring | Custom GPU utilization, token throughput, TTFT dashboards |

## Performance Metrics

| Metric | Target |
|--------|--------|
| Time to First Token (TTFT) | < 500ms (chat) |
| Inter-Token Latency (ITL) | < 30ms per token |
| Throughput | Thousands of tokens/sec/GPU |
| GPU Utilization | > 90% during peak |
| Availability | 99.9%+ |

## Lessons Learned

1. **Memory is the bottleneck, not compute** — KV cache memory limits concurrent requests far more than GPU compute capacity. PagedAttention's virtual memory approach unlocks 2–4x more concurrency.

2. **Continuous batching transforms GPU economics** — Filling every decode step with useful work (instead of padding to max length) can double effective throughput.

3. **The prefill/decode split is fundamental** — Prefill (processing the prompt) is compute-bound; decode (generating tokens) is memory-bandwidth-bound. Disaggregating these phases onto different hardware optimizes both.

4. **Quantization is a production necessity** — FP8 and INT8 quantization halve memory requirements with minimal quality loss, enabling larger batch sizes and lower costs.

5. **Speculative decoding changes the latency equation** — For models where a good draft model exists, speculative decoding provides 2–3x latency improvement at no quality cost.

## Further Reading

- [Efficient Memory Management for Large Language Model Serving with PagedAttention (SOSP 2023)](https://arxiv.org/abs/2309.06180)
- [vLLM: Easy, Fast, and Cheap LLM Serving](https://github.com/vllm-project/vllm)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models (OSDI 2022)](https://www.usenix.org/conference/osdi22/presentation/yu)
- [OpenAI API Platform](https://platform.openai.com/docs)
