"""
===============================================================================
Enterprise AI Gateway (EAIG)

Global Exception Handlers

Version:
    1.0.0
===============================================================================
"""

from fastapi import Request
from fastapi.responses import JSONResponse

async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    correlation_id = getattr(
        request.state,
        "correlation_id",
        "UNKNOWN",
    )

    return JSONResponse(
        status_code=500,
        content={
            "request_id": correlation_id,
            "error": str(exc),
        },
    )
