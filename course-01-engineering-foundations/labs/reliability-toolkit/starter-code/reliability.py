from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, TypeVar


T = TypeVar("T")


def retry(
    fn: Callable[[], T],
    *,
    max_attempts: int,
    base_delay_s: float,
    max_delay_s: float,
) -> T:
    """Retry an idempotent operation.

    TODO (exercise): implement exponential backoff with jitter.
    """
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt == max_attempts:
                break

            # Starter: fixed sleep (intentionally suboptimal).
            delay = min(base_delay_s, max_delay_s)
            time.sleep(delay)

    assert last_exc is not None
    raise last_exc


@dataclass
class CircuitBreaker:
    failure_threshold: int
    recovery_timeout_s: float

    _state: str = "closed"  # closed | open | half_open
    _consecutive_failures: int = 0
    _opened_at: float | None = None

    def call(self, fn: Callable[[], T]) -> T:
        """Call fn through the breaker.

        TODO (exercise): implement half-open behavior.
        """
        now = time.monotonic()

        if self._state == "open":
            assert self._opened_at is not None
            if now - self._opened_at < self.recovery_timeout_s:
                raise RuntimeError("circuit_open")
            self._state = "half_open"

        try:
            result = fn()
        except Exception:  # noqa: BLE001
            self._consecutive_failures += 1
            if self._consecutive_failures >= self.failure_threshold:
                self._state = "open"
                self._opened_at = now
            raise

        self._consecutive_failures = 0
        self._state = "closed"
        self._opened_at = None
        return result


def jittered_delay(base: float) -> float:
    return base * (0.5 + random.random())
