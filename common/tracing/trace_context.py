"""
===============================================================================
Enterprise AI Gateway (EAIG)

Tracing Context

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from contextvars import ContextVar

###############################################################################
_trace_depth: ContextVar[int] = ContextVar(
    "trace_depth",
    default=0,
)
