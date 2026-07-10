"""
===============================================================================
Build Knowledge Index
===============================================================================
"""

from pathlib import Path

from common.factories.vectorstore_factory import VectorStoreFactory

from knowledge.chunking.recursive_chunker import RecursiveChunker
from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.embeddings.openai_embedding_provider import (
    OpenAIEmbeddingProvider,
)
from knowledge.indexing.knowledge_indexer import KnowledgeIndexer
from knowledge.loaders.pdf_loader import PDFLoader

###############################################################################
def main():
    print()
    print("=" * 70)
    print("Building Knowledge Index")
    print("=" * 70)

    #
    # Services
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
    # Find PDF files.
    #
    pdf_folder = Path("samples/pdfs")

    pdf_files = sorted(
        pdf_folder.glob("*.pdf")
    )

    print()
    print(f"Found {len(pdf_files)} PDF files.")

    #
    # Index them.
    #
    total_chunks = indexer.index_files(
        pdf_files,
    )

    #
    # Save the vector store.
    #
    vector_store.save(
        "data/knowledge_index",
    )

    print()
    print(f"Indexed {total_chunks} chunks.")
    print()
    print("Knowledge index saved successfully.")


###############################################################################
if __name__ == "__main__":
    main()
