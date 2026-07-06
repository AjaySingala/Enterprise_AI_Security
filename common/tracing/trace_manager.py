"""
===============================================================================
Enterprise AI Gateway (EAIG)

Trace Manager
===============================================================================
"""

from __future__ import annotations

import time

from common.logger import get_logger
from common.tracing.trace_context import _trace_depth

logger = get_logger(__name__)

###############################################################################
class TraceManager:
    ###########################################################################
    def enter(
        self,
        name: str,
    ) -> float:
        depth = _trace_depth.get()
        indent = "    " * depth
        logger.info(
            "%s▶ ENTER %s",
            indent,
            name,
        )

        _trace_depth.set(
            depth + 1,
        )

        return time.perf_counter()

    ###########################################################################
    def exit(
        self,
        name: str,
        start: float,
    ) -> None:
        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        depth = max(
            0,
            _trace_depth.get() - 1,
        )

        _trace_depth.set(
            depth,
        )

        indent = "    " * depth
        logger.info(
            "%s◀ EXIT %s (%.2f ms)",
            indent,
            name,
            elapsed,
        )


###############################################################################
trace_manager = TraceManager()
