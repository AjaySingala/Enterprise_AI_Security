"""
===============================================================================
Enterprise AI Gateway (EAIG)

dependencies.py

Version:
    1.1.0
===============================================================================
"""

from common.services import services

def get_pipeline():
    return services.pipeline

def get_metrics():
    return services.metrics

def get_audit():
    return services.audit

def get_llm():
    return services.llm
