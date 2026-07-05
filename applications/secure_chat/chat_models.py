"""
===============================================================================
Enterprise AI Gateway (EAIG)

Application:
    Secure Chat

File:
    chat_models.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Models used by the Secure Chat application.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

###############################################################################
# Roles
###############################################################################
class ChatRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

###############################################################################
# Message
###############################################################################
@dataclass(slots=True)
class ChatMessage:
    role: ChatRole
    content: str
    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Conversation
###############################################################################
@dataclass(slots=True)
class Conversation:
    conversation_id: str
    title: str = "New Conversation"
    messages: list[ChatMessage] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    ###############################################################################
    # Usage Statistics
    ###############################################################################
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0

    ###########################################################################
    def add_message(
        self,
        role: ChatRole,
        content: str,
    ) -> None:
        self.messages.append(
            ChatMessage(
                role=role,
                content=content,
            )
        )

        #
        # Automatically generate a title from the first user message.
        #
        if (
            role == ChatRole.USER
            and self.title == "New Conversation"
        ):
            title = content.strip()
            if len(title) > 60:
                title = title[:57] + "..."
            self.title = title
           
        self.updated_at = datetime.utcnow()

    ###########################################################################
    def clear(
        self,
    ) -> None:
        self.messages.clear()
        self.updated_at = datetime.utcnow()

    ###########################################################################
    def add_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        estimated_cost: float,
    ) -> None:
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens += (
            input_tokens +
            output_tokens
        )

        self.estimated_cost += estimated_cost
        self.updated_at = datetime.utcnow()
        
###############################################################################
# Chat Result
###############################################################################
@dataclass(slots=True)
class ChatResult:
    success: bool
    user_message: str
    assistant_message: str
    decision: str
    request_id: str
    processing_time_ms: float
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    sanitized_prompt: str = ""
    reasons: list[str] = field(
        default_factory=list
    )

###############################################################################
# Streaming
###############################################################################
class StreamEventType(str, Enum):
    START = "start"
    TOKEN = "token"
    COMPLETE = "complete"
    ERROR = "error"

###############################################################################
@dataclass(slots=True)
class StreamEvent:
    event: StreamEventType
    data: object | None = None
