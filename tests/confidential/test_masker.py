from security.confidential.confidential_detector import ConfidentialDetector
from security.confidential.confidential_masker import ConfidentialMasker
from security.confidential.confidential_types import MaskMode

text = """
Internal Strategy Document

Project Phoenix is our highest priority initiative.

The pricing strategy and revenue forecast for FY27
must not be shared outside the organization.

Project Apollo will begin next quarter.
"""

detector = ConfidentialDetector()

result = detector.detect(text)

masker = ConfidentialMasker()

print("=" * 80)
print("ORIGINAL")
print("=" * 80)

print(text)

print()

print("=" * 80)
print("PLACEHOLDER")
print("=" * 80)

print(
    masker.mask(
        text,
        result,
        MaskMode.PLACEHOLDER,
    )
)

print()

print("=" * 80)
print("PARTIAL")
print("=" * 80)

print(
    masker.mask(
        text,
        result,
        MaskMode.PARTIAL,
    )
)

print()

print("=" * 80)
print("FULL")
print("=" * 80)

print(
    masker.mask(
        text,
        result,
        MaskMode.FULL,
    )
)
