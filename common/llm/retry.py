"""
===============================================================================
File        : retry.py
Project     : Enterprise AI Security Framework

Description
-----------
Retry helper for transient failures.

Features
--------
✓ Configurable retry count
✓ Exponential backoff
✓ Automatic logging
✓ Enterprise friendly

===============================================================================
"""

from __future__ import annotations

import time
from typing import Callable
from typing import TypeVar

from common.logger import logger

T = TypeVar("T")


class Retry:
    """
    Generic retry helper.
    Example
    retry = Retry()
    result = retry.execute(function)
    """
    def __init__(
        self,
        retries: int = 3,
        initial_delay: float = 1.0,
        multiplier: float = 2.0
    ) -> None:

        self.retries = retries
        self.initial_delay = initial_delay
        self.multiplier = multiplier

    ###########################################################################

    def execute(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        delay = self.initial_delay
        last_exception = None

        for attempt in range(1, self.retries + 1):
            try:
                logger.info(
                    "Attempt %d of %d",
                    attempt,
                    self.retries
                )

                return func(
                    *args,
                    **kwargs
                )
            except Exception as ex:
                last_exception = ex
                logger.warning(
                    "Attempt %d failed : %s",
                    attempt,
                    ex
                )

                if attempt < self.retries:
                    logger.info(
                        "Retrying in %.1f seconds...",
                        delay
                    )

                    time.sleep(delay)

                    delay *= self.multiplier

        logger.error(
            "All retry attempts failed."
        )

        raise last_exception
    