"""
===============================================================================
Enterprise AI Security Framework

Security Router

Version:
    1.0.0
===============================================================================
"""

import uuid

from fastapi import APIRouter, Depends

from api.dependencies import get_pipeline
from api.models import (
    AnalyzeRequest,
    AnalyzeResponse,
)

from security.pipeline.pipeline_engine import SecurityPipeline

router = APIRouter(
    prefix="/security",
    tags=["Security"],
)

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
def analyze(
    request: AnalyzeRequest,
    pipeline: SecurityPipeline = Depends(get_pipeline),
):
    result = pipeline.process(request.text)

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
