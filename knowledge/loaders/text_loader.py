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

from knowledge.loaders.base_loader import BaseLoader
from knowledge.loaders.document import Document

###############################################################################
# Text Loader
###############################################################################
class TextLoader(BaseLoader):
    ###########################################################################
    def load(
        self,
        file: Path,
    ) -> Document:
        text = file.read_text(
            encoding="utf-8",
        )

        return Document(
            source=file,
            content=text,
            metadata={
                "loader": "TextLoader",
                "extension": file.suffix,
                "filename": file.name,
            },
        )
    