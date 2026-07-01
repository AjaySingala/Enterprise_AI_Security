"""
===============================================================================
File        : timer.py
Project     : Enterprise AI Gateway (EAIG)

Description
-----------
Provides utilities for measuring execution time.

Features
--------
1. Context Manager
2. Decorator
3. High precision timing
4. Automatic logging
5. Optional console output

Example
-------

with Timer("Prompt Injection"):

    detector.analyze(text)

or

@measure_time
def analyze():
    ...

===============================================================================
"""

from __future__ import annotations

import time
from functools import wraps
from typing import Any
from typing import Callable

from common.logger import logger

class Timer:
    """
    Context manager used to measure execution time.
    """
    def __init__(
        self,
        operation_name: str,
        display: bool = True
    ) -> None:

        self.operation_name = operation_name
        self.display = display

        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0

    ###########################################################################
    def __enter__(self):

        logger.debug(
            "Starting timer : %s",
            self.operation_name
        )

        self.start_time = time.perf_counter()

        return self

    ###########################################################################
    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ) -> None:

        self.end_time = time.perf_counter()

        self.elapsed_time = self.end_time - self.start_time

        logger.info(
            "%s completed in %.3f seconds.",
            self.operation_name,
            self.elapsed_time
        )

        if self.display:

            print(
                f"\nExecution Time : "
                f"{self.elapsed_time:.3f} seconds"
            )


###############################################################################
# Decorator
###############################################################################
def measure_time(
    func: Callable[..., Any]
) -> Callable[..., Any]:
    """
    Decorator that measures execution time.

    Example

    @measure_time
    def analyze():
        ...
    """

    @wraps(func)
    def wrapper(
        *args,
        **kwargs
    ):

        logger.debug(
            "Entering function : %s",
            func.__name__
        )

        start = time.perf_counter()

        try:

            result = func(
                *args,
                **kwargs
            )

            return result

        finally:

            end = time.perf_counter()

            elapsed = end - start

            logger.info(
                "%s executed in %.3f seconds.",
                func.__name__,
                elapsed
            )

            print(
                f"\nExecution Time : "
                f"{elapsed:.3f} seconds"
            )

            logger.debug(
                "Leaving function : %s",
                func.__name__
            )

    return wrapper


###############################################################################
# Simple Helper
###############################################################################
def elapsed_time(
    start_time: float
) -> float:
    """
    Returns elapsed time in seconds.

    Parameters
    ----------
    start_time
        Start time returned by time.perf_counter().
    """

    return time.perf_counter() - start_time


###############################################################################
# Example
###############################################################################
if __name__ == "__main__":

    import time

    @measure_time
    def sample():

        print("Doing some work...")

        time.sleep(1.5)

    sample()

    with Timer("Context Manager Example"):

        time.sleep(2)
