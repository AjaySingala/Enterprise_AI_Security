"""
===============================================================================
Enterprise AI Gateway (EAIG)

Enterprise Logger

Version:
    1.1.0

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
from pathlib import Path

from config.config import settings

###############################################################################
_configured = False
###############################################################################

def _configure() -> None:
    global _configured
    if _configured:
        return

    root = logging.getLogger()
    root.handlers.clear()
    level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    root.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    #
    # Console
    #
    if settings.log_to_console:
        console = logging.StreamHandler(
            sys.stdout,
        )

        console.setFormatter(
            formatter,
        )

        root.addHandler(
            console,
        )

    #
    # File
    #
    if settings.log_to_file:
        folder = Path(
            settings.log_folder,
        )

        folder.mkdir(
            exist_ok=True,
        )

        file = logging.FileHandler(
            folder / settings.log_filename,
            encoding="utf-8",
        )

        file.setFormatter(
            formatter,
        )

        root.addHandler(
            file,
        )
    
    # This prevents any unexpected propagation or warnings if logging is enabled 
    # but no handlers are configured.
    if not root.handlers:
        root.addHandler(
            logging.NullHandler(),
        )
        
    _configured = True

###############################################################################

def get_logger(
    name: str,
) -> logging.Logger:
    _configure()

    return logging.getLogger(
        name,
    )
