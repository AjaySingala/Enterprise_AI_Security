"""
===============================================================================
File        : provider.py
Project     : Enterprise AI Gateway (EAIG)

Description
-----------
Defines the supported LLM providers.

The rest of the application should never directly reference provider names.
Instead, it should use this enumeration.

Benefits
--------
- Strong typing
- Avoids hard-coded strings
- Easy to extend
===============================================================================
"""

from __future__ import annotations
from enum import Enum

class LLMProvider(str, Enum):
    """
    Supported LLM providers.
    """
    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"
    ANTHROPIC = "Anthropic"
    GOOGLE = "Google Gemini"
    OLLAMA = "Ollama"
    LOCAL = "Local Model"
    UNKNOWN = "Unknown"
