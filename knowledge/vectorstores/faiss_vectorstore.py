"""
FAISS Vector Store
"""

from __future__ import annotations

import faiss
import numpy as np

from common.tracing.trace_decorator import trace

from knowledge.embeddings.embedding import Embedding
from knowledge.vectorstores.base_vectorstore import BaseVectorStore
from knowledge.vectorstores.search_result import SearchResult

class FAISSVectorStore(BaseVectorStore):
    ##########################################################################
    def __init__(self):
        self.index = None

        #
        # Keep the original Embedding objects
        #
        self.embeddings: list[Embedding] = []

    ##########################################################################
    @trace
    def add(
        self,
        embeddings: list[Embedding],
    ) -> None:
        if not embeddings:
            return

        #
        # First insert
        #
        if self.index is None:
            dimension = embeddings[0].dimensions
            
            # faiss.IndexFlatL2: This uses Euclidean distance, not Cosine similarity.
            # For a production RAG system, recommend:
            # - Normalize every embedding to unit length.
            # - Use IndexFlatIP (Inner Product).
            # That makes:
            #   Inner Product == Cosine Similarity
            # for normalized vectors, which is generally a better choice for semantic search.  
            self.index = faiss.IndexFlatL2(
                dimension,
            )

        vectors = np.array(
            [e.vector for e in embeddings],
            dtype=np.float32,
        )

        self.index.add(
            vectors,
        )

        self.embeddings.extend(
            embeddings,
        )

    ##########################################################################
    @trace
    def search(
        self,
        query_embedding: Embedding,
        k: int = 5,
    ) -> list[SearchResult]:
        if self.index is None:
            return []

        query = np.array(
            [query_embedding.vector],
            dtype=np.float32,
        )

        distances, indices = self.index.search(
            query,
            k,
        )

        results: list[SearchResult] = []

        for rank, (distance, index) in enumerate(
            zip(
                distances[0],
                indices[0],
            ),
            start=1,
        ):

            if index == -1:
                continue

            results.append(
                SearchResult(
                    embedding=self.embeddings[index],
                    score=float(distance),
                    rank=rank,
                )
            )

        return results

    ##########################################################################
    def count(
        self,
    ) -> int:
        return len(
            self.embeddings,
        )

    ##########################################################################
    def clear(
        self,
    ) -> None:
        self.index = None
        self.embeddings.clear()
