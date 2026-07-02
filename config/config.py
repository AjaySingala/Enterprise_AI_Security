# pip install python-dotenv
"""
Configuration Module

Loads all configuration from the .env file.

This file should be the ONLY place that reads
environment variables directly.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

DEBUG = (os.getenv("DEBUG","True").lower() == "true")

if DEBUG:
    print("--> Entering: config.py")

class Settings:
    """
    Global application settings.
    """
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("MODEL_NAME","gpt-4o-mini")
        self.text_embedding_model = os.getenv("TEXT_EMBEDDING_MODEL", "text-embedding-3-small"),
        self.debug = (os.getenv("DEBUG","True").lower() == "true")
        self.log_level=os.getenv("LOG_LEVEL", "INFO"),

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in .env"
            )
       
settings = Settings()

# print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")

if DEBUG:
    print("<-- Exiting : config.py")
