"""
Central logging utility.
"""

from __future__ import annotations

import logging
from pathlib import Path

from config import CONFIG

LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOGGER = logging.getLogger("EnterpriseAI")

if not LOGGER.handlers:
    LOGGER.setLevel(getattr(logging, CONFIG.log_level.upper()))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logfile = logging.FileHandler(
        LOG_FOLDER / "application.log",
        encoding="utf-8"
    )
    logfile.setFormatter(formatter)

    LOGGER.addHandler(console)
    LOGGER.addHandler(logfile)

    LOGGER.propagate = False

def info(message: str) -> None:
    LOGGER.info(message)

def warning(message: str) -> None:
    LOGGER.warning(message)

def error(message: str) -> None:
    LOGGER.error(message)

def debug(message: str) -> None:
    if CONFIG.debug:
        LOGGER.debug(message)
