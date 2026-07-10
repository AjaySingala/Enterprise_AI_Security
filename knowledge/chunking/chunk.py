"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Chunk Model

Version:
    1.1.0

Python:
    3.13.11

Notes:
- When a new property is added, rebuild the index and test with:
python -m applications.rag.build_index
python -m applications.rag.rag_console
===============================================================================
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import uuid

from knowledge.loaders.document_metadata import DocumentMetadata

###############################################################################
# Chunk
###############################################################################
@dataclass(slots=True, frozen=True)
class Chunk:
    document_id: str
    content: str
    chunk_index: int = 0
    # chunk_id is auto-generated.
    chunk_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    metadata: DocumentMetadata = field(
        default_factory=DocumentMetadata,
    )
    page_number: int | None = None

    @property
    def length(self) -> int:
        return len(self.content)
