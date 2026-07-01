"""
===============================================================================
Enterprise AI Gateway (EAIG)

File:
    engine.py

Feature:
    PII Detection

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Enterprise PII Engine.

Pipeline

Input Text
    │
    ▼
Regex Detection
    │
    ▼
Presidio Detection
    │
    ▼
Merge Results
    │
    ▼
Masking
    │
    ▼
Return Final Result
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from security.pii.pii_detector import PIIDetector
from security.pii.pii_masker import PIIMasker
from security.pii.pii_types import (
    MaskMode,
    PIIDetectionResult,
)

###############################################################################
# Engine Result
###############################################################################
@dataclass(slots=True)
class PIIEngineResult:
    original_text: str
    masked_text: str
    detection_result: PIIDetectionResult


###############################################################################
# Engine
###############################################################################
class PIIEngine:
    """
    Enterprise PII Engine.
    """

    ###########################################################################
    def __init__(self) -> None:
        print("--> Entering PIIEngine.__init__")

        self.detector = PIIDetector()
        self.masker = PIIMasker()

        print("<-- Exiting PIIEngine.__init__")

    ###########################################################################
    def process(
        self,
        text: str,
        mask_mode: MaskMode = MaskMode.PLACEHOLDER,
    ) -> PIIEngineResult:
        print("--> Entering PIIEngine.process")

        detection = self.detector.detect(text)
        masked = self.masker.mask(
            text,
            detection,
            mask_mode,
        )

        print("<-- Exiting PIIEngine.process")

        return PIIEngineResult(
            original_text=text,
            masked_text=masked,
            detection_result=detection,
        )
    