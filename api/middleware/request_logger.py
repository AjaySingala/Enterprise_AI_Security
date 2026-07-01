"""
===============================================================================
Enterprise AI Gateway (EAIG)

Request Logging Middleware

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

import time

from starlette.middleware.base import BaseHTTPMiddleware

from common.logger import get_logger

logger = get_logger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request,
        call_next,
    ):
        correlation_id = getattr(
            request.state,
            "correlation_id",
            "UNKNOWN",
        )

        logger.info("=" * 80)
        logger.info("Request Started")
        logger.info("Request ID : %s", correlation_id)
        logger.info("Method     : %s", request.method)
        logger.info("Path       : %s", request.url.path)
        logger.info("Client     : %s", request.client.host)

        start = time.perf_counter()

        response = await call_next(request)

        elapsed = time.perf_counter() - start

        logger.info("Status     : %s", response.status_code)
        logger.info("Duration   : %.4f sec", elapsed)
        logger.info("Request Completed")
        logger.info("=" * 80)

        return response
    