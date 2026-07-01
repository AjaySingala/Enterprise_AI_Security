"""
===============================================================================
Enterprise AI Gateway (EAIG)

Security Router

Version:
    1.0.0
===============================================================================
"""

import uuid
import time

from fastapi import APIRouter, Depends

from api.dependencies import get_pipeline
from api.models import (
    AnalyzeRequest,
    AnalyzeResponse,
)

from security.pipeline.pipeline_engine import SecurityPipeline

from api.dependencies import (
    get_metrics,
    get_pipeline,
)

router = APIRouter(
    prefix="/api/v1/security",
    tags=["Security"],
)

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
def analyze(
    request: AnalyzeRequest,
    pipeline = Depends(get_pipeline),
    metrics = Depends(get_metrics),
):
    start = time.perf_counter()
    result = pipeline.process(request.text)

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    metrics.record(
        result.decision.value,
        elapsed_ms,
    )

    return AnalyzeResponse(
        request_id=str(uuid.uuid4()),
        decision=result.decision.value,
        sanitized_text=result.sanitized_text,
        reasons=result.reasons,
    )

@router.post("/sanitize")
def sanitize(
    request: AnalyzeRequest,
    pipeline: SecurityPipeline = Depends(get_pipeline),
):
    result = pipeline.process(request.text)

    return {
        "request_id": str(uuid.uuid4()),
        "sanitized_text": result.sanitized_text,
    }
