"""
===============================================================================
Enterprise AI Security Framework

Feature:
    Secret Detection

File:
    detector.py

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

import re

from security.secrets.secrets_entropy import EntropyDetector
from security.secrets.secrets_patterns import PATTERNS
from security.secrets.secrets_types import (
    SecretDetectionResult,
    SecretEntity,
    SecretType,
    Severity,
)

class SecretDetector:
    """
    Enterprise Secret Detector.
    """

    ###########################################################################
    def __init__(self):
        print("--> Entering SecretDetector.__init__")

        self.context_keywords = {
            "password",
            "passwd",
            "pwd",
            "secret",
            "token",
            "apikey",
            "api_key",
            "key",
            "credential",
            "connectionstring",
            "connection_string",
            "bearer",
        }

        print("<-- Exiting SecretDetector.__init__")

    ###########################################################################
    def detect(
        self,
        text: str,
    ) -> SecretDetectionResult:
        print("--> Entering SecretDetector.detect")

        entities: list[SecretEntity] = []

        #######################################################################
        # Regex Detection
        #######################################################################
        for secret_type, pattern in PATTERNS.items():
            for match in re.finditer(pattern, text):
                entities.append(
                    SecretEntity(
                        secret_type=secret_type,
                        value=match.group(),
                        start=match.start(),
                        end=match.end(),
                        confidence=1.0,
                        severity=self._severity(secret_type),
                        detector="Regex",
                    )
                )

        #######################################################################
        # High Entropy Detection
        #######################################################################
        words = re.findall(
            # r"[A-Za-z0-9_\-+=/]{20,}",      # Try this first. Does not detect "random" in "test_masker".
            r"[A-Za-z0-9!@#$%^&*()_\-+=/\\|:;,.?~`]{20,}",
            text,
        )

        for word in words:
            if EntropyDetector.is_high_entropy(word):
                #
                # Avoid duplicates.
                #
                if any(e.value == word for e in entities):
                    continue

                entities.append(
                    SecretEntity(
                        secret_type=SecretType.UNKNOWN,
                        value=word,
                        start=text.find(word),
                        end=text.find(word) + len(word),
                        confidence=0.70,
                        severity=Severity.MEDIUM,
                        detector="Entropy",
                    )
                )

        #######################################################################
        # Risk Score
        #######################################################################
        risk = min(
            len(entities) * 15,
            100,
        )

        print("<-- Exiting SecretDetector.detect")

        return SecretDetectionResult(
            entities=entities,
            entity_count=len(entities),
            has_secrets=len(entities) > 0,
            risk_score=risk,
        )

    ###########################################################################

    @staticmethod
    def _severity(
        secret_type: SecretType,
    ) -> Severity:
        if secret_type in {
            SecretType.OPENAI_KEY,
            SecretType.AWS_SECRET_KEY,
            SecretType.PRIVATE_KEY,
        }:
            return Severity.CRITICAL

        if secret_type in {
            SecretType.GITHUB_PAT,
            SecretType.AWS_ACCESS_KEY,
        }:
            return Severity.HIGH

        if secret_type in {
            SecretType.JWT,
            SecretType.CONNECTION_STRING,
        }:
            return Severity.MEDIUM

        return Severity.LOW
    