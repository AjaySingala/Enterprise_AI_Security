"""
===============================================================================
Enterprise AI Gateway (EAIG)

Enterprise Logger

Version:
    1.0.0

Python:
    3.13.11

Usage:
Instead of:
--------
print("--> Entering SecretDetector.detect")

print("Prompt Injection detected.")

print(exception)

Do this:
--------
from common.logger import get_logger
logger = get_logger(__name__)
logger.info("Entering SecretDetector.detect")

logger.warning("Prompt injection detected.")

logger.exception("Unexpected error")

===============================================================================
"""

from __future__ import annotations

import logging
import sys

from config.config import settings
from pathlib import Path

###############################################################################
# Configure Logger
###############################################################################
logger = logging.getLogger()
logger.setLevel(settings.log_level)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)

logger.handlers.clear()

if settings.log_to_console:
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

if settings.log_to_file:
    Path(settings.log_folder).mkdir(
        exist_ok=True,
    )
    file = logging.FileHandler(
        Path(settings.log_folder) / settings.log_filename,
        encoding="utf-8",
    )

    file.setFormatter(formatter)
    logger.addHandler(file)

###############################################################################
# Factory
###############################################################################
def get_logger(name: str):
    return logging.getLogger(name)
