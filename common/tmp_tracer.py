"""
Simple tracing helpers.

Every function in this project should call
trace_enter() and trace_exit().
"""

from config.config import DEBUG

def trace_enter(function_name: str):
    if DEBUG:
        print(f"\n--> Entering : {function_name}")


def trace_exit(function_name: str):
    if DEBUG:
        print(f"<-- Exiting  : {function_name}")
