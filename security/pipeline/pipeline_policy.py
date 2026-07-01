"""
===============================================================================
Enterprise AI Security Framework

Feature:
    Enterprise Security Pipeline

File:
    policy.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Enterprise Policy Engine.

This module makes the final decision based on the
results produced by all security engines.

Flow:
-----
Prompt Injection?
↓
BLOCK
--------------------------------
Secrets?
↓
FULL MASK
--------------------------------
PII?
↓
PLACEHOLDER
--------------------------------
Confidential?
↓
PARTIAL
--------------------------------
Final Decision
↓
ALLOW
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from security.pipeline.pipeline_types import PipelineDecision

###############################################################################
# Policy
###############################################################################
@dataclass(slots=True)
class SecurityPolicy:
    #
    # Prompt Injection
    #
    block_prompt_injection: bool = True

    #
    # PII
    #
    sanitize_pii: bool = True

    #
    # Secrets
    #
    sanitize_secrets: bool = True

    #
    # Confidential
    #
    sanitize_confidential: bool = True

###############################################################################
# Policy Engine
###############################################################################
class PolicyEngine:
    """
    Enterprise Policy Decision Engine.
    """

    ###########################################################################
    def __init__(
        self,
        policy: SecurityPolicy | None = None,
    ) -> None:
        print("--> Entering PolicyEngine.__init__")

        self.policy = policy or SecurityPolicy()

        print("<-- Exiting PolicyEngine.__init__")

    ###########################################################################
    def evaluate(
        self,
        prompt_result,
        pii_result,
        secret_result,
        confidential_result,
    ) -> PipelineDecision:
        print("--> Entering PolicyEngine.evaluate")

        #
        # Prompt Injection
        #
        if (
            self.policy.block_prompt_injection
            and prompt_result.decision.value == "BLOCK"
        ):

            print("Policy Decision : BLOCK (Prompt Injection)")

            print("<-- Exiting PolicyEngine.evaluate")

            return PipelineDecision.BLOCK

        #
        # Sanitization Required?
        #
        if (
            self.policy.sanitize_pii
            and pii_result.detection_result.has_pii
        ):
            print("Policy Decision : SANITIZE (PII)")

            print("<-- Exiting PolicyEngine.evaluate")

            return PipelineDecision.SANITIZE

        if (
            self.policy.sanitize_secrets
            and secret_result.detection_result.has_secrets
        ):
            print("Policy Decision : SANITIZE (Secrets)")

            print("<-- Exiting PolicyEngine.evaluate")

            return PipelineDecision.SANITIZE

        if (
            self.policy.sanitize_confidential
            and confidential_result.detection_result.has_confidential_data
        ):
            print("Policy Decision : SANITIZE (Confidential)")

            print("<-- Exiting PolicyEngine.evaluate")

            return PipelineDecision.SANITIZE

        print("Policy Decision : ALLOW")

        print("<-- Exiting PolicyEngine.evaluate")

        return PipelineDecision.ALLOW
    