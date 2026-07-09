"""
Run:
python -m tests.knowledge.test_knowledge_indexer
"""
from common.factories.vectorstore_factory import VectorStoreFactory
from knowledge.chunking.recursive_chunker import RecursiveChunker
from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.embeddings.openai_embedding_provider import OpenAIEmbeddingProvider
from knowledge.indexing.knowledge_indexer import KnowledgeIndexer
from knowledge.loaders.pdf_loader import PDFLoader

loader = PDFLoader()
chunker = RecursiveChunker()
provider = OpenAIEmbeddingProvider()
embedding_engine = EmbeddingEngine(
    provider=provider,
)
vector_store = VectorStoreFactory.create()
indexer = KnowledgeIndexer(
    loader=loader,
    chunker=chunker,
    embedding_engine=embedding_engine,
    vector_store=vector_store,
)

count = indexer.index_file(
    "samples/pdfs/employee_handbook.pdf",
)

print(f"Indexed {count} chunks.")

assert count > 0
assert vector_store.count() == count
