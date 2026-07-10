"""
Base Vector Store

Abstract interface for all vector databases.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

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

    ###############################################################################
    @abstractmethod
    def save(
        self,
        folder: str | Path,
    ) -> None:
        """
        Persist the vector store.
        """
        raise NotImplementedError


    ###############################################################################
    @abstractmethod
    def load(
        self,
        folder: str | Path,
    ) -> None:
        """
        Load a persisted vector store.
        """
        raise NotImplementedError
    