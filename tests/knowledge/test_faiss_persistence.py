"""
===============================================================================
FAISS Persistence Test

Run :
python -m tests.knowledge.test_faiss_persistence
===============================================================================
"""

from pathlib import Path

from knowledge.chunking.recursive_chunker import RecursiveChunker
from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.embeddings.openai_embedding_provider import (
    OpenAIEmbeddingProvider,
)
from knowledge.indexing.knowledge_indexer import KnowledgeIndexer
from knowledge.loaders.pdf_loader import PDFLoader
from common.factories.vectorstore_factory import VectorStoreFactory

###############################################################################
def test_faiss_persistence():
    #
    # Create a fresh vector store.
    #
    provider = OpenAIEmbeddingProvider()
    embedding_engine = EmbeddingEngine(
        provider=provider,
    )
    vector_store = VectorStoreFactory.create()
    loader = PDFLoader()
    chunker = RecursiveChunker()
    indexer = KnowledgeIndexer(
        loader=loader,
        chunker=chunker,
        embedding_engine=embedding_engine,
        vector_store=vector_store,
    )

    #
    # Index a sample PDF.
    #
    count = indexer.index_file(
        "samples/pdfs/employee_handbook.pdf",
    )

    print(f"Indexed {count} chunks.")

    assert count > 0

    #
    # Save the index.
    #
    folder = Path("data/knowledge_index")

    vector_store.save(folder)

    print("Vector store saved.")

    #
    # Create a NEW vector store.
    #
    new_store = VectorStoreFactory.create()

    new_store.load(folder)

    print("Vector store loaded.")

    #
    # Basic verification.
    #
    assert len(new_store.embeddings) == len(vector_store.embeddings)

    print(f"Embeddings restored : {len(new_store.embeddings)}")

    # Verify that the loaded index is usable.
    results = new_store.search(
        query_embedding=vector_store.embeddings[0],
        k=3,
    )

    print(f"Retrieved {len(results)} results.")
    assert len(results) > 0

if __name__ == "__main__":
    test_faiss_persistence()
