"""
Run:
python -m tests.knowledge.test_embedding_model
"""
from knowledge.embeddings import Embedding

def main():
    embedding = Embedding(
        chunk_id="chunk-001",
        vector=[0.1, 0.2, 0.3],
        model="text-embedding-3-small",
        dimensions=3,
        input_tokens=42,
    )

    print()
    print(embedding)
    print()

    print("Dimensions:", embedding.dimensions)
    print("Vector length:", len(embedding.vector))
    print()

if __name__ == "__main__":
    main()
