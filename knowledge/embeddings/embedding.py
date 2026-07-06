"""
Embedding Model

Represents a vector embedding produced for a chunk of text.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from knowledge.chunking.chunk import Chunk

@dataclass(slots=True, frozen=True)
class Embedding:
    """
    Represents a vector embedding for a Chunk.
    """
    #
    # Source
    #
    chunk: Chunk

    #
    # Vector
    #
    vector: Sequence[float]

    #
    # Metadata
    #
    model: str

    #
    # Statistics
    #
    input_tokens: int = 0
    elapsed_ms: float = 0.0

    @property
    def dimensions(self) -> int:
        return len(self.vector)

    @property
    def chunk_id(self) -> str:
        return self.chunk.chunk_id

    @property
    def document_id(self) -> str:
        return self.chunk.document_id

    @property
    def chunk_index(self) -> int:
        return self.chunk.chunk_index

    @property
    def content(self) -> str:
        return self.chunk.content