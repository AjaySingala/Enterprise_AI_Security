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
        page_offsets: list[int] = []
        offset = 0

        for page in pdf:
            page_text = page.get_text()
            page_offsets.append(offset)
            pages.append(page_text)
            offset += len(page_text) + 2

        text = "\n\n".join(pages,)

        metadata = DocumentMetadata()

        self.populate_common_metadata(
            file=file_path,
            metadata=metadata,
        )

        metadata.page_count = len(pages,)

        return Document(
            document_id=file_path.stem,
            source=str(file_path),
            content=text,
            metadata=metadata,
            pages=pages,
            page_offsets=page_offsets,
        )
    