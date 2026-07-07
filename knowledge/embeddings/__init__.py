"""
===============================================================================
Enterprise AI Gateway (EAIG)

KB Embeddings

Version:
    1.0.0
===============================================================================
"""
from .embedding import Embedding
from .embedding_provider import EmbeddingProvider

__all__ = [
    "Embedding",
    "EmbeddingProvider",
]
