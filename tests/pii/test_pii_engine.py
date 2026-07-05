"""
===============================================================================
Run:
python -m tests.pii.test_pii_engine
===============================================================================
"""

from security.pii.pii_engine import PIIEngine
from security.pii.pii_types import MaskMode

text = """
Employee

Name : Ajay Singala

Email : ajay.singala@company.com

Phone : +91 9876543210

PAN : ABCDE1234F

Aadhaar : 2345 6789 1234

GitHub :
ghp_abcdefghijklmnopqrstuvwxyz1234567890

OpenAI :
sk-abcdefghijklmnopqrstuvwxyz1234567890
"""

engine = PIIEngine()

result = engine.process(
    text,
    MaskMode.PLACEHOLDER,
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

print("=" * 80)
print("SUMMARY")
print("=" * 80)

print("Entities :", result.detection_result.entity_count)
print("Risk :", result.detection_result.risk_level)
print("Score :", result.detection_result.risk_score)
print()

for entity in result.detection_result.entities:
    print(entity)

# Which detector found each entity.
# For example:
# Entity	    Value	            Detector
# --------------------------------------------
# EMAIL	        ajay@company.com	Presidio
# PAN	        ABCDE1234F	        Regex
# OPENAI_KEY	sk-...	            Regex
