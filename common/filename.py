"""
===============================================================================
Enterprise AI Gateway (EAIG)

Filename Utilities

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

import re


###############################################################################
INVALID_FILENAME_CHARS = r'[<>:"/\\|?*\x00-\x1F]'


###############################################################################
def make_safe_filename(
    text: str,
    max_length: int = 80,
) -> str:
    """
    Convert arbitrary text into a filesystem-safe filename.
    """

    #
    # Remove invalid filename characters.
    #
    text = re.sub(
        INVALID_FILENAME_CHARS,
        "",
        text,
    )

    #
    # Replace whitespace with underscores.
    #
    text = re.sub(
        r"\s+",
        "_",
        text.strip(),

    )

    #
    # Remove repeated underscores.
    #
    text = re.sub(
        r"_+",
        "_",
        text,
    )

    #
    # Remove trailing dots and spaces (Windows)
    #
    text = text.rstrip(". ")

    #
    # Empty?
    #
    if not text:
        text = "conversation"

    #
    # Limit length
    #
    text = text[:max_length]

    return text
