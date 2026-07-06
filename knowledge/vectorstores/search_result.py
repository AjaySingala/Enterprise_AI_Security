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
)
"""
from dataclasses import dataclass

from knowledge.embeddings.embedding import Embedding

@dataclass(slots=True)
class SearchResult:
    embedding: Embedding
    score: float
    rank: int
