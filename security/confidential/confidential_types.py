"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Confidential Data Detection

File:
    types.py

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

###############################################################################
# Confidential Types
###############################################################################
class ConfidentialType(str, Enum):
    PROJECT = "PROJECT"
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"
    CONTRACT = "CONTRACT"
    FINANCIAL = "FINANCIAL"
    SOURCE_CODE = "SOURCE_CODE"
    ROADMAP = "ROADMAP"
    INTERNAL_URL = "INTERNAL_URL"
    STRATEGY = "STRATEGY"
    UNKNOWN = "UNKNOWN"

###############################################################################
# Risk
###############################################################################
class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

###############################################################################
# Mask Mode
###############################################################################
class MaskMode(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    PLACEHOLDER = "PLACEHOLDER"

###############################################################################
# Entity
###############################################################################
@dataclass(slots=True)
class ConfidentialEntity:
    entity_type: ConfidentialType
    value: str
    start: int
    end: int
    confidence: float
    risk: RiskLevel
    detector: str

###############################################################################
# Result
###############################################################################
@dataclass(slots=True)
class ConfidentialDetectionResult:
    entities: list[ConfidentialEntity]
    entity_count: int
    risk_score: int
    has_confidential_data: bool
