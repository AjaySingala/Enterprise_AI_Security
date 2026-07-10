"""
FAISS Vector Store
"""

from __future__ import annotations

from pathlib import Path
import pickle

import faiss
import numpy as np

from common.tracing.trace_decorator import trace

from knowledge.embeddings.embedding import Embedding
from knowledge.vectorstores.base_vectorstore import BaseVectorStore
from knowledge.retrieval.search_result import SearchResult
from knowledge.query.metadata_query import MetadataQuery
from knowledge.query.filter_operator import FilterOperator
from knowledge.vectorstores.retrieval_method import RetrievalMethod

class FAISSVectorStore(BaseVectorStore):
    # When the caller requests top_k=5, FAISS actually retrieves:
    #   5 × 20 = 100
    # candidates before applying the metadata filters.
    # Why?
    # If you only retrieve exactly five vectors and then filter them, 
    # you might end up with zero results even though relevant matching documents exist
    # slightly lower in the similarity ranking. 
    # Using an oversampling multiplier gives much better recall while keeping the API unchanged.
    POST_FILTER_MULTIPLIER = 20     # The oversampling multiplier.

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
        metadata_query: MetadataQuery | None = None,
    ) -> list[SearchResult]:
        if self.index is None:
            return []

        query = np.array(
            [query_embedding.vector],
            dtype=np.float32,
        )

        candidate_count = max(
            k,
            k * self.POST_FILTER_MULTIPLIER,
        )

        candidate_count = min(
            candidate_count,
            len(self.embeddings),
        )

        distances, indices = self.index.search(
            query,
            candidate_count,
        )

        results: list[SearchResult] = []

        rank = 1

        for distance, index in zip(
            distances[0],
            indices[0],
        ):
            if index == -1:
                continue

            embedding = self.embeddings[index]

            if not self._matches(
                embedding,
                metadata_query,
            ):
                continue

            results.append(
                SearchResult(
                    chunk=embedding.chunk,
                    embedding=embedding,
                    score=float(distance),
                    rank=rank,
                    source=RetrievalMethod.SEMANTIC,
                )
            )

            rank += 1

            if len(results) >= k:
                break

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

    def _matches(
        self,
        embedding: Embedding,
        metadata_query: MetadataQuery | None,
    ) -> bool:
        if (
            metadata_query is None
            or metadata_query.empty
        ):
            return True

        metadata = embedding.chunk.metadata

        for metadata_filter in metadata_query.filters:
            value = getattr(
                metadata,
                metadata_filter.field,
                None,
            )

            if metadata_filter.operator != FilterOperator.EQ:
                raise NotImplementedError(
                    f"{metadata_filter.operator} not yet supported."
                )

            if value != metadata_filter.value:
                return False

        return True
    
    ###############################################################################
    @trace
    def save(
        self,
        folder: str | Path,
    ) -> None:
        """
        Persist the FAISS index and embeddings.
        """
        folder = Path(folder)

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        #
        # Save FAISS index.
        #
        faiss.write_index(
            self.index,
            str(folder / "faiss.index"),
        )

        #
        # Save embeddings.
        #
        with open(
            folder / "embeddings.pkl",
            "wb",
        ) as file:
            pickle.dump(
                self.embeddings,
                file,
            )

    ###############################################################################
    @trace
    def load(
        self,
        folder: str | Path,
    ) -> None:
        """
        Load a persisted FAISS index.
        """
        folder = Path(folder)

        #
        # Load FAISS index.
        #
        self.index = faiss.read_index(
            str(folder / "faiss.index"),
        )

        #
        # Load embeddings.
        #
        with open(
            folder / "embeddings.pkl",
            "rb",
        ) as file:
            self.embeddings = pickle.load(
                file,
            )
