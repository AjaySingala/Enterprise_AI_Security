"""
Run:
python -m tests.knowledge.test_embedding_engine
"""

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding_engine import EmbeddingEngine

def main():
    chunk = Chunk(
        document_id="doc-001",
        content="""
Retrieval Augmented Generation combines
vector search with LLM reasoning.
""",
        chunk_index = 0,
    )

    engine = EmbeddingEngine()
    embedding = engine.embed(
        chunk,
    )

    print()
    print("Model:", embedding.model)
    print("Dimensions:", embedding.dimensions)
    print("Input Tokens:", embedding.input_tokens)
    print("Vector Length:", len(embedding.vector))
    print()

    print("First 10 values")
    print("----------------")

    for value in embedding.vector[:10]:
        print(value)

    print()

if __name__ == "__main__":
    main()
