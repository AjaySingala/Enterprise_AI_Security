"""
===============================================================================
PDF Loader
===============================================================================
"""

from __future__ import annotations

from pathlib import Path
import fitz

from common.tracing.trace_decorator import trace

from knowledge.loaders.base_loader import BaseLoader
from knowledge.loaders.document import Document
from knowledge.loaders.document_metadata import DocumentMetadata

###############################################################################
class PDFLoader(BaseLoader):
    """
    Loads PDF documents.
    """
    ###########################################################################
    @trace
    def load(
        self,
        file_path: str | Path,
    ) -> Document:
        file_path = Path(file_path)

        pdf = fitz.open(file_path)
        pages: list[str] = []

        for page in pdf:
            pages.append(
                page.get_text()
            )

        text = "\n\n".join(
            pages,
        )

        metadata = DocumentMetadata()

        self.populate_common_metadata(
            file=file_path,
            metadata=metadata,
        )

        metadata.page_count = len(pages,)

        return Document(
            source=str(file_path),
            document_id=file_path.stem,
            content=text,
            metadata=metadata,
            pages=pages,
        )
    