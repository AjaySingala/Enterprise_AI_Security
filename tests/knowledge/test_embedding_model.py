"""
Run:
python -m tests.knowledge.test_embedding_model
"""
from knowledge.embeddings import Embedding
from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding import Embedding

def main():
    chunk = Chunk(
        document_id="doc-001",
        content="Retrieval Augmented Generation combines vector search with LLMs.",
        chunk_index=0,
    )

    embedding = Embedding(
        chunk=chunk,
        vector=[0.1, 0.2, 0.3],
        model="text-embedding-3-small",
        input_tokens=42,
    )

    print()
    print(embedding)
    print()

    print("Chunk ID      :", embedding.chunk.chunk_id)
    print("Document ID   :", embedding.chunk.document_id)
    print("Chunk Index   :", embedding.chunk.chunk_index)
    print("Content       :", embedding.chunk.content)
    print("Dimensions:", embedding.dimensions)
    print("Vector length:", len(embedding.vector))
    print()

if __name__ == "__main__":
    main()
