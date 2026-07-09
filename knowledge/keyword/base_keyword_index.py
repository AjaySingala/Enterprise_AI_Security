"""
===============================================================================
Base Keyword Index
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from knowledge.chunking.chunk import Chunk
from knowledge.retrieval.search_result import SearchResult

###############################################################################
class BaseKeywordIndex(ABC):
    """
    Base class for all keyword indexes.
    """
    ###########################################################################
    @abstractmethod
    def add(
        self,
        chunks: list[Chunk],
    ) -> None:
        raise NotImplementedError

    ###########################################################################
    @abstractmethod
    def search(
        self,
        query: str,
        k: int = 5,
    ) -> list[SearchResult]:
        raise NotImplementedError

    ###########################################################################
    @abstractmethod
    def count(
        self,
    ) -> int:
        raise NotImplementedError

    ###########################################################################
    @abstractmethod
    def clear(
        self,
    ) -> None:
        raise NotImplementedError
    