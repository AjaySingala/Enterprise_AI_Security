"""
===============================================================================
Metadata Filter
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from knowledge.query.filter_operator import (
    FilterOperator,
)

###############################################################################
@dataclass(slots=True)
class MetadataFilter:
    """
    Represents one metadata filter.
    Example
        department == HR
        country == India
    """

    field: str
    value: object
    operator: FilterOperator = (
        FilterOperator.EQ
    )
