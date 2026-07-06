"""
Embedding Providers
"""

from enum import StrEnum

class EmbeddingProvider(StrEnum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    VOYAGE = "voyage"
    COHERE = "cohere"
