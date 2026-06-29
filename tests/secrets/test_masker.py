from security.secrets.detector import SecretDetector
from security.secrets.masker import SecretMasker
from security.secrets.types import MaskMode

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

random2 =
ZXhhbXBsZUBjb21wYW55LmNvbQ==
"""

detector = SecretDetector()
result = detector.detect(text)

masker = SecretMasker()

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
