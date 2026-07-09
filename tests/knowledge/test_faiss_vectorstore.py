"""
Run:
python -m tests.knowledge.test_faiss_vectorstore
"""
from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.embeddings.openai_embedding_provider import OpenAIEmbeddingProvider
from knowledge.loaders.document_metadata import DocumentMetadata
from knowledge.vectorstores.faiss_vectorstore import FAISSVectorStore
from knowledge.query.metadata_query import MetadataQuery

def main():
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
        content="What is RAG?",
        chunk_index=0,
    )

    query_embedding = engine.embed(
        query,
    )

    results = store.search(
        query_embedding,
        k=3,
    )

    print("Search Results")
    print("----------------")

    for result in results:
        print(f"Chunk: {result.chunk.content}")
        print(f"Rank : {result.rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Chunk Id: {result.chunk.chunk_id}")
        print()
        
if __name__ == "__main__":
    main()
