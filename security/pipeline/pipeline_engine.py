"""
===============================================================================
Enterprise AI Security Framework

Feature:
    Enterprise Security Pipeline

File:
    engine.py

Version:
    1.0.0

Python:
    3.13.11

Description
-----------
Enterprise Security Pipeline.

This is the primary entry point used by applications.
===============================================================================
"""

from __future__ import annotations

from security.pipeline.pipeline_policy import PolicyEngine
from security.pipeline.pipeline_types import (
    PipelineDecision,
    SecurityPipelineResult,
)

from security.prompt_injection.prompt_injection_engine import PromptInjectionEngine

from security.pii.pii_engine import PIIEngine
from security.pii.pii_types import MaskMode as PIIMaskMode

from security.secrets.secrets_engine import SecretEngine
from security.secrets.secrets_types import MaskMode as SecretMaskMode

from security.confidential.confidential_engine import ConfidentialEngine
from security.confidential.confidential_types import (
    MaskMode as ConfidentialMaskMode,
)

class SecurityPipeline:
    """
    Enterprise Security Gateway.
    """

    ###########################################################################
    def __init__(self):
        print("--> Entering SecurityPipeline.__init__")

        self.prompt_engine = PromptInjectionEngine()
        self.pii_engine = PIIEngine()
        self.secret_engine = SecretEngine()
        self.confidential_engine = ConfidentialEngine()
        self.policy = PolicyEngine()

        print("<-- Exiting SecurityPipeline.__init__")

    ###########################################################################
    def process(
        self,
        text: str,
    ) -> SecurityPipelineResult:
        print("--> Entering SecurityPipeline.process")

        reasons = []

        #######################################################################
        # Prompt Injection
        #######################################################################
        prompt_result = self.prompt_engine.analyze(text)

        #######################################################################
        # PII
        #######################################################################
        pii_result = self.pii_engine.process(
            text,
            PIIMaskMode.PLACEHOLDER,
        )

        #######################################################################
        # Secrets
        #######################################################################
        secret_result = self.secret_engine.process(
            text,
            SecretMaskMode.PLACEHOLDER,
        )

        #######################################################################
        # Confidential
        #######################################################################
        confidential_result = self.confidential_engine.process(
            text,
            ConfidentialMaskMode.PLACEHOLDER,
        )

        #######################################################################
        # Policy
        #######################################################################
        decision = self.policy.evaluate(
            prompt_result,
            pii_result,
            secret_result,
            confidential_result,
        )

        #######################################################################
        # Build Sanitized Text
        #######################################################################
        sanitized = text

        if decision != PipelineDecision.BLOCK:
            sanitized = pii_result.masked_text
            sanitized = self.secret_engine.process(
                sanitized,
                SecretMaskMode.PLACEHOLDER,
            ).masked_text

            sanitized = self.confidential_engine.process(
                sanitized,
                ConfidentialMaskMode.PLACEHOLDER,
            ).masked_text

        #######################################################################
        # Audit Reasons
        #######################################################################
        if prompt_result.decision.value == "BLOCK":
            reasons.append("Prompt injection detected.")

        if pii_result.detection_result.has_pii:
            reasons.append(
                f"{pii_result.detection_result.entity_count} PII entities detected."
            )

        if secret_result.detection_result.has_secrets:
            reasons.append(
                f"{secret_result.detection_result.entity_count} secrets detected."
            )

        if confidential_result.detection_result.has_confidential_data:
            reasons.append(
                f"{confidential_result.detection_result.entity_count} confidential items detected."
            )

        print("<-- Exiting SecurityPipeline.process")

        return SecurityPipelineResult(
            original_text=text,
            sanitized_text=sanitized,
            decision=decision,
            reasons=reasons,
            prompt_result=prompt_result,
            pii_result=pii_result,
            secret_result=secret_result,
            confidential_result=confidential_result,
        )
    