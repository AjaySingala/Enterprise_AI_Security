"""
===============================================================================
Search Source
===============================================================================
"""
from __future__ import annotations

from enum import Enum

###############################################################################
class RetrievalMethod(str, Enum):
    """
    Indicates which search provider produced the result.
    """
    SEMANTIC = "SEMANTIC"
    LEXICAL = "LEXICAL"
    HYBRID = "HYBRID"
    GRAPH = "GRAPH"
    SQL = "SQL"
    MEMORY = "MEMORY"
    AZURE = "AZURE"
