"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Base Chunker

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from knowledge.chunking.chunk import Chunk

###############################################################################
# Base Chunker
###############################################################################
class BaseChunker(ABC):
    """
    Base class for all chunking strategies.
    """

    @abstractmethod
    def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:
        raise NotImplementedError
    