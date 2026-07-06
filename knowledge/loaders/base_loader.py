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

from pathlib import Path

from knowledge.loaders.document import Document

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
    