"""
Retriever

Performs semantic retrieval using the configured vector store.
"""

from __future__ import annotations

from common.tracing.trace_decorator import trace

from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.vectorstores.base_vectorstore import BaseVectorStore
from knowledge.chunking.chunk import Chunk
from knowledge.vectorstores.search_result import SearchResult
from knowledge.query.metadata_query import MetadataQuery

class Retriever:
    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        vector_store: BaseVectorStore,
    ):
        self.embedding_engine = embedding_engine
        self.vector_store = vector_store
    
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
        return self.vector_store.search(
            query_embedding=query_embedding,
            k=k,
            metadata_query=metadata_query,
        )
        