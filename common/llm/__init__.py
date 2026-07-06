"""
===============================================================================
Enterprise AI Gateway (EAIG)

LLM Common

Version:
    1.0.0
===============================================================================
"""
from .client import LLM
from .response import LLMResponse

__all__ = [
    "LLM",
    "LLMResponse",
]
