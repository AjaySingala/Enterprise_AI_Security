"""
===============================================================================
PII Detector

Enterprise AI Security Framework

This detector combines:

1. Enterprise Regex Detection
2. Microsoft Presidio Detection
3. Result Deduplication
4. Risk Scoring

Text
 │
 ├── Enterprise Regex Rules
 │
 ├── Microsoft Presidio
 │
 ├── Merge Results
 │
 ├── Remove Duplicates
 │
 ├── Calculate Risk
 │
 └── Return PIIDetectionResult
===============================================================================
"""

from __future__ import annotations

import re

from presidio_analyzer import AnalyzerEngine

from security.pii.patterns import PATTERNS
from security.pii.types import (
    PIIDetectionResult,
    PIIEntity,
    PIIType,
    RiskLevel,
)

class PIIDetector:
    """
    Enterprise PII detector.
    """

    ###########################################################################
    def __init__(self) -> None:
        print("--> Entering PIIDetector.__init__")

        # The first time this line executes, it takes a lot of time.
        # Presidio loads:
        # - NLP engine
        # - spaCy
        # - Named Entity Recognition (NER) models
        # - Recognizers
        # - Pattern registry
        # - en-core-web-lg package - large English NLP model from spaCy.
        # If the required spaCy model isn't installed, it may even try to download or 
        # initialize resources depending on your environment.
        self.analyzer = AnalyzerEngine()

        print("<-- Exiting PIIDetector.__init__")

    ###########################################################################
    def detect(
        self,
        text: str,
    ) -> PIIDetectionResult:
        print("--> Entering PIIDetector.detect")

        entities: list[PIIEntity] = []

        #######################################################################
        # Enterprise Regex Detection
        #######################################################################
        for entity_type, pattern in PATTERNS.items():
            for match in re.finditer(pattern, text):
                entities.append(
                    PIIEntity(
                        entity_type=entity_type,
                        value=match.group(),
                        start=match.start(),
                        end=match.end(),
                        confidence=1.0,
                        detector="Regex",
                    )
                )

        #######################################################################
        # Presidio Detection
        #######################################################################
        presidio_results = self.analyzer.analyze(
            text=text,
            language="en",
        )

        mapping = {
            "PERSON": PIIType.PERSON,
            "EMAIL_ADDRESS": PIIType.EMAIL,
            "PHONE_NUMBER": PIIType.PHONE,
            "CREDIT_CARD": PIIType.CREDIT_CARD,
            "IP_ADDRESS": PIIType.IP_ADDRESS,
            "URL": PIIType.URL,
        }

        for result in presidio_results:
            entity = mapping.get(
                result.entity_type,
                PIIType.UNKNOWN,
            )

            entities.append(
                PIIEntity(
                    entity_type=entity,
                    value=text[result.start:result.end],
                    start=result.start,
                    end=result.end,
                    confidence=result.score,
                    detector="Presidio",
                )
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
            len(entities) * 10,
            100,
        )

        if risk_score == 0:
            risk = RiskLevel.LOW
        elif risk_score < 40:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.HIGH

        print("<-- Exiting PIIDetector.detect")

        return PIIDetectionResult(
            entities=entities,
            entity_count=len(entities),
            risk_score=risk_score,
            risk_level=risk,
            has_pii=len(entities) > 0,
        )
    