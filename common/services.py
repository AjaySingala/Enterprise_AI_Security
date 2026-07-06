"""
===============================================================================
Enterprise AI Gateway (EAIG)

Service Registry

Version:
    1.0.0

Python:
    3.13.11

Rules:
| ------------------ | ----------------------- | ---------------------- |
| Layer              | Can construct objects?  | Can import `services`? |
| ------------------ | ----------------------- | ---------------------- |
| common/services.py | ✅ Yes                  | N/A                   |
| applications       | ❌ No                   | ✅ Yes                |
| api                | ❌ No                   | ✅ Yes                |
| tests              | ❌ No                   | ✅ Yes                |
| knowledge          | ❌ No                   | ❌ Never              |
| security           | ❌ No                   | ❌ Never              |
===============================================================================
"""

from __future__ import annotations

from common.metrics import MetricsService
from common.audit import AuditService
from common.llm import LLM

from security.pipeline.pipeline_engine import SecurityPipeline

from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.vectorstores.faiss_vectorstore import FAISSVectorStore
from knowledge.retrieval.retriever import Retriever
from knowledge.pipelines.prompt_builder import PromptBuilder

###############################################################################
# Service Registry
###############################################################################
class ServiceRegistry:
    """
    Central registry for shared singleton services.
    """
    ###########################################################################
    def __init__(self):   
        self._pipeline = SecurityPipeline()
        self._metrics = MetricsService()
        self._audit = AuditService()
        self._llm = LLM()
        self._prompt_builder = PromptBuilder()

        self._initialize_knowledge()

    def _initialize_knowledge(self):
        self._embedding_engine = EmbeddingEngine()
        self._vector_store = FAISSVectorStore()
        self._retriever = Retriever(
            embedding_engine=self._embedding_engine,
            vector_store=self._vector_store,
        )

    ###########################################################################
    @property
    def pipeline(self) -> SecurityPipeline:
        return self._pipeline

    ###########################################################################
    @property
    def metrics(self) -> MetricsService:
        return self._metrics

    @property
    def audit(self) -> AuditService:

        return self._audit

    @property
    def llm(self) -> LLM:
        return self._llm

    @property
    def embedding_engine(self) -> EmbeddingEngine:
        return self._embedding_engine

    @property
    def vector_store(self) -> FAISSVectorStore:
        return self._vector_store

    @property
    def retriever(self):
        return self._retriever
    
    @property
    def prompt_builder(self):
        return self._prompt_builder

###############################################################################
# Singleton
###############################################################################
services = ServiceRegistry()
