"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Text Loader

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from common.tracing.trace_decorator import trace
from knowledge.loaders.base_loader import BaseLoader
from knowledge.loaders.document import Document

from knowledge.loaders.document_metadata import DocumentMetadata

###############################################################################
# Text Loader
###############################################################################
class TextLoader(BaseLoader):
    ###########################################################################
    @trace
    def load(
        self,
        file: Path,
        metadata: DocumentMetadata | None = None,
    ) -> Document:
        text = file.read_text(
            encoding="utf-8",
        )

        #
        # Use supplied metadata or create a default instance.
        #
        document_metadata = metadata or DocumentMetadata()

        self.populate_common_metadata(
            file,
            document_metadata,
        )

        return Document(
            source=file,
            content=text,
            metadata=document_metadata,
        )
    