""""
Vector Store Inspector Demo

Shows the current contents of a vector store.

This is not part of the SDK.
It is a developer tool.
Think of it like:

Git
    git status

Docker
    docker ps

EAIG
    inspect_vector_store()

Run:
python -m tests.knowledge.test_vector_store_inspector
"""

from common.services import services

from knowledge.chunking.chunk import Chunk

###############################################################################
def print_separator():
    print("=" * 80)

###############################################################################
def print_store_info():
    store = services.vector_store

    print_separator()
    print("VECTOR STORE")
    print_separator()
    print()

    print(f"Store Type : {type(store).__name__}")
    print(f"Embeddings : {store.count()}")
    print()

    if store.index is None:
        print("Store is empty.")
        return

    print(f"FAISS Index : {type(store.index).__name__}")
    print(f"Dimension   : {store.index.d}")
    print(f"Vectors     : {store.index.ntotal}")
    print()

###############################################################################
def print_sample_entries():
    store = services.vector_store

    print_separator()
    print("SAMPLE ENTRIES")
    print_separator()
    print()

    if not store.embeddings:
        print("No embeddings.")
        return

    for i, embedding in enumerate(
        store.embeddings,
        start=1,
    ):

        print(f"Embedding #{i}")
        print("----------------")
        print(f"Chunk ID    : {embedding.chunk_id}")
        print(f"Document ID : {embedding.document_id}")
        print(f"Chunk Index : {embedding.chunk_index}")
        print(f"Content     : {embedding.content}")
        print(f"Model       : {embedding.model}")
        print(f"Dimensions  : {embedding.dimensions}")
        print(f"Tokens      : {embedding.input_tokens}")
        print()

        if i >= 5:
            break

###############################################################################
def build_sample_store():
    engine = services.embedding_engine
    store = services.vector_store
    store.clear()
    chunks = [
        Chunk(
            document_id="doc001",
            content="Retrieval Augmented Generation combines vector search with LLMs.",
            chunk_index=0,
        ),
        Chunk(
            document_id="doc001",
            content="Embeddings convert text into vectors.",
            chunk_index=1,
        ),
        Chunk(
            document_id="doc001",
            content="Prompt Injection attacks target language models.",
            chunk_index=2,
        ),
        Chunk(
            document_id="doc001",
            content="Python is widely used for AI.",
            chunk_index=3,
        ),
    ]

    embeddings = engine.embed_batch(
        chunks,
    )

    store.add(
        embeddings,
    )

###############################################################################
def main():
    build_sample_store()
    print_store_info()
    print_sample_entries()

###############################################################################
if __name__ == "__main__":
    main()
