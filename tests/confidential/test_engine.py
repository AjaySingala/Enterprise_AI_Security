from security.confidential.engine import ConfidentialEngine
from security.confidential.types import MaskMode

text = """
Internal Strategy Document

Project Phoenix is our highest priority initiative.

The pricing strategy and revenue forecast
must not be shared outside the organization.

Project Apollo begins next month.

Customer Alpha has approved the proposal.
"""

engine = ConfidentialEngine()

result = engine.process(
    text,
    MaskMode.PLACEHOLDER,
    # MaskMode.FULL,
    # MaskMode.PARTIAL,
)

print("=" * 80)
print("ORIGINAL")
print("=" * 80)

print(result.original_text)

print()

print("=" * 80)
print("MASKED")
print("=" * 80)

print(result.masked_text)

print()

summary = result.detection_result

print("=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"Found      : {summary.has_confidential_data}")
print(f"Count      : {summary.entity_count}")
print(f"Risk Score : {summary.risk_score}")

print()

print("=" * 80)
print("ENTITIES")
print("=" * 80)

for entity in summary.entities:
    print(
        f"{entity.entity_type.value:15}"
        f"{entity.risk.value:12}"
        f"{entity.detector:15}"
        f"{entity.value}"
    )
