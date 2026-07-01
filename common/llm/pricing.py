"""
===============================================================================
File        : pricing.py
Project     : Enterprise AI Gateway (EAIG)

Description
-----------
Provides approximate token pricing for supported LLM models.

NOTE
----
These prices are estimates and may change over time.

Update this file whenever provider pricing changes.
===============================================================================
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ModelPricing:
    model: str
    input_price_per_million: float
    output_price_per_million: float


###############################################################################
# OpenAI Pricing
###############################################################################
MODEL_PRICING = {
    # Approximate pricing (USD / 1M tokens)
    "gpt-4o-mini":
        ModelPricing(
            model="gpt-4o-mini",
            input_price_per_million=0.15,
            output_price_per_million=0.60
        ),
}


###############################################################################
def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Estimate the total request cost.

    Returns
    -------
    Estimated cost in USD.
    """

    if model not in MODEL_PRICING:
        return 0.0

    pricing = MODEL_PRICING[model]

    input_cost = (
        input_tokens / 1_000_000
    ) * pricing.input_price_per_million

    output_cost = (
        output_tokens / 1_000_000
    ) * pricing.output_price_per_million

    return round(
        input_cost + output_cost,
        8
    )
