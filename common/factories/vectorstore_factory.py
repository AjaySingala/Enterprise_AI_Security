"""
Vector Store Factory
"""

from __future__ import annotations

from config import settings

from knowledge.vectorstores.base_vectorstore import BaseVectorStore
from knowledge.vectorstores.faiss_vectorstore import FAISSVectorStore

###############################################################################
class VectorStoreFactory:
    """
    Creates the configured Vector Store.
    """

    ###########################################################################
    @staticmethod
    def create() -> BaseVectorStore:
        provider = settings.vector_store
        match provider:
            case "faiss":
                return FAISSVectorStore()
            #
            # Future
            #
            # case "chroma":
            #     return ChromaVectorStore()
            #
            # case "azure":
            #     return AzureAISearchVectorStore()
            case _:
                raise ValueError(
                    f"Unsupported vector store: {provider}"
                )
            