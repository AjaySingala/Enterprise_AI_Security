"""
===============================================================================
Enterprise AI Gateway (EAIG)

Admin Router

Version:
    1.0.0
===============================================================================
"""

from fastapi import APIRouter

from fastapi import Depends

from api.dependencies import get_metrics

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Administration"],
)

@router.get("/metrics")
def metrics(
    metrics = Depends(get_metrics),
):
    return metrics.snapshot()
