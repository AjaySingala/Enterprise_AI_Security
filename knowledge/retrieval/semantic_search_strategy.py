"""
===============================================================================
Semantic Search Strategy
===============================================================================
"""

from __future__ import annotations

from common.tracing.trace_decorator import trace

from knowledge.embeddings.embedding import Embedding
from knowledge.query.metadata_query import MetadataQuery
from knowledge.retrieval.search_strategy import SearchStrategy
from knowledge.vectorstores.base_vectorstore import BaseVectorStore
from knowledge.retrieval.search_result import SearchResult

###############################################################################
class SemanticSearchStrategy(SearchStrategy):
    ###########################################################################
    @trace
    def search(
        self,
        query_embedding: Embedding,
        vector_store: BaseVectorStore,
        k: int,
        metadata_query: MetadataQuery | None = None,
    ) -> list[SearchResult]:
        return vector_store.search(
            query_embedding=query_embedding,
            k=k,
            metadata_query=metadata_query,
        )
    