"""
===============================================================================
File        : response.py
Project     : Enterprise AI Gateway (EAIG)

Description
-----------
Defines the standard response object returned by the Enterprise LLM SDK.

Every LLM request in this project returns an instance of LLMResponse
instead of a plain string. This provides additional metadata such as:

- Response text
- Success status
- Model used
- Execution time
- Token usage
- Estimated cost
- Request ID

Benefits
--------
1. Strong typing
2. Easier debugging
3. Better logging
4. Enterprise-style SDK design
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

# from common.tracer import trace_enter
# from common.tracer import trace_exit
from common.tracing.trace_decorator import trace

@dataclass(slots=True)
class LLMResponse:
    """
    Standard response returned by the Enterprise LLM SDK.
    """
    success: bool
    text: str = ""
    model: str = ""
    request_id: str = ""
    elapsed_time: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    finish_reason: str = ""
    error_message: str = ""
    raw_response: Optional[Any] = None

    ###########################################################################
    # Helper Methods
    ###########################################################################
    @trace
    def is_success(self) -> bool:
        """
        Returns True if the request completed successfully.
        """
        # trace_enter("LLMResponse.is_success")

        result = self.success

        # trace_exit("LLMResponse.is_success")

        return result

    ###########################################################################
    @trace
    def has_error(self) -> bool:
        """
        Returns True if an error occurred.
        """
        # trace_enter("LLMResponse.has_error")

        result = not self.success

        # trace_exit("LLMResponse.has_error")

        return result

    ###########################################################################
    @trace
    def print_summary(self) -> None:
        """
        Prints a concise summary of the response.
        """
        # trace_enter("LLMResponse.print_summary")

        print("\n" + "=" * 80)
        print("LLM RESPONSE SUMMARY")
        print("=" * 80)

        print(f"Success           : {self.success}")
        print(f"Model             : {self.model}")
        print(f"Request ID        : {self.request_id}")

        print(f"Elapsed Time      : {self.elapsed_time:.2f} sec")

        print(f"Input Tokens      : {self.input_tokens}")
        print(f"Output Tokens     : {self.output_tokens}")
        print(f"Total Tokens      : {self.total_tokens}")

        print(f"Estimated Cost    : ${self.estimated_cost:.6f}")

        if self.finish_reason:
            print(f"Finish Reason     : {self.finish_reason}")

        if self.error_message:
            print(f"Error             : {self.error_message}")

        print("=" * 80)

        # trace_exit("LLMResponse.print_summary")

    ###########################################################################
    @trace
    def print_answer(self) -> None:
        """
        Prints only the generated text.
        """
        # trace_enter("LLMResponse.print_answer")

        print("\nGenerated Response")
        print("-" * 80)
        print(self.text)
        print("-" * 80)

        # trace_exit("LLMResponse.print_answer")

    ###########################################################################
    @trace
    def to_dict(self) -> dict:
        """
        Converts the object into a dictionary.
        """
        # trace_enter("LLMResponse.to_dict")

        data = {
            "success": self.success,
            "text": self.text,
            "model": self.model,
            "request_id": self.request_id,
            "elapsed_time": self.elapsed_time,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost": self.estimated_cost,
            "finish_reason": self.finish_reason,
            "error_message": self.error_message,
        }

        # trace_exit("LLMResponse.to_dict")

        return data

    ###########################################################################
    @trace
    @classmethod
    def failure(cls, message: str) -> "LLMResponse":
        """
        Creates a standard failure response.
        """
        # trace_enter("LLMResponse.failure")

        response = cls(
            success=False,
            error_message=message
        )

        # trace_exit("LLMResponse.failure")

        return response

    ###########################################################################
    @trace
    @classmethod
    def success_response(
        cls,
        text: str,
        model: str
    ) -> "LLMResponse":
        """
        Creates a minimal success response.
        """
        # trace_enter("LLMResponse.success_response")

        response = cls(
            success=True,
            text=text,
            model=model
        )

        # trace_exit("LLMResponse.success_response")

        return response
    