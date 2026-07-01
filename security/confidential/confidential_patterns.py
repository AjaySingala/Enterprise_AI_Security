"""
===============================================================================
Enterprise AI Gateway (EAIG)

Feature:
    Confidential Data Detection

File:
    patterns.py

Version:
    1.1.0

Description
-----------
Loads the confidential dictionary from JSON.
===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

from security.confidential.confidential_types import ConfidentialType

def load_patterns() -> dict[ConfidentialType, list[str]]:
    print("--> Entering load_patterns")

    dictionary_file = (
        Path(__file__).resolve()
        .parents[2]
        / "data"
        / "confidential"
        / "dictionary.json"
    )

    with open(
        dictionary_file,
        "r",
        encoding="utf-8",
    ) as fp:
        data = json.load(fp)

    patterns = {}

    for key, values in data.items():
        try:
            patterns[ConfidentialType[key]] = values
        except KeyError:
            print(f"Warning: Unknown confidential type '{key}'")

    print("<-- Exiting load_patterns")

    return patterns

PATTERNS = load_patterns()
