# Lab: Reliability Toolkit — Retries and Circuit Breakers

## Overview
Implement two common reliability patterns used in production services:

- **Retries with exponential backoff + jitter**
- **Circuit breaker** (closed → open → half-open)

You will use a simulated flaky downstream dependency and observe how these patterns affect success rate and tail latency.

## Learning Objectives
- Implement retry logic that is safe for idempotent operations.
- Prevent cascading failures with a circuit breaker.
- Measure trade-offs between reliability and latency.

## Prerequisites
- Python 3.10+

## Setup

```bash
cd course-01-engineering-foundations/labs/reliability-toolkit/starter-code
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python simulate.py
```

## Validation
Your output should show:

- baseline success rate and p95 latency
- improved success rate after adding retries
- improved stability after adding a circuit breaker (lower worst-case latency)

## Experiment
Tune backoff and breaker thresholds.

1. Increase `max_attempts` and observe how p95/p99 changes.
2. Change `failure_threshold` (breaker trips sooner/later) and compare success rate vs latency.

## Solution

```bash
cd ../solution
python simulate.py
```

The reference script prints baseline, retry, and circuit-breaker runs. No extra packages are required.
