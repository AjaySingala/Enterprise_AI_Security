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
    messages: list[ChatMessage] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )

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

        self.updated_at = datetime.utcnow()

    ###########################################################################
    def clear(
        self,
    ) -> None:
        self.messages.clear()
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
    sanitized_prompt: str = ""
    reasons: list[str] = field(
        default_factory=list
    )
