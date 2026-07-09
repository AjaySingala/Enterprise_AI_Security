"""
Retriever

Performs semantic retrieval using the configured vector store.
"""

from __future__ import annotations

from common.tracing.trace_decorator import trace

from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.vectorstores.base_vectorstore import BaseVectorStore
from knowledge.chunking.chunk import Chunk
from knowledge.retrieval.search_result import SearchResult
from knowledge.query.metadata_query import MetadataQuery
from knowledge.retrieval.search_strategy import SearchStrategy

class Retriever:
    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        vector_store: BaseVectorStore,
        strategy: SearchStrategy,
    ):
        self.embedding_engine = embedding_engine
        self.vector_store = vector_store
        self.strategy = strategy
    
    ###########################################################################
    @trace
    def retrieve(
        self,
        query: str,
        k: int = 5,
        metadata_query: MetadataQuery | None = None,
    ) -> list[SearchResult]:
        #
        # Convert the question into a temporary Chunk.
        #
        query_chunk = Chunk(
            document_id="QUERY",
            content=query,
            chunk_index=0,
        )

        #
        # Embed the question.
        #
        query_embedding = self.embedding_engine.embed(
            query_chunk,
        )

        #
        # Search.
        #
        return self.strategy.search(
            query_embedding=query_embedding,
            k=k,
            metadata_query=metadata_query,
            vector_store=self.vector_store,
        )
        