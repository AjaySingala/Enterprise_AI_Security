"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Confidential Data Detection

File:
    engine.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Enterprise Confidential Data Detection Engine.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from security.confidential.confidential_detector import ConfidentialDetector
from security.confidential.confidential_masker import ConfidentialMasker
from security.confidential.confidential_types import (
    ConfidentialDetectionResult,
    MaskMode,
)

###############################################################################
# Engine Result
###############################################################################
@dataclass(slots=True)
class ConfidentialEngineResult:
    original_text: str
    masked_text: str
    detection_result: ConfidentialDetectionResult

###############################################################################
# Engine
###############################################################################
class ConfidentialEngine:
    """
    Enterprise Confidential Data Detection Engine.
    """

    ###########################################################################
    def __init__(self):
        print("--> Entering ConfidentialEngine.__init__")

        self.detector = ConfidentialDetector()
        self.masker = ConfidentialMasker()

        print("<-- Exiting ConfidentialEngine.__init__")

    ###########################################################################
    def process(
        self,
        text: str,
        mask_mode: MaskMode = MaskMode.PLACEHOLDER,
    ) -> ConfidentialEngineResult:
        print("--> Entering ConfidentialEngine.process")

        detection = self.detector.detect(text)

        masked = self.masker.mask(
            text,
            detection,
            mask_mode,
        )

        print("<-- Exiting ConfidentialEngine.process")

        return ConfidentialEngineResult(
            original_text=text,
            masked_text=masked,
            detection_result=detection,
        )
    