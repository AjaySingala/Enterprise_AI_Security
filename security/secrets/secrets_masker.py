"""
===============================================================================
Enterprise AI Security Framework

Feature:
    Secret Detection

File:
    masker.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Masks detected secrets using one of three modes.

1. FULL
2. PARTIAL
3. PLACEHOLDER
===============================================================================
"""

from __future__ import annotations

from security.secrets.secrets_types import (
    MaskMode,
    SecretDetectionResult,
)

class SecretMasker:
    """
    Masks detected secrets.
    """

    ###########################################################################
    def mask(
        self,
        text: str,
        detection_result: SecretDetectionResult,
        mode: MaskMode = MaskMode.PLACEHOLDER,
    ) -> str:
        print("--> Entering SecretMasker.mask")

        #
        # Replace from right-to-left so indexes remain valid.
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
                entity.secret_type.value,
                mode,
            )

            masked_text = (
                masked_text[:entity.start]
                + replacement
                + masked_text[entity.end:]
            )

        print("<-- Exiting SecretMasker.mask")

        return masked_text

    ###########################################################################
    def _replacement(
        self,
        value: str,
        secret_name: str,
        mode: MaskMode,
    ) -> str:
        if mode == MaskMode.FULL:
            return "*" * len(value)

        if mode == MaskMode.PARTIAL:
            return self._partial_mask(value)

        return f"<{secret_name}>"

    ###########################################################################
    @staticmethod
    def _partial_mask(
        value: str,
    ) -> str:
        if len(value) <= 6:
            return "*" * len(value)

        return (
            value[:4]
            + "*" * (len(value) - 8)
            + value[-4:]
        )
    