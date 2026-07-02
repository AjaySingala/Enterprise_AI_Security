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

from applications.secure_chat.chat_models import (
    ChatRole,
    ChatResult,
    Conversation,
)

from common.llm import LLM

from security.pipeline.pipeline_engine import SecurityPipeline

###############################################################################
# Chat Engine
###############################################################################
class ChatEngine:
    """
    Enterprise Secure Chat Engine.
    """

    ###########################################################################
    def __init__(self):
        self.pipeline = SecurityPipeline()
        self.llm = LLM()
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

        self.conversation.add_message(
            ChatRole.ASSISTANT,
            response,
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
    def clear_history(
        self,
    ) -> None:
        self.conversation.clear()
