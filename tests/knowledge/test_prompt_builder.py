"""
Tests the PromptBuilder.

Flow:
Chunks
    ↓
Embeddings
    ↓
Vector Store
    ↓
Retriever
    ↓
Prompt Builder

Run:
python -m test.knowledge.test_prompt_builder
"""

from common.services import services

from knowledge.chunking.chunk import Chunk

###############################################################################
def build_vector_store():
    store = services.vector_store
    store.clear()

    chunks = [
        Chunk(
            document_id="AI",
            content="""
Retrieval Augmented Generation (RAG) combines vector search
with Large Language Models to answer questions using external
knowledge.
""".strip(),
            chunk_index=0,
        ),

        Chunk(
            document_id="AI",
            content="""
Embeddings convert text into high-dimensional vectors so that
semantically similar text is located close together.
""".strip(),
            chunk_index=1,
        ),

        Chunk(
            document_id="SECURITY",
            content="""
Prompt Injection is an attack where malicious instructions are
embedded into user input or retrieved documents.
""".strip(),
            chunk_index=2,
        ),

        Chunk(
            document_id="PYTHON",
            content="""
Python is a popular programming language for AI and machine learning.
""".strip(),
            chunk_index=3,
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
    build_vector_store()

    query = "What is Retrieval Augmented Generation?"

    #
    # Retrieve relevant chunks.
    #
    results = services.retriever.retrieve(
        query=query,
        k=3,
    )

    #
    # Build prompt.
    #
    prompt = services.prompt_builder.build_prompt(
        query=query,
        results=results,
    )

    print()
    print("=" * 80)
    print("SYSTEM PROMPT")
    print("=" * 80)
    print()
    print(prompt.system_prompt)

    print()
    print("=" * 80)
    print("USER PROMPT")
    print("=" * 80)
    print()
    print(prompt.user_prompt)

    print()
    print("=" * 80)
    print("FULL PROMPT")
    print("=" * 80)
    print()
    print(prompt.full_prompt)

###############################################################################
if __name__ == "__main__":
    main()
