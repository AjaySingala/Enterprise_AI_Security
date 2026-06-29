"""
===============================================================================
PII Types: Data Model.

Defines common data structures used throughout the PII module.
===============================================================================
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class PIIType(str, Enum):
    PERSON = "PERSON"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    CREDIT_CARD = "CREDIT_CARD"
    PAN = "PAN"
    AADHAAR = "AADHAAR"
    PASSPORT = "PASSPORT"
    UPI = "UPI"
    IFSC = "IFSC"
    IP_ADDRESS = "IP_ADDRESS"
    URL = "URL"
    OPENAI_KEY = "OPENAI_KEY"
    GITHUB_TOKEN = "GITHUB_TOKEN"
    AWS_ACCESS_KEY = "AWS_ACCESS_KEY"
    JWT = "JWT"
    UNKNOWN = "UNKNOWN"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class MaskMode(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    PLACEHOLDER = "PLACEHOLDER"

@dataclass(slots=True)
class PIIEntity:
    entity_type: PIIType
    value: str
    start: int
    end: int
    confidence: float
    detector: str

@dataclass(slots=True)
class PIIDetectionResult:
    entities: list[PIIEntity]
    entity_count: int
    risk_score: int
    risk_level: RiskLevel
    has_pii: bool
    