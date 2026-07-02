"""
===============================================================================
Prompt Injection LLM Classifier

This is the second stage of the detection pipeline.

Uses an LLM to classify prompts that have already gone through the
deterministic detector.

This is the second stage of the security pipeline.
===============================================================================
"""

# User Prompt
#       │
#       ▼
# Deterministic Detector
#       │
#       ▼
# LLM Classifier
#       │
#       ▼
# Decision Engine

from __future__ import annotations

from dataclasses import dataclass

from common.llm import llm
from common.prompts import PROMPT_INJECTION_SYSTEM_PROMPT
from config.config import settings

@dataclass(slots=True)
class ClassificationResult:
    """
    Result returned by the LLM classifier.
    """
    is_attack: bool
    attack_type: str
    confidence: int
    risk: str
    reason: str

class PromptInjectionClassifier:
    """
    Uses an LLM to classify suspicious prompts.
    """

    ###########################################################################
    def classify(
        self,
        prompt: str,
    ) -> ClassificationResult:
        if settings.debug:
            print("--> Entering PromptInjectionClassifier.classify")

        try:
            result = llm.generate_json(
                system_prompt=PROMPT_INJECTION_SYSTEM_PROMPT,
                user_prompt=prompt,
            )

            classification = ClassificationResult(
                is_attack=bool(
                    result.get("is_attack", False)
                ),
                attack_type=str(
                    result.get("attack_type", "Unknown")
                ),
                confidence=int(
                    result.get("confidence", 0)
                ),
                risk=str(
                    result.get("risk", "Low")
                ),
                reason=str(
                    result.get("reason", "")
                ),
            )

        except Exception as ex:
            classification = ClassificationResult(
                is_attack=True,
                attack_type="Parser Error",
                confidence=100,
                risk="High",
                reason=str(ex),
            )

        if settings.debug:
            print("<-- Exiting PromptInjectionClassifier.classify")

        return classification
    