from security.secrets.secrets_engine import SecretEngine
from security.secrets.secrets_types import MaskMode

text = """
OPENAI_API_KEY = "sk-abcdefghijklmnopqrstuvwxyz123456789012345678"

github_token = "ghp_abcdefghijklmnopqrstuvwxyz123456789012"

aws_access = "AKIAIOSFODNN7EXAMPLE"

jwt =
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
.eyJzdWIiOiIxMjM0NTY3ODkwIn0
.signature

random =
xP9K#Lm2Qv8Rw4NzTy6Uc1Gh
"""

engine = SecretEngine()

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

summary = result.detection_result

print(f"Secrets Found : {summary.has_secrets}")
print(f"Count         : {summary.entity_count}")
print(f"Risk Score    : {summary.risk_score}")

print()

print("=" * 80)
print("DETECTED SECRETS")
print("=" * 80)

for entity in summary.entities:
    print(
        f"{entity.secret_type.value:20}"
        f"{entity.detector:10}"
        f"{entity.severity.value:10}"
        f"{entity.value}"
    )
