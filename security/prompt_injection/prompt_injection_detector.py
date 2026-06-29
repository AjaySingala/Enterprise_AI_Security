"""
===============================================================================
Deterministic Prompt Injection Detector.

Fast, inexpensive checks that run BEFORE calling the LLM.

Feature 01

Enterprise AI Security Framework

Objective
---------
Detect common Prompt Injection attacks before invoking an LLM.

This detector performs a deterministic scan using

• keywords
• regex
• scoring

The output is later combined with an LLM classifier.

Author
------
Ajay Singala AI Security Repository
===============================================================================
"""

# User Prompt
#       │
#       ▼
# Deterministic Detector
#       │
#       ├── Safe  ─────────────► LLM
#       │
#       └── Suspicious ───────► LLM Classifier

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class DetectionResult:
    is_attack: bool
    score: int
    confidence: int
    matched_rules: list[str]
    reason: str


class PromptInjectionDetector:
    def __init__(self) -> None:
        self.rules = {

            # High Risk
            r"ignore\s+(all\s+)?previous\s+instructions": 60,
            r"forget\s+previous\s+instructions": 50,
            r"forget\s+your\s+instructions": 50,
            # r"forget\s+your\s+safety\s+rules": 60,        # Uncomment later.
            r"forget\s+safety\s+rules": 60,
            r"system\s+prompt": 50,
            r"developer\s+message": 50,
            r"hidden\s+instructions": 45,
            r"api\s*key": 60,
            r"password": 50,
            r"secret": 45,
            r"disable\s+safety": 60,
            r"disable\s+guardrails": 60,
            r"bypass\s+guardrails": 60,
            r"override\s+instructions": 60,
            r"override\s+system": 60,
            r"reveal\s+system\s+prompt": 70,

            # Medium Risk
            r"pretend\s+you\s+are": 35,
            r"act\s+as": 30,
            r"roleplay": 25,
            r"jailbreak": 60,
            r"\bdan\b": 60,
        }

    ###########################################################################
    def analyze(
        self,
        prompt: str,
    ) -> DetectionResult:
        score = 0
        matches: list[str] = []

        for pattern, weight in self.rules.items():
            if re.search(pattern, prompt, flags=re.IGNORECASE):
                score += weight
                matches.append(pattern)

        confidence = min(score, 100)
        attack = score >= 30

        if attack:
            reason = "Suspicious prompt injection patterns detected."
        else:
            reason = "Prompt appears safe."

        return DetectionResult(
            is_attack=attack,
            score=score,
            confidence=confidence,
            matched_rules=matches,
            reason=reason,
        )
    