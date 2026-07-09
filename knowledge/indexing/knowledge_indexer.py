"""
===============================================================================
Knowledge Indexer
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from common.tracing.trace_decorator import trace

from knowledge.chunking.base_chunker import BaseChunker
from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.loaders.base_loader import BaseLoader
from knowledge.loaders.document import Document
from knowledge.vectorstores.base_vectorstore import BaseVectorStore

###############################################################################
class KnowledgeIndexer:
    """
    Orchestrates the complete indexing pipeline.

        Load
            ↓
        Chunk
            ↓
        Embed
            ↓
        Store
    """
    ###############################################################################
    def __init__(
        self,
        loader: BaseLoader,
        chunker: BaseChunker,
        embedding_engine: EmbeddingEngine,
        vector_store: BaseVectorStore,
    ):
        self.loader = loader
        self.chunker = chunker
        self.embedding_engine = embedding_engine
        self.vector_store = vector_store

    ###############################################################################
    @trace
    def index_file(
        self,
        file_path: str | Path,
    ) -> int:
        """
        Index a single document.

        Returns
        -------
        int
            Number of chunks indexed.
        """
        #
        # Load
        #
        document = self.loader.load(
            file_path,
        )

        #
        # Chunk
        #
        chunks = self.chunker.chunk(
            document,
        )

        #
        # Embed
        #
        embeddings = self.embedding_engine.embed_batch(
            chunks,
        )

        #
        # Store
        #
        self.vector_store.add(
            embeddings,
        )

        return len(
            embeddings,
        )
    