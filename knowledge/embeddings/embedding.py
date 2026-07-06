"""
Embedding Model

Represents a vector embedding produced for a chunk of text.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

@dataclass(slots=True)
class Embedding:
    #
    # Source
    #
    chunk_id: str

    #
    # Vector
    #
    vector: Sequence[float]

    #
    # Metadata
    #
    model: str
    dimensions: int

    #
    # Statistics
    #
    input_tokens: int = 0
