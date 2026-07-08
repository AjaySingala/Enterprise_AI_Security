"""
Base Vector Store

Abstract interface for all vector databases.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from knowledge.embeddings.embedding import Embedding
from knowledge.query.metadata_query import MetadataQuery

class BaseVectorStore(ABC):
    @abstractmethod
    def add(
        self,
        embeddings: list[Embedding],
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: Embedding,
        k: int = 5,
        metadata_query: MetadataQuery | None = None,
    ):
        pass

    @abstractmethod
    def count(
        self,
    ) -> int:
        pass

    @abstractmethod
    def clear(
        self,
    ) -> None:
        pass
