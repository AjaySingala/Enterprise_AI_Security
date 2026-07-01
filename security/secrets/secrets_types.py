"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Secret Detection

File:
    types.py

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

###############################################################################
# Secret Types
###############################################################################
class SecretType(str, Enum):
    OPENAI_KEY = "OPENAI_KEY"
    AZURE_OPENAI_KEY = "AZURE_OPENAI_KEY"
    GITHUB_PAT = "GITHUB_PAT"
    AWS_ACCESS_KEY = "AWS_ACCESS_KEY"
    AWS_SECRET_KEY = "AWS_SECRET_KEY"
    GOOGLE_API_KEY = "GOOGLE_API_KEY"
    JWT = "JWT"
    PASSWORD = "PASSWORD"
    CONNECTION_STRING = "CONNECTION_STRING"
    PRIVATE_KEY = "PRIVATE_KEY"
    SSH_KEY = "SSH_KEY"
    PEM_CERTIFICATE = "PEM_CERTIFICATE"
    UNKNOWN = "UNKNOWN"

###############################################################################
# Severity
###############################################################################
class Severity(str, Enum):
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
# Secret Entity
###############################################################################
@dataclass(slots=True)
class SecretEntity:
    secret_type: SecretType
    value: str
    start: int
    end: int
    confidence: float
    severity: Severity
    detector: str

###############################################################################
# Detection Result
###############################################################################
@dataclass(slots=True)
class SecretDetectionResult:
    entities: list[SecretEntity]
    entity_count: int
    has_secrets: bool
    risk_score: int
