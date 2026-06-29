"""
===============================================================================
File        : exceptions.py
Project     : Enterprise AI Security Framework

Description
-----------
Custom exceptions used by the Enterprise LLM SDK.

Using custom exceptions instead of generic Exception makes it easier
to identify and handle failures throughout the application.
===============================================================================
"""

from __future__ import annotations

class LLMError(Exception):
    """
    Base exception for all LLM related errors.
    """
    pass


class AuthenticationError(LLMError):
    """
    Raised when authentication with the LLM provider fails.
    """
    pass


class RateLimitError(LLMError):
    """
    Raised when the provider rate limits requests.
    """
    pass


class ConnectionError(LLMError):
    """
    Raised when a network connection cannot be established.
    """
    pass


class TimeoutError(LLMError):
    """
    Raised when a request times out.
    """
    pass


class InvalidResponseError(LLMError):
    """
    Raised when the provider returns an invalid response.
    """
    pass


class InvalidConfigurationError(LLMError):
    """
    Raised when mandatory configuration values are missing.
    """
    pass


class JSONParsingError(LLMError):
    """
    Raised when JSON parsing fails.
    """
    pass
