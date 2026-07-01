"""
===============================================================================
Enterprise AI Gateway (EAIG)

Metrics Service

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from threading import Lock

###############################################################################
# Metrics
###############################################################################
@dataclass(slots=True)
class Metrics:
    requests: int = 0
    allowed: int = 0
    sanitized: int = 0
    blocked: int = 0
    total_processing_time_ms: float = 0.0

###############################################################################
# Service
###############################################################################
class MetricsService:
    def __init__(self):
        self._metrics = Metrics()
        self._lock = Lock()

    ###########################################################################
    def record(
        self,
        decision: str,
        processing_time_ms: float,
    ) -> None:
        with self._lock:
            self._metrics.requests += 1
            self._metrics.total_processing_time_ms += processing_time_ms
            decision = decision.upper()

            if decision == "ALLOW":
                self._metrics.allowed += 1
            elif decision == "SANITIZE":
                self._metrics.sanitized += 1
            elif decision == "BLOCK":
                self._metrics.blocked += 1

    ###########################################################################
    def snapshot(self) -> dict:
        with self._lock:
            average = 0.0
            if self._metrics.requests > 0:
                average = (
                    self._metrics.total_processing_time_ms
                    / self._metrics.requests
                )

            return {
                "requests": self._metrics.requests,
                "allowed": self._metrics.allowed,
                "sanitized": self._metrics.sanitized,
                "blocked": self._metrics.blocked,
                "average_response_time_ms": round(
                    average,
                    2,
                ),
            }

###############################################################################
metrics_service = MetricsService()
