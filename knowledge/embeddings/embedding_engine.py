"""
Embedding Engine

Facade over embedding providers.
"""

from __future__ import annotations

from openai import OpenAI

from config.config import settings

from common.logger import get_logger
from common.tracing.trace_decorator import trace

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding import Embedding

logger = get_logger(__name__)

class EmbeddingEngine:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.api_key,
        )

        self.model = settings.text_embedding_model

    ##########################################################################
    @trace
    def embed_individual(
        self,
        chunk: Chunk,
    ) -> Embedding:
        response = self.client.embeddings.create(
            model=self.model,
            input=chunk.content,
        )

        item = response.data[0]

        usage = getattr(
            response,
            "usage",
            None,
        )

        return Embedding(
            chunk_id=chunk.chunk_id,
            vector=item.embedding,
            model=self.model,
            dimensions=len(item.embedding),
            input_tokens=(
                usage.prompt_tokens
                if usage
                else 0
            ),
        )

    @trace
    def embed(
        self,
        chunk: Chunk,
    ) -> Embedding:
        return self.embed_batch([chunk])[0]

    @trace
    def embed_batch(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        if not chunks:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=[chunk.content for chunk in chunks],
        )

        usage = getattr(response, "usage", None)
        embeddings: list[Embedding] = []

        for chunk, item in zip(chunks, response.data):
            embeddings.append(
                Embedding(
                    chunk_id=chunk.chunk_id,
                    vector=item.embedding,
                    model=self.model,
                    dimensions=len(item.embedding),
                    input_tokens=(
                        usage.prompt_tokens
                        if usage
                        else 0
                    ),
                )
            )

        return embeddings
    