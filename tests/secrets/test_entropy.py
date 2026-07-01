from security.secrets.secrets_entropy import EntropyDetector

samples = [
    "password",
    "HelloWorld",
    "1234567890",
    "sk-abcdefghijklmnopqrstuvwxyz1234567890",
    "AKIAIOSFODNN7EXAMPLE",
    "xP9K#Lm2Qv8Rw4NzTy6Uc1Gh",
    "aaaaaaaaaaaaaaaaaaaaaaaa",
]

for value in samples:
    print("=" * 80)
    print(value)

    entropy = EntropyDetector.calculate(value)
    print(f"Entropy : {entropy:.2f}")

    print(
        "High Entropy :",
        EntropyDetector.is_high_entropy(value),
    )

    print()
