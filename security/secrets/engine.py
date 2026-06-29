"""
===============================================================================
Enterprise AI Security Framework

Feature:
    Secret Detection

File:
    engine.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Enterprise Secret Detection Engine.

Pipeline

Input
   │
   ▼
Regex Detection
   │
   ▼
Entropy Detection
   │
   ▼
Risk Scoring
   │
   ▼
Masking
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from security.secrets.detector import SecretDetector
from security.secrets.masker import SecretMasker
from security.secrets.types import (
    MaskMode,
    SecretDetectionResult,
)

###############################################################################
# Engine Result
###############################################################################
@dataclass(slots=True)
class SecretEngineResult:
    original_text: str
    masked_text: str
    detection_result: SecretDetectionResult

###############################################################################
# Engine
###############################################################################
class SecretEngine:
    """
    Enterprise Secret Detection Engine.
    """
    ###########################################################################
    def __init__(self):
        print("--> Entering SecretEngine.__init__")

        self.detector = SecretDetector()
        self.masker = SecretMasker()

        print("<-- Exiting SecretEngine.__init__")

    ###########################################################################
    def process(
        self,
        text: str,
        mask_mode: MaskMode = MaskMode.PLACEHOLDER,
    ) -> SecretEngineResult:
        print("--> Entering SecretEngine.process")

        detection = self.detector.detect(text)
        masked = self.masker.mask(
            text,
            detection,
            mask_mode,
        )

        print("<-- Exiting SecretEngine.process")

        return SecretEngineResult(
            original_text=text,
            masked_text=masked,
            detection_result=detection,
        )
    