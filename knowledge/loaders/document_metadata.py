from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

@dataclass(slots=True,)
class DocumentMetadata:
    """
    Metadata associated with a document or chunk.
    """
    # Source.
    source: str = ""
    filename: str = ""
    extension: str = ""

    # Document information.
    page: int = 0
    section: str = ""
    author: str = ""
    version: str = ""
    language: str = "en"

    # Business metadata.
    department: str = ""
    country: str = ""
    classification: str = ""

    # Processing.
    loader: str = ""
    page_count: int = 0
    tags: list[str] = field(
        default_factory=list,
    )

    # Extensibility.
    custom: dict[str, str] = field(
        default_factory=dict,
    )

    created_at: datetime | None = None
    modified_at: datetime | None = None
    
