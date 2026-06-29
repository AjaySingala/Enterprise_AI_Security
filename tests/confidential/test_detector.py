from security.confidential.detector import ConfidentialDetector

text = """
Internal Document

Project Phoenix

This document contains the FY27 pricing strategy.

Revenue forecast for next year.

Roadmap for Project Apollo.

Please do not distribute this document.
"""

detector = ConfidentialDetector()
result = detector.detect(text)

print("=" * 80)

print("CONFIDENTIAL DATA FOUND")

print("=" * 80)

print(f"Found      : {result.has_confidential_data}")
print(f"Count      : {result.entity_count}")
print(f"Risk Score : {result.risk_score}")

print()

for entity in result.entities:
    print(
        f"{entity.entity_type.value:15}"
        f"{entity.risk.value:12}"
        f"{entity.detector:15}"
        f"{entity.value}"
    )
