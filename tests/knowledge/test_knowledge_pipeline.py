"""
Run:
python -m tests.knowledge.test_knowledge_pipeline
"""
from common.services import services

from knowledge.chunking.chunk import Chunk

###############################################################################
def load_documents():
    store = services.vector_store
    store.clear()
    chunks = [
        Chunk(
            document_id="AI",
            content="Retrieval Augmented Generation combines vector search with Large Language Models.",
            chunk_index=0,
        ),
        Chunk(
            document_id="AI",
            content="Embeddings convert text into vectors used for semantic similarity.",
            chunk_index=1,
        ),
        Chunk(
            document_id="SECURITY",
            content="Prompt Injection attacks manipulate an LLM by inserting malicious instructions.",
            chunk_index=2,
        ),
    ]

    embeddings = services.embedding_engine.embed_batch(
        chunks,
    )

    store.add(
        embeddings,
    )

###############################################################################
def main():
    load_documents()

    response = services.knowledge_pipeline.ask(
        query="What is Retrieval Augmented Generation?",
    )

    print()
    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print()

    print(response.llm_response)

    print()
    print("=" * 80)
    print("SOURCES")
    print("=" * 80)
    print()

    for result in response.search_results:
        print(
            f"{result.embedding.document_id} "
            f"[Chunk {result.embedding.chunk_index}]"
        )

    print()
    print("=" * 80)
    print(f"Elapsed : {response.elapsed_ms:.2f} ms")
    print("=" * 80)

###############################################################################
if __name__ == "__main__":
    main()
