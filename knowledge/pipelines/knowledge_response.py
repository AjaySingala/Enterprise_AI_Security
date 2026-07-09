"""
Knowledge Response
"""

from __future__ import annotations

from dataclasses import dataclass

from common.llm.response import LLMResponse
from knowledge.pipelines.prompt import Prompt
from knowledge.retrieval.search_result import SearchResult

@dataclass(
    slots=True,
    frozen=True,
)
class KnowledgeResponse:
    """
    Response returned by the Knowledge Pipeline.
    """
    prompt: Prompt
    llm_response: LLMResponse
    search_results: list[SearchResult]
    elapsed_ms: float = 0.0
