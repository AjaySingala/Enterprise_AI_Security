"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Enterprise Security Pipeline

File:
    types.py

Version:
    1.1.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

###############################################################################
# Decision
###############################################################################
class PipelineDecision(str, Enum):
    ALLOW = "ALLOW"
    SANITIZE = "SANITIZE"
    BLOCK = "BLOCK"

###############################################################################
# Pipeline Result
###############################################################################
@dataclass(slots=True)
class SecurityPipelineResult:
    #
    # Original user input
    #
    original_text: str

    #
    # Sanitized text that can safely be sent to the LLM
    #
    sanitized_text: str

    #
    # Final decision
    #
    decision: PipelineDecision

    #
    # Why this decision was taken
    #
    reasons: list[str] = field(default_factory=list)

    #
    # Individual engine results
    #
    prompt_result: object | None = None
    pii_result: object | None = None
    secret_result: object | None = None
    confidential_result: object | None = None
