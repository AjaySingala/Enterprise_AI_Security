"""
===============================================================================
Enterprise AI Gateway (EAIG)

Correlation ID Middleware

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

import uuid

from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request,
        call_next,
    ):
        #
        # Reuse incoming correlation ID if present
        #
        correlation_id = request.headers.get(
            "X-Correlation-ID",
            str(uuid.uuid4()),
        )

        request.state.correlation_id = correlation_id

        response = await call_next(request)

        response.headers["X-Correlation-ID"] = correlation_id

        return response
    