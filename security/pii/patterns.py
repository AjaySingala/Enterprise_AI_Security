"""
===============================================================================
Enterprise Regex Patterns
Detection Rules.

These are additional patterns beyond what Presidio provides.

These patterns are intentionally kept separate so that
they can easily be extended.
===============================================================================
"""

from __future__ import annotations

from security.pii.types import PIIType

###############################################################################
# Enterprise Regex Rules
###############################################################################
PATTERNS = {
    #
    # India
    #

    PIIType.PAN:
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

    PIIType.AADHAAR:
        r"\b[2-9][0-9]{3}\s?[0-9]{4}\s?[0-9]{4}\b",

    PIIType.UPI:
        r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b",

    PIIType.IFSC:
        r"\b[A-Z]{4}0[A-Z0-9]{6}\b",

    #
    # OpenAI
    #
    PIIType.OPENAI_KEY:
        r"\bsk-[A-Za-z0-9_\-]{20,}\b",

    #
    # GitHub
    #
    PIIType.GITHUB_TOKEN:
        r"\bgh[pousr]_[A-Za-z0-9]{36,}\b",

    #
    # AWS
    #
    PIIType.AWS_ACCESS_KEY:
        r"\bAKIA[0-9A-Z]{16}\b",

    #
    # JWT
    #
    PIIType.JWT:
        r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+",
}
