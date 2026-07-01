"""
===============================================================================
Enterprise AI Security Framework

File:
    masker.py

Feature:
    PII Detection

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Masks detected PII using one of three modes:

1. FULL
    john.doe@gmail.com
    ↓
    *******************

2. PARTIAL
    john.doe@gmail.com
    ↓
    j***@gmail.com

3. PLACEHOLDER
    john.doe@gmail.com
    ↓
    <EMAIL>
===============================================================================
"""

from __future__ import annotations

from security.pii.pii_types import (
    MaskMode,
    PIIDetectionResult,
)

class PIIMasker:
    """
    Masks detected PII.
    """

    ###########################################################################
    def mask(
        self,
        text: str,
        detection_result: PIIDetectionResult,
        mode: MaskMode = MaskMode.PLACEHOLDER,
    ) -> str:
        print("--> Entering PIIMasker.mask")

        #
        # Important:
        # Replace entities from right-to-left.
        # Otherwise indexes become invalid after replacements.
        #
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

        print("<-- Exiting PIIMasker.mask")

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

        #
        # Default
        #
        return f"<{entity_name}>"

    ###########################################################################
    @staticmethod
    def _partial_mask(
        value: str,
    ) -> str:
        if len(value) <= 4:
            return "*" * len(value)

        return (
            value[:2]
            + "*" * (len(value) - 4)
            + value[-2:]
        )
    