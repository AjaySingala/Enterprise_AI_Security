"""
===============================================================================
Enterprise AI Gateway (EAIG)

Service Registry

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from common.metrics import MetricsService

from security.pipeline.pipeline_engine import SecurityPipeline

###############################################################################
# Service Registry
###############################################################################
class ServiceRegistry:
    """
    Central registry for shared singleton services.
    """

    ###########################################################################
    def __init__(self):
        self._pipeline = SecurityPipeline()
        self._metrics = MetricsService()

    ###########################################################################
    @property
    def pipeline(self) -> SecurityPipeline:
        return self._pipeline

    ###########################################################################
    @property
    def metrics(self) -> MetricsService:
        return self._metrics

###############################################################################
# Singleton
###############################################################################
services = ServiceRegistry()
