"""
Knowledge Pipeline
"""

from __future__ import annotations

from time import perf_counter

from common.llm.client import LLM
from common.tracing.trace_decorator import trace

from knowledge.pipelines.knowledge_response import KnowledgeResponse
from knowledge.pipelines.prompt import Prompt
from knowledge.pipelines.prompt_builder import PromptBuilder
from knowledge.retrieval.retriever import Retriever

class KnowledgePipeline:
    ###########################################################################
    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm: LLM,
    ):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm

    ###########################################################################
    @trace
    def ask(
        self,
        query: str,
        k: int = 5,
    ) -> KnowledgeResponse:
        start = perf_counter()

        #
        # Retrieve relevant chunks.
        #
        search_results = self.retriever.retrieve(
            query=query,
            k=k,
        )

        #
        # Build prompt.
        #
        prompt: Prompt = self.prompt_builder.build_prompt(
            query=query,
            results=search_results,
        )

        #
        # Ask the LLM.
        #
        llm_response = self.llm.generate(
            system_prompt=prompt.system_prompt,
            user_prompt=prompt.user_prompt,
        )

        elapsed = (perf_counter() - start) * 1000

        return KnowledgeResponse(
            prompt=prompt,
            llm_response=llm_response,
            search_results=search_results,
            elapsed_ms=elapsed,
        )
    