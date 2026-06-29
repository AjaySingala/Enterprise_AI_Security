"""
===============================================================================
File        : llm.py
Project     : Enterprise AI Security Framework
Author      : ChatGPT

Description
-----------
Centralized lightweight wrapper around the OpenAI Responses API.

Tested with:
    openai==2.44.0
    
Why use a wrapper?
------------------
Instead of every demo directly calling the OpenAI SDK,
all demos call this wrapper.

Benefits:
- Single location to change model
- Easier logging
- Easier debugging
- Easier migration to Azure OpenAI
- Easier migration to Anthropic/Gemini/Ollama later

If tomorrow you move to Azure OpenAI, Anthropic, Gemini, or a local model, only this file changes.
===============================================================================
"""

from __future__ import annotations

import json
import time

from openai import OpenAI

from config import settings
from common.llm_response import LLMResponse

class LLM:
    def __init__(self) -> None:
        print("--> Entering LLM.__init__")

        self.client = OpenAI(
            api_key=settings.api_key
        )

        print("<-- Exiting LLM.__init__")

    ###########################################################################
    @staticmethod
    def _extract_text(response) -> str:
        """
        Safely extract text from a Responses API object.
        """
        # Preferred
        if hasattr(response, "output_text") and response.output_text:
            return response.output_text

        # Fallback
        try:
            parts = []
            for item in response.output:
                if getattr(item, "type", "") != "message":
                    continue
                for content in item.content:
                    if hasattr(content, "text"):
                        parts.append(content.text)

            return "\n".join(parts)
        except Exception:
            return ""

    ###########################################################################
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        print("--> Entering LLM.generate")

        start = time.perf_counter()

        response = self.client.responses.create(
            model=settings.model,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": system_prompt,
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": user_prompt,
                        }
                    ],
                },
            ],
        )

        elapsed = round(
            time.perf_counter() - start,
            3,
        )

        usage = getattr(response, "usage", None)

        input_tokens = getattr(
            usage,
            "input_tokens",
            0,
        )

        output_tokens = getattr(
            usage,
            "output_tokens",
            0,
        )

        total_tokens = getattr(
            usage,
            "total_tokens",
            input_tokens + output_tokens,
        )

        request_id = getattr(
            response,
            "id",
            "",
        )

        text = self._extract_text(response)

        print("<-- Exiting LLM.generate")

        return LLMResponse(
            text=text,
            model=settings.model,
            request_id=request_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            elapsed_time=elapsed,
            raw_response=response,
        )

    ###########################################################################
    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:
        print("--> Entering LLM.generate_json")

        response = self.generate(
            system_prompt,
            user_prompt,
        )

        cleaned = response.text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        result = json.loads(cleaned)

        print("<-- Exiting LLM.generate_json")

        return result

###
llm = LLM()
