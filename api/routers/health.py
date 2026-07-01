"""
===============================================================================
Enterprise AI Gateway (EAIG)

Health Router

Version:
    1.0.0
===============================================================================
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health"],
)

@router.get("")
def health():
    return {
        "status": "UP",
        "version": "1.0.0",
    }

@router.get("/ready")
def readiness():
    #
    # Later:
    # Check OpenAI
    # Check Vector DB
    # Check Database
    #
    return {
        "status": "READY",
    }
