"""
===============================================================================
Metadata Filtering Tests
===============================================================================
"""

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding import Embedding
from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.embeddings.openai_embedding_provider import OpenAIEmbeddingProvider
from knowledge.loaders.document_metadata import DocumentMetadata
from knowledge.query.metadata_query import MetadataQuery
from knowledge.vectorstores.faiss_vectorstore import FAISSVectorStore

def test_metadata_filter():
    provider = OpenAIEmbeddingProvider()
    engine = EmbeddingEngine(
        provider=provider,
    )

    store = FAISSVectorStore()
    chunks = [
        Chunk(
            document_id="doc1",
            content="Retrieval Augmented Generation",
            chunk_index=0,
        ),
        Chunk(
            document_id="doc2",
            content="Vector databases store embeddings.",
            chunk_index=1,
        ),
        Chunk(
            document_id="doc3",
            content="Prompt Injection attacks target LLMs.",
            chunk_index=2,
        ),
        Chunk(
            document_id="doc4",
            content="Python is a programming language.",
            chunk_index=3,
        ),
        Chunk(
            document_id="doc-5",
            content="Annual leave policy",
            chunk_index=0,
            metadata=DocumentMetadata(department="HR", country="India",),
        ),
        Chunk(
            document_id="doc-6",
            content="Expense reimbursement policy",
            chunk_index=0,
            metadata=DocumentMetadata(department="Finance", country="India",),
        ),
    ]

    embeddings = engine.embed_batch(
        chunks,
    )

    store.add(
        embeddings,
    )

    print()
    print(
        f"Stored {store.count()} embeddings"
    )
    print()

    query = Chunk(
        document_id="query",
        content="What is the reimbursement policy?",
        chunk_index=0,
    )

    query_embedding = engine.embed(
        query,
    )

    metadata_query = MetadataQuery()
    metadata_query.add(
        "department",
        "sales",
    )

    results = store.search(
        query_embedding=query_embedding,
        k=5,
        metadata_query=metadata_query,
    )

    print("Metadata Query Search Results")
    print("-----------------------------")

    if len(results) == 0:
        print("*** No results. ***")

    for result in results:
        print(f"Chunk: {result.chunk.content}")
        print(f"Rank : {result.rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Chunk Id: {result.chunk.chunk_id}")
        print()

        # assert (
        #     result
        #     .embedding
        #     .chunk
        #     .metadata
        #     .department
        #     == "HR"
        # )
        
###############################################################################
def build_embedding(
    document_id: str,
    department: str,
    country: str,
    vector: list[float],
) -> Embedding:
    chunk = Chunk(
        document_id=document_id,
        content=f"{department} document",
        chunk_index=0,
        metadata=DocumentMetadata(
            department=department,
            country=country,
        ),
    )

    return Embedding(
        chunk=chunk,
        vector=vector,
        model="test-model",
        input_tokens=0,
    )

###############################################################################
def main():
    store = FAISSVectorStore()

    #
    # Add three documents.
    #
    # Why fake vectors instead of calling OpenAI.?
    # This gives us:
    # - deterministic tests,
    # - no API cost,
    # - no internet dependency,
    # - no model drift,
    # - very fast execution.
    # That's exactly what unit/component tests should be.
    embeddings = [
        build_embedding(
            "HR-India",
            "HR",
            "India",
            [1.0, 0.0, 0.0],
        ),
        build_embedding(
            "Finance-India",
            "Finance",
            "India",
            [0.9, 0.1, 0.0],
        ),
        build_embedding(
            "HR-USA",
            "HR",
            "USA",
            [0.8, 0.2, 0.0],
        ),
    ]

    store.add(
        embeddings,
    )

    #
    # Query embedding.
    #
    query = build_embedding(
        "QUERY",
        "",
        "",
        [1.0, 0.0, 0.0],
    )

    #
    # HR only.
    #
    metadata_query = MetadataQuery()

    metadata_query.add(
        field="department",
        value="HR",
    )

    results = store.search(
        query_embedding=query,
        k=5,
        metadata_query=metadata_query,
    )

    print()
    print("HR Filter")

    for result in results:
        print(
            result.chunk.content,
            result.chunk.document_id,
            result.chunk.metadata.department,
            result.chunk.metadata.country,
        )

    assert len(results) == 2

    #
    # HR + India.
    #
    metadata_query = MetadataQuery()
    metadata_query.add(
        "department",
        "HR",
    )

    metadata_query.add(
        "country",
        "India",
    )

    results = store.search(
        query_embedding=query,
        k=5,
        metadata_query=metadata_query,
    )

    print()
    print("HR + India")

    for result in results:
        print(
            result.chunk.content,
            result.chunk.document_id,
            result.chunk.metadata.department,
            result.chunk.metadata.country,
        )

    assert len(results) == 1
    assert (
        results[0]
        .embedding
        .chunk
        .document_id
        == "HR-India"
    )

    print()
    print("Metadata filtering passed.")

    # # To test with OpenAI and FAISS Vector Store, uncomment this.
    # test_metadata_filter()

if __name__ == "__main__":
    main()
