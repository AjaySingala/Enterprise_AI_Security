"""
Prompt Builder

Builds prompts from retrieved search results.
"""

from __future__ import annotations

from common.tracing.trace_decorator import trace

from knowledge.vectorstores.search_result import SearchResult
from knowledge.pipelines.prompt import Prompt

###############################################################################
class PromptBuilder:
    @trace
    def build_prompt(
        self,
        query: str,
        results: list[SearchResult],
    ) -> Prompt:
        context_parts = []

        for result in results:
            chunk = result.embedding.chunk
            context_parts.append(
                f"""
Document : {chunk.document_id}
Chunk    : {chunk.chunk_index}

{chunk.content}
""".strip()
            )

        context = "\n\n".join(
            context_parts,
        )

        # System prompt.
        system_prompt = """
You are a helpful AI assistant.

Answer the user's question using ONLY the supplied context.

If the answer is not present,
reply exactly:

I don't know based on the supplied context.
""".strip()
        
        # User Prompt.
        user_prompt = f"""
Context
-------
{context}

Question
--------
{query}

Answer
------
""".strip()

        return Prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            full_prompt=f"{system_prompt}\n\n{user_prompt}",
        )
