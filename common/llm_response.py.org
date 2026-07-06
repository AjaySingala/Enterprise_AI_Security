"""
Structured response returned by the Enterprise LLM wrapper.

Compatible with:
    openai==2.44.0
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class LLMResponse:
    """
    Standard response object returned by the LLM wrapper.
    """
    text: str
    model: str
    request_id: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    elapsed_time: float
    raw_response: object
