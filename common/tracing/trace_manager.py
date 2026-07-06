"""
===============================================================================
Enterprise AI Gateway (EAIG)

Trace Manager

1) ENABLE_TRACING=False
↓
No tracing
No logger
No timing
Almost zero overhead

2) ENABLE_TRACING=True and TRACE_OUTPUT=none
↓
Collect timing
Future LangSmith
Future OpenTelemetry
No console output

3) ENABLE_TRACING=True and TRACE_OUTPUT=console
↓
Console/file logging
===============================================================================
"""

from __future__ import annotations

import time

from common.logger import get_logger
from common.tracing.trace_context import _trace_depth
from config.config import settings
from common.tracing.trace_constants import TraceOutput

logger = get_logger(__name__)

###############################################################################
class TraceManager:
    ###########################################################################
    def enter(
        self,
        name: str,
    ) -> float:
        if not settings.enable_tracing:
            return None

        start = time.perf_counter()
        depth = _trace_depth.get()
        indent = "    " * depth

        match settings.trace_output:
            case TraceOutput.NONE:
                pass
            case TraceOutput.CONSOLE:
                print(
                    f"{indent}▶ ENTER {name}",
                )
            case TraceOutput.LOGGER:
                logger.info(
                    "%s▶ ENTER %s",
                    indent,
                    name,
                )
            case TraceOutput.LANGSMITH:
                #
                # Future
                #
                pass
            case TraceOutput.OPENTELEMETRY:
                #
                # Future
                #
                pass

        _trace_depth.set(
            depth + 1,
        )

        return start

    ###########################################################################
    def exit(
        self,
        name: str,
        start: float,
    ) -> None:
        if start is None:
            return

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

        match settings.trace_output:
            case TraceOutput.NONE:
                pass
            case TraceOutput.CONSOLE:
                print(
                    f"{indent}◀ EXIT {name} ({elapsed:.2f} ms)"
                )
            case TraceOutput.LOGGER:
                logger.info(
                    "%s◀ EXIT %s (%.2f ms)",
                    indent,
                    name,
                    elapsed,
                )
            case TraceOutput.LANGSMITH:
                pass
            case TraceOutput.OPENTELEMETRY:
                pass

###############################################################################
trace_manager = TraceManager()
