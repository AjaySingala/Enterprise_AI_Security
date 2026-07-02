"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Secret Detection

File:
    entropy.py

Version:
    1.0.0

Python:
    3.13.11


Input
   │
   ▼
Regex Detector
   │
   ▼
Entropy Detector
   │
   ▼
Context Detector
   │
   ▼
Risk Scoring
   │
   ▼
Masker
   │
   ▼
Engine
   │
   ▼
Demo
    
Description
-----------
Calculates Shannon Entropy.

High entropy strings are often API keys, passwords, tokens and secrets.

Many secret scanners don't rely solely on regex. 
They also look for high-entropy strings—random-looking values that may be credentials
even if they don't match a known format.

For example:
a8K#vP92LmQx7RzTn4YhUc5W

It doesn't match any regex, but it's suspicious because it has the characteristics of a generated secret.
===============================================================================
"""

from __future__ import annotations

import math
from config.config import settings

class EntropyDetector:
    """
    Shannon Entropy Calculator.
    """
    ###########################################################################
    @staticmethod
    def calculate(
        text: str,
    ) -> float:
        if settings.debug:
            print("--> Entering EntropyDetector.calculate")

        if not text:
            return 0.0

        length = len(text)
        frequencies = {}

        for ch in text:
            frequencies[ch] = frequencies.get(ch, 0) + 1

        entropy = 0.0

        for count in frequencies.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        if settings.debug:
            print("<-- Exiting EntropyDetector.calculate")

        return entropy

    ###########################################################################
    @staticmethod
    def is_high_entropy(
        text: str,
        threshold: float = 4.0,
        min_length: int = 20,
    ) -> bool:
        if settings.debug:
            print("--> Entering EntropyDetector.is_high_entropy")

        #
        # Ignore short strings.
        #
        if len(text) < min_length:
            if settings.debug:
                print("<-- Exiting EntropyDetector.is_high_entropy")
            return False

        entropy = EntropyDetector.calculate(text)

        if settings.debug:
            print(f"Entropy : {entropy:.2f}")

        result = entropy >= threshold

        if settings.debug:
            print("<-- Exiting EntropyDetector.is_high_entropy")

        return result
