"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Confidential Data Detection

File:
    masker.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Masks confidential information.

Supported Modes

1. FULL
2. PARTIAL
3. PLACEHOLDER
===============================================================================
"""

from __future__ import annotations

from config.config import settings

from security.confidential.confidential_types import (
    ConfidentialDetectionResult,
    MaskMode,
)

class ConfidentialMasker:
    """
    Masks confidential information.
    """

    ###########################################################################
    def mask(
        self,
        text: str,
        detection_result: ConfidentialDetectionResult,
        mode: MaskMode = MaskMode.PLACEHOLDER,
    ) -> str:
        if settings.debug:
            print("--> Entering ConfidentialMasker.mask")

        entities = sorted(
            detection_result.entities,
            key=lambda x: x.start,
            reverse=True,
        )

        masked_text = text

        for entity in entities:
            replacement = self._replacement(
                entity.value,
                entity.entity_type.value,
                mode,
            )

            masked_text = (
                masked_text[:entity.start]
                + replacement
                + masked_text[entity.end:]
            )

        if settings.debug:
            print("<-- Exiting ConfidentialMasker.mask")

        return masked_text

    ###########################################################################
    def _replacement(
        self,
        value: str,
        entity_name: str,
        mode: MaskMode,
    ) -> str:
        if mode == MaskMode.FULL:
            return "*" * len(value)

        if mode == MaskMode.PARTIAL:
            return self._partial_mask(value)

        return f"<{entity_name}>"

    ###########################################################################
    @staticmethod
    def _partial_mask(
        value: str,
    ) -> str:
        if len(value) <= 6:
            return "*" * len(value)

        return (
            value[:3]
            + "*" * (len(value) - 6)
            + value[-3:]
        )
    