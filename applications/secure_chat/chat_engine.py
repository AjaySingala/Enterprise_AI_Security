"""
===============================================================================
Enterprise AI Gateway (EAIG)

Application:
    Secure Chat

File:
    chat_engine.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Enterprise Secure Chat Engine.
===============================================================================
"""

from __future__ import annotations

import time
import uuid
import json
from dataclasses import asdict
from pathlib import Path

from applications.secure_chat.chat_models import (
    ChatRole,
    ChatResult,
    Conversation,
)

from common.services import services

from config.pricing import MODEL_PRICING
from collections.abc import Generator

###############################################################################
# Chat Engine
###############################################################################
class ChatEngine:
    """
    Enterprise Secure Chat Engine.
    """

    ###########################################################################
    def __init__(self):
        self.pipeline = services.pipeline
        self.llm = services.llm
        self.conversation = Conversation(
            conversation_id=str(uuid.uuid4())
        )

    ###########################################################################
    def chat(
        self,
        user_message: str,
    ) -> ChatResult:
        """
        Process one user message.
        """
        start = time.perf_counter()

        #
        # Store original user message
        #
        self.conversation.add_message(
            ChatRole.USER,
            user_message,
        )

        #
        # Security Pipeline
        #
        security_result = self.pipeline.process(
            user_message,
        )

        #
        # Request blocked
        #
        if security_result.decision.value == "BLOCK":
            elapsed = (
                time.perf_counter() - start
            ) * 1000

            return ChatResult(
                success=False,
                user_message=user_message,
                assistant_message=(
                    "Your request has been blocked by "
                    "the Enterprise AI Gateway."
                ),
                decision="BLOCK",
                request_id=str(uuid.uuid4()),
                processing_time_ms=elapsed,
                sanitized_prompt=security_result.sanitized_text,
                reasons=security_result.reasons,
            )

        #
        # Build conversation for the LLM
        #
        messages = []
        for message in self.conversation.messages:
            messages.append(
                {
                    "role": message.role.value,
                    "content": message.content,
                }
            )

        #
        # Replace last user message with sanitized version
        #
        messages[-1]["content"] = (
            security_result.sanitized_text
        )

        #
        # Call the LLM
        #
        llm_response = self.llm.chat(messages)
        response = llm_response.text

        ###########################################################################
        # Cost Calculation
        ###########################################################################
        pricing = MODEL_PRICING.get(
            llm_response.model,
            {
                "input": 0.0,
                "output": 0.0,
            },
        )

        input_cost = (
            llm_response.input_tokens
            / 1_000_000
        ) * pricing["input"]

        output_cost = (
            llm_response.output_tokens
            / 1_000_000
        ) * pricing["output"]

        estimated_cost = (
            input_cost +
            output_cost
        )

        self.conversation.add_message(
            ChatRole.ASSISTANT,
            response,
        )

        # Estimated Cost.
        self.conversation.add_usage(
            llm_response.input_tokens,
            llm_response.output_tokens,
            estimated_cost,
        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return ChatResult(
            success=True,
            user_message=user_message,
            assistant_message=response,
            model=llm_response.model,
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
            total_tokens=llm_response.total_tokens,
            sanitized_prompt=security_result.sanitized_text,
            decision=security_result.decision.value,
            request_id=str(uuid.uuid4()),
            processing_time_ms=elapsed,
            reasons=security_result.reasons,
        )
    
    ###########################################################################
    def stream_chat(
        self,
        user_message: str,
    ) -> Generator[str, None, ChatResult]:
        """
        Stream an assistant response.

        Yields text chunks.

        Returns ChatResult when complete.
        """

        start = time.perf_counter()

        #
        # Store user message
        #
        self.conversation.add_message(
            ChatRole.USER,
            user_message,
        )

        #
        # Security Pipeline
        #
        security_result = self.pipeline.process(
            user_message,
        )

        #
        # Block?
        #
        if security_result.decision.value == "BLOCK":
            elapsed = (
                time.perf_counter()
                - start
            ) * 1000

            return ChatResult(
                success=False,
                user_message=user_message,
                assistant_message="",
                decision="BLOCK",
                request_id="",
                processing_time_ms=elapsed,
                reasons=security_result.reasons,
            )

        #
        # Build messages
        #
        messages = []
        for message in self.conversation.messages:
            messages.append(
                {
                    "role": message.role.value,
                    "content": message.content,
                }
            )

        #
        # Replace latest prompt with sanitized version
        #
        messages[-1]["content"] = (
            security_result.sanitized_text
        )

        #
        # Stream
        #
        generator = self.llm.stream_chat(
            messages,
        )

        full_response = ""
        try:
            while True:
                token = next(generator)
                full_response += token
                yield token
        except StopIteration as result:
            llm_response = result.value

        #
        # Save assistant message
        #
        self.conversation.add_message(
            ChatRole.ASSISTANT,
            full_response,
        )

        #
        # Cost
        #
        pricing = MODEL_PRICING.get(
            llm_response.model,
            {
                "input": 0.0,
                "output": 0.0,
            },
        )

        input_cost = (
            llm_response.input_tokens
            / 1_000_000
        ) * pricing["input"]

        output_cost = (
            llm_response.output_tokens
            / 1_000_000
        ) * pricing["output"]

        estimated_cost = (
            input_cost +
            output_cost
        )

        self.conversation.add_usage(
            llm_response.input_tokens,
            llm_response.output_tokens,
            estimated_cost,
        )

        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        return ChatResult(
            success=True,
            user_message=user_message,
            assistant_message=full_response,
            decision=security_result.decision.value,
            request_id=llm_response.request_id,
            processing_time_ms=elapsed,
            model=llm_response.model,
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
            total_tokens=llm_response.total_tokens,
            sanitized_prompt=security_result.sanitized_text,
            reasons=security_result.reasons,
        )

    ###########################################################################
    def clear_history(
        self,
    ) -> None:
        self.conversation.clear()

    ###########################################################################
    def save_conversation(
        self,
        filename: str | Path,
    ) -> None:
        path = Path(filename)
        conversation = {
            "conversation_id": self.conversation.conversation_id,
            "title": self.conversation.title,
            "created_at": self.conversation.created_at.isoformat(),
            "updated_at": self.conversation.updated_at.isoformat(),
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat(),
                }
                for message in self.conversation.messages
            ],
        }

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as fp:
            json.dump(
                conversation,
                fp,
                indent=4,
            )

    ###########################################################################
    def load_conversation(
        self,
        filename: str,
    ) -> None:
        path = Path(filename)
        with open(
            path,
            "r",
            encoding="utf-8",
        ) as fp:
            data = json.load(fp)

        self.conversation.messages.clear()

        self.conversation.title = data.get(
            "title",
            "New Conversation",
        )

        from datetime import datetime
        from applications.secure_chat.chat_models import (
            ChatMessage,
            ChatRole,
        )

        for message in data["messages"]:
            self.conversation.messages.append(
                ChatMessage(
                    role=ChatRole(message["role"]),
                    content=message["content"],
                    timestamp=datetime.fromisoformat(
                        message["timestamp"]
                    ),
                )
            )

    ###########################################################################
    def conversation_stats(
        self,
    ) -> dict:
        users = 0
        assistants = 0
        systems = 0

        for message in self.conversation.messages:
            if message.role == ChatRole.USER:
                users += 1
            elif message.role == ChatRole.ASSISTANT:
                assistants += 1
            else:
                systems += 1

        return {
            "conversation_id": self.conversation.conversation_id,
            "title": self.conversation.title,
            "messages": len(self.conversation.messages),
            "user_messages": users,
            "assistant_messages": assistants,
            "system_messages": systems,
            "input_tokens": self.conversation.input_tokens,
            "output_tokens":  self.conversation.output_tokens,
            "total_tokens": self.conversation.total_tokens,
            "estimated_cost_usd":
                round(
                    self.conversation.estimated_cost,
                    6,
                ),
        }

    ###########################################################################
    def new_conversation(
        self,
    ) -> None:
        self.conversation = Conversation(
            conversation_id=str(uuid.uuid4())
        )
