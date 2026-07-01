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
    get_audit,
)

from common.audit import AuditRecord
from datetime import datetime
import time
import uuid

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
    audit = Depends(get_audit),
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

    audit.write(
        AuditRecord(
            timestamp=datetime.utcnow().isoformat(),
            request_id=str(uuid.uuid4()),   # request.state.correlation_id
            client_ip=request.client.host,
            decision=result.decision.value,
            pii_count=result.pii_result.detection_result.entity_count,
            secret_count=result.secret_result.detection_result.entity_count,
            confidential_count=result.confidential_result.detection_result.entity_count,
            processing_time_ms=elapsed_ms,
        )
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

