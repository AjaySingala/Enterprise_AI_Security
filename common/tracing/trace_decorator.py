"""
===============================================================================
Enterprise AI Gateway (EAIG)

Trace Decorator
===============================================================================
"""

from __future__ import annotations

from functools import wraps

from common.tracing.trace_manager import trace_manager

###############################################################################
def trace(func):
    """
    Trace a function.
    """
    @wraps(func)
    def wrapper(
        *args,
        **kwargs,
    ):
        start = trace_manager.enter(
            func.__qualname__,
        )

        try:
            return func(
                *args,
                **kwargs,
            )
        finally:
            trace_manager.exit(
                func.__qualname__,
                start,
            )

    return wrapper
