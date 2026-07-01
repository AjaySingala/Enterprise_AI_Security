from security.pii.pii_detector import PIIDetector
from security.pii.pii_masker import PIIMasker
from security.pii.pii_types import MaskMode

text = """
Name      : Ajay Singala

Email     : ajay.singala@company.com

Phone     : +91 9876543210

PAN       : ABCDE1234F

Aadhaar   : 2345 6789 1234

GitHub    : ghp_abcdefghijklmnopqrstuvwxyz1234567890

OpenAI    : sk-abcdefghijklmnopqrstuvwxyz1234567890
"""

detector = PIIDetector()

result = detector.detect(text)

masker = PIIMasker()

print("=" * 80)
print("ORIGINAL")
print("=" * 80)
print(text)

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
