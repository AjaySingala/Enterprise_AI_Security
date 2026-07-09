"""
===============================================================================
Search Strategy
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from knowledge.embeddings.embedding import Embedding
from knowledge.query.metadata_query import MetadataQuery
from knowledge.vectorstores.base_vectorstore import BaseVectorStore
from knowledge.retrieval.search_result import SearchResult

###############################################################################
class SearchStrategy(ABC):
    """
    Base class for all retrieval/search strategies.
    """
    ###########################################################################
    @abstractmethod
    def search(
        self,
        query_embedding: Embedding,
        vector_store: BaseVectorStore,
        k: int,
        metadata_query: MetadataQuery | None = None,
    ) -> list[SearchResult]:
        """
        Perform retrieval.
        """
        raise NotImplementedError
    