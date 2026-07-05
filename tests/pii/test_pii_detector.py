"""
===============================================================================
Run:
python -m tests.pii.test_pii_detector
===============================================================================
"""

from security.pii.pii_detector import PIIDetector

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

detector = PIIDetector()
result = detector.detect(text)

print()
print("PII FOUND :", result.has_pii)
print("COUNT :", result.entity_count)
print("RISK :", result.risk_level)
print()

for entity in result.entities:
    print(entity)
