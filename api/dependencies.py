"""
===============================================================================
Enterprise AI Gateway (EAIG)

dependencies.py

Version:
    1.0.0
===============================================================================
"""

from security.pipeline.pipeline_engine import SecurityPipeline

#
# Singleton
#
_pipeline = SecurityPipeline()

def get_pipeline() -> SecurityPipeline:
    return _pipeline
