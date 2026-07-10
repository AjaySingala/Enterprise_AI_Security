"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Document Models

Version:
    1.1.0

Notes:
- When a new property is added, rebuild the index and test with:
python -m applications.rag.build_index
python -m applications.rag.rag_console
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
import uuid

from knowledge.loaders.document_metadata import DocumentMetadata

###############################################################################
# Document
###############################################################################
@dataclass(slots=True)
class Document:
    source: Path
    content: str
    document_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    metadata: DocumentMetadata = field(
        default_factory=DocumentMetadata,
    )

    pages: list[str] = field(
        default_factory=list,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    page_offsets: list[int] = field(
        default_factory=list,
    )
