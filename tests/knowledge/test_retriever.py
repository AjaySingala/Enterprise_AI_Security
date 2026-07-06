"""

Run:
python -m tests.knowledge.test_retriever
"""
from common.services import services

from knowledge.chunking.chunk import Chunk

def build_store():
    store = services.vector_store
    store.clear()
    chunks = [
        Chunk(
            document_id="AI",
            content="Retrieval Augmented Generation combines vector search with LLMs.",
            chunk_index=0,
        ),
        Chunk(
            document_id="AI",
            content="Embeddings convert text into vectors.",
            chunk_index=1,
        ),
        Chunk(
            document_id="SECURITY",
            content="Prompt Injection attacks target language models.",
            chunk_index=2,
        ),
        Chunk(
            document_id="PYTHON",
            content="Python is an interpreted programming language.",
            chunk_index=3,
        ),
    ]

    embeddings = services.embedding_engine.embed_batch(
        chunks,
    )

    store.add(
        embeddings,
    )

def main():
    build_store()

    print()
    print("=" * 80)

    query = "What is Retrieval Augmented Generation?"

    print(f"Query: {query}")
    print()

    results = services.retriever.retrieve(
        query=query,
        k=3,        # Play with this.
    )

    for result in results:
        print(
            f"Rank : {result.rank}"
        )
        print(
            f"Score: {result.score:.4f}"
        )
        print(
            f"Document : {result.embedding.document_id}"
        )
        print(
            f"Chunk    : {result.embedding.chunk_index}"
        )
        print(
            result.embedding.content
        )
        print()

if __name__ == "__main__":
    main()
