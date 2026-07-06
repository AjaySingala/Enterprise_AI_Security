"""
Embedding Provider Interface
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding import Embedding

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(
        self,
        chunk: Chunk,
    ) -> Embedding:
        """
        Generate an embedding for one chunk.
        """
        raise NotImplementedError()

    @abstractmethod
    def embed_batch(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        """
        Generate embeddings for multiple chunks.
        """
        raise NotImplementedError()
    