"""
Embedding Engine

Facade over embedding providers.
"""

from __future__ import annotations

from config.config import settings

from common.tracing.trace_decorator import trace

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding import Embedding
from knowledge.embeddings.embedding_provider import EmbeddingProvider

class EmbeddingEngine:
    def __init__(
        self,
        provider: EmbeddingProvider,
    ):

        self.provider = provider

    ##########################################################################
    @trace
    def embed(
        self,
        chunk: Chunk,
    ) -> Embedding:
        return self.provider.embed(
            chunk,
        )

    @trace
    def embed_batch(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        return self.provider.embed_batch(
            chunks,
        )
    