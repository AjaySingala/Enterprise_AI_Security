"""
===============================================================================
Enterprise AI Security Framework

Timing Middleware

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

import time

from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request,
        call_next,
    ):
        start = time.perf_counter()

        response = await call_next(request)

        elapsed = time.perf_counter() - start

        response.headers["X-Process-Time"] = f"{elapsed:.4f}"

        return response
    