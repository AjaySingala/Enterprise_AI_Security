"""
===============================================================================
Enterprise AI Security Framework

Enterprise Security API

models.py

Version:
    1.0.0
===============================================================================
"""

from pydantic import BaseModel

###############################################################################
# Requests
###############################################################################
class AnalyzeRequest(BaseModel):
    text: str

###############################################################################
# Responses
###############################################################################
class AnalyzeResponse(BaseModel):
    request_id: str
    decision: str
    sanitized_text: str
    reasons: list[str]
