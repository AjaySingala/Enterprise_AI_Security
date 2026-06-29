"""
===============================================================================
File        : client.py
Project     : Enterprise AI Security Framework

Description
-----------
Enterprise wrapper around the OpenAI Responses API.

Responsibilities
----------------
- Initialize the OpenAI client
- Validate configuration
- Handle retries
- Measure execution time
- Log requests
- Return a strongly typed LLMResponse

NOTE
----
The actual generate() implementation will be completed in Part 2.
===============================================================================
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from openai import OpenAI

import config

from common.logger import logger
from common.llm.exceptions import InvalidConfigurationError
from common.llm.provider import LLMProvider
from common.llm.response import LLMResponse
from common.llm.retry import Retry

class LLMClient:
    """
    Enterprise wrapper around the OpenAI SDK.

    All demos should use this class rather than directly using
    the OpenAI SDK.
    """

    ###########################################################################
    # Constructor
    ###########################################################################
    def __init__(self) -> None:
        logger.info("Initializing LLMClient...")
        self._validate_configuration()
        self.provider = LLMProvider.OPENAI
        self.model = config.MODEL_NAME
        self.retry = Retry()
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY
        )

        logger.info(
            "LLMClient initialized successfully."
        )

    ###########################################################################
    # Configuration Validation
    ###########################################################################
    @staticmethod
    def _validate_configuration() -> None:
        """
        Validate mandatory configuration.
        """
        logger.debug("Validating configuration...")

        if not config.OPENAI_API_KEY:
            raise InvalidConfigurationError(
                "OPENAI_API_KEY not found in .env"
            )

        if not config.MODEL_NAME:
            raise InvalidConfigurationError(
                "MODEL_NAME not configured."
            )

    ###########################################################################
    # Private Helper
    ###########################################################################
    def _build_messages(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> list[dict[str, Any]]:
        """
        Build the input payload expected by the Responses API.
        """
        logger.debug("Building request payload...")

        return [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": system_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_prompt
                    }
                ]
            }
        ]

    ###########################################################################
    # Private Helper
    ###########################################################################
    @staticmethod
    def _get_usage(response: Any) -> tuple[int, int, int]:
        """
        Safely extract token usage.

        Returns
        -------
        (input_tokens, output_tokens, total_tokens)

        Returns zeros if usage information is unavailable.
        """
        usage = getattr(response, "usage", None)

        if usage is None:
            return 0, 0, 0

        input_tokens = getattr(
            usage,
            "input_tokens",
            0
        )

        output_tokens = getattr(
            usage,
            "output_tokens",
            0
        )

        total_tokens = getattr(
            usage,
            "total_tokens",
            input_tokens + output_tokens
        )

        return (
            input_tokens,
            output_tokens,
            total_tokens
        )

    ###########################################################################
    # Private Helper
    ###########################################################################
    @staticmethod
    def _extract_text(response: Any) -> str:
        """
        Extract generated text from the Responses API object.
        """
        if hasattr(response, "output_text"):
            return response.output_text

        return ""

    ###########################################################################
    # Private Helper
    ###########################################################################
    @staticmethod
    def _elapsed(start: float) -> float:
        """
        Return elapsed time in seconds.
        """
        return round(
            perf_counter() - start,
            3
        )

    ###########################################################################
    # Public API
    ###########################################################################
    def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> LLMResponse:
        """
        Generate a response from the LLM.

        NOTE
        ----
        Full implementation is added in Commit 0004B.
        """
        raise NotImplementedError(
            "Implemented in Commit 0004B."
        )


###############################################################################
# Singleton
###############################################################################
llm = LLMClient()
