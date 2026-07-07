"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Document Models

Version:
    1.1.0
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

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
