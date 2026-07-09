"""
Don't return tuples.
Don't return raw FAISS indices.
Create a model.

Why SearchResult?

Instead of returning:
[(0.94, embedding)]

We return:
SearchResult(
    embedding=...,
    score=0.94,
    rank=1,
    ...
)
"""
from __future__ import annotations

from dataclasses import dataclass

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding import Embedding
from knowledge.vectorstores.retrieval_method import RetrievalMethod

###############################################################################
@dataclass(slots=True)
class SearchResult:
    """
    Represents one retrieved search result.
    Independent of the underlying retrieval provider.
    """
    #
    # Always available
    #
    chunk: Chunk
    score: float
    rank: int
    source: RetrievalMethod

    #
    # Optional
    #
    embedding: Embedding | None = None
