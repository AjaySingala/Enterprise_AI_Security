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

###############################################################################
# Configure Logger
###############################################################################
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    ),
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

###############################################################################
# Factory
###############################################################################
def get_logger(
    name: str,
) -> logging.Logger:
    return logging.getLogger(name)
