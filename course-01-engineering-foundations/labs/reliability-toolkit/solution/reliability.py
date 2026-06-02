from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, TypeVar


T = TypeVar("T")


def _backoff_delay_s(*, attempt: int, base_delay_s: float, max_delay_s: float) -> float:
    # attempt is 1-based (first failure => attempt=1)
    exp = base_delay_s * (2 ** (attempt - 1))
    capped = min(exp, max_delay_s)
    jitter = capped * (0.5 + random.random())
    return jitter


def retry(
    fn: Callable[[], T],
    *,
    max_attempts: int,
    base_delay_s: float,
    max_delay_s: float,
) -> T:
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt == max_attempts:
                break

            time.sleep(
                _backoff_delay_s(
                    attempt=attempt,
                    base_delay_s=base_delay_s,
                    max_delay_s=max_delay_s,
                )
            )

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

            if self._state == "half_open":
                # One failure in half-open sends us back to open.
                self._state = "open"
                self._opened_at = now
                raise

            if self._consecutive_failures >= self.failure_threshold:
                self._state = "open"
                self._opened_at = now
            raise

        # Success
        self._consecutive_failures = 0
        self._state = "closed"
        self._opened_at = None
        return result
