"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Chunk Model

Version:
    1.1.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import uuid

###############################################################################
# Chunk
###############################################################################
@dataclass(slots=True)
class Chunk:
    document_id: str
    content: str
    chunk_index: int = 0
    # chunk_id is auto-generated.
    chunk_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def length(self) -> int:
        return len(self.content)
