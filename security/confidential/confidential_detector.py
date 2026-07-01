"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Confidential Data Detection

File:
    detector.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Detects organization-specific confidential information using
dictionary-based matching.

Future versions may also use:

1. Regex
2. LLM Classification
3. ML Classifiers
===============================================================================
"""

from __future__ import annotations

from security.confidential.confidential_patterns import PATTERNS
from security.confidential.confidential_types import (
    ConfidentialDetectionResult,
    ConfidentialEntity,
    ConfidentialType,
    RiskLevel,
)

class ConfidentialDetector:
    """
    Enterprise Confidential Data Detector.
    """
    ###########################################################################
    def __init__(self) -> None:
        print("--> Entering ConfidentialDetector.__init__")
        print("<-- Exiting ConfidentialDetector.__init__")

    ###########################################################################
    def detect(
        self,
        text: str,
    ) -> ConfidentialDetectionResult:
        print("--> Entering ConfidentialDetector.detect")

        entities: list[ConfidentialEntity] = []
        text_lower = text.lower()

        #######################################################################
        # Dictionary Detection
        #######################################################################
        for entity_type, keywords in PATTERNS.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                start = text_lower.find(keyword_lower)

                while start != -1:
                    end = start + len(keyword)
                    entities.append(
                        ConfidentialEntity(
                            entity_type=entity_type,
                            value=text[start:end],
                            start=start,
                            end=end,
                            confidence=1.0,
                            risk=self._risk(entity_type),
                            detector="Dictionary",
                        )
                    )

                    start = text_lower.find(
                        keyword_lower,
                        end,
                    )

        #######################################################################
        # Remove duplicates
        #######################################################################
        unique = {}
        for entity in entities:
            key = (
                entity.start,
                entity.end,
                entity.entity_type,
            )

            unique[key] = entity

        entities = sorted(
            unique.values(),
            key=lambda x: x.start,
        )

        #######################################################################
        # Risk Score
        #######################################################################
        risk_score = min(
            len(entities) * 20,
            100,
        )

        print("<-- Exiting ConfidentialDetector.detect")

        return ConfidentialDetectionResult(
            entities=entities,
            entity_count=len(entities),
            risk_score=risk_score,
            has_confidential_data=len(entities) > 0,
        )

    ###########################################################################
    @staticmethod
    def _risk(
        entity_type: ConfidentialType,
    ) -> RiskLevel:
        if entity_type in {
            ConfidentialType.STRATEGY,
            ConfidentialType.FINANCIAL,
        }:
            return RiskLevel.CRITICAL

        if entity_type in {
            ConfidentialType.PROJECT,
            ConfidentialType.ROADMAP,
        }:
            return RiskLevel.HIGH

        return RiskLevel.MEDIUM
    