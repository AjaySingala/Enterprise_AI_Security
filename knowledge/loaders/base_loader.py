"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Base Loader

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from datetime import datetime
from pathlib import Path

from knowledge.loaders.document import Document
from knowledge.loaders.document_metadata import DocumentMetadata

###############################################################################
# Base Loader
###############################################################################
class BaseLoader(ABC):
    """
    Base class for all document loaders.
    """

    ###########################################################################
    @abstractmethod
    def load(
        self,
        file: Path,
    ) -> Document:
        """
        Load a document.

        Returns
        -------
        Document
        """

        raise NotImplementedError
    
    def populate_common_metadata(
        self,
        file: Path,
        metadata: DocumentMetadata,
    ) -> None:
        #
        # Populate loader-specific metadata.
        #
        metadata.source = str(file)
        metadata.filename = file.name
        metadata.extension = file.suffix
        metadata.loader = self.__class__.__name__

        stat = file.stat()

        metadata.created_at = datetime.fromtimestamp(
            stat.st_birthtime,
        )

        metadata.modified_at = datetime.fromtimestamp(
            stat.st_mtime,
        )