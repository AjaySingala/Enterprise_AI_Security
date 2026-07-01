from security.secrets.secrets_detector import SecretDetector

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

detector = SecretDetector()
result = detector.detect(text)

print()
print("=" * 80)
print("Secrets Found :", result.has_secrets)
print("Count :", result.entity_count)
print("Risk :", result.risk_score)
print()

for entity in result.entities:
    print(f"{entity.secret_type.value} | {entity.value} | {entity.detector} | {entity.severity.value}")
