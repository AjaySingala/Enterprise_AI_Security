"""
===============================================================================
Enterprise AI Gateway (EAIG)

Model Pricing

Version:
    1.1.0

Python:
    3.13.11

Description
-----------
LLM pricing configuration.

Prices are USD per 1 Million tokens.
===============================================================================
"""

MODEL_PRICING = {
    #
    # OpenAI
    #
    "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60,
    },
    "gpt-4.1-mini": {
        "input": 0.40,
        "output": 1.60,
    },
    "gpt-4.1": {
        "input": 2.00,
        "output": 8.00,
    },
}
