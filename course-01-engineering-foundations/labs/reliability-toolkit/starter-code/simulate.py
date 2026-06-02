from __future__ import annotations

import random
import statistics
import time

from reliability import CircuitBreaker, retry


def flaky_dependency() -> str:
    # 25% failure rate, plus occasional slow spikes.
    if random.random() < 0.25:
        raise RuntimeError("downstream_error")
    if random.random() < 0.05:
        time.sleep(0.25)
    time.sleep(0.01)
    return "ok"


def run(label: str, fn, *, n: int = 200):
    latencies = []
    successes = 0
    for _ in range(n):
        start = time.perf_counter()
        try:
            fn()
            successes += 1
        except Exception:  # noqa: BLE001
            pass
        latencies.append((time.perf_counter() - start) * 1000)

    latencies_sorted = sorted(latencies)
    p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
    print(
        f"{label}: success={successes}/{n} ({successes/n:.0%}), "
        f"median={statistics.median(latencies):.1f}ms, p95={p95:.1f}ms"
    )


def main() -> None:
    random.seed(7)

    run("baseline", flaky_dependency)

    run(
        "retry(3)",
        lambda: retry(
            flaky_dependency,
            max_attempts=3,
            base_delay_s=0.02,
            max_delay_s=0.2,
        ),
    )

    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout_s=0.5)
    run(
        "retry(3)+breaker",
        lambda: retry(
            lambda: breaker.call(flaky_dependency),
            max_attempts=3,
            base_delay_s=0.02,
            max_delay_s=0.2,
        ),
    )


if __name__ == "__main__":
    main()
