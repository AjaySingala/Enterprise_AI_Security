"""
===============================================================================
Metadata Query
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from knowledge.query.metadata_filter import (
    MetadataFilter,
)

###############################################################################
@dataclass(slots=True)
class MetadataQuery:
    """
    Collection of metadata filters.

    Initially supports AND semantics.
    """
    filters: list[MetadataFilter] = field(
        default_factory=list
    )

    ###########################################################################
    def add(
        self,
        field: str,
        value: object,
    ) -> None:
        self.filters.append(
            MetadataFilter(
                field=field,
                value=value,
            )
        )

    ###########################################################################
    @property
    def empty(self) -> bool:
        return len(self.filters) == 0
    
    # Returns something like this:
    #   department eq HR
    #   country eq India
    # instead of a raw dataclass representation.
    def __str__(self):
        return (
            f"{self.field} "
            f"{self.operator.value} "
            f"{self.value}"
        )
    