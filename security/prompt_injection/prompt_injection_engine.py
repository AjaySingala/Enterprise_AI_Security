"""
===============================================================================
Prompt Injection Engine

This module orchestrates the complete prompt injection detection pipeline.
Feature 01

Combines

1. Deterministic Detection
2. LLM Classification
3. Decision Engine

Enterprise Workflow/Pipeline:

User Prompt
      │
      ▼
Deterministic Detector
      │
      ├── Safe ───────────────► ALLOW
      │
      └── Suspicious
              │
              ▼
      LLM Classifier
              │
              ▼
        Decision Engine
              │
              ▼
 ALLOW / REVIEW / BLOCK

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from config.config import settings

from security.prompt_injection.prompt_injection_detector import (
    PromptInjectionDetector,
)

from security.prompt_injection.prompt_injection_classifier import (
    PromptInjectionClassifier,
)

###############################################################################
# Decision Enum
###############################################################################
class Decision(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"

###############################################################################
# Final Result
###############################################################################
@dataclass(slots=True)
class EngineResult:
    decision: Decision
    confidence: int
    reason: str
    detector_score: int
    detector_matches: list[str]
    llm_used: bool
    llm_attack_type: str
    llm_risk: str


###############################################################################
# Engine
###############################################################################
class PromptInjectionEngine:
    """
    Enterprise Prompt Injection Engine.
    """
    def __init__(self) -> None:
        if settings.debug:
            print("--> Entering PromptInjectionEngine.__init__")

        self.detector = PromptInjectionDetector()
        self.classifier = PromptInjectionClassifier()

        #
        # Tunable thresholds
        # 0–14 → Clearly safe
        # 15–79 → Needs LLM classification
        # 80+ → Almost certainly malicious
        #
        self.allow_threshold = 15
        self.review_threshold = 80

        if settings.debug:
            print("<-- Exiting PromptInjectionEngine.__init__")

    ###########################################################################
    def analyze(
        self,
        prompt: str,
    ) -> EngineResult:
        if settings.debug:
            print("--> Entering PromptInjectionEngine.analyze")

        detector_result = self.detector.analyze(prompt)

        #
        # Completely safe
        #
        if detector_result.score < self.allow_threshold:
            print("Prompt considered SAFE. LLM skipped.")
            if settings.debug:
                print("<-- Exiting PromptInjectionEngine.analyze")

            return EngineResult(
                decision=Decision.ALLOW,
                confidence=100,
                reason="No suspicious prompt injection patterns detected.",
                detector_score=detector_result.score,
                detector_matches=detector_result.matched_rules,
                llm_used=False,
                llm_attack_type="None",
                llm_risk="Low",
            )

        #
        # Run the LLM classifier
        #
        llm_result = self.classifier.classify(prompt)

        #
        # Decision Logic
        #
        if llm_result.is_attack:
            if llm_result.confidence >= self.review_threshold:
                decision = Decision.BLOCK
            else:
                decision = Decision.REVIEW
        else:
            decision = Decision.ALLOW

        if settings.debug:
            print("<-- Exiting PromptInjectionEngine.analyze")

        return EngineResult(
            decision=decision,
            confidence=llm_result.confidence,
            reason=llm_result.reason,
            detector_score=detector_result.score,
            detector_matches=detector_result.matched_rules,
            llm_used=True,
            llm_attack_type=llm_result.attack_type,
            llm_risk=llm_result.risk,
        )
    