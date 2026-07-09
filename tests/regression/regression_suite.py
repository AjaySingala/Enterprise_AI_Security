"""
Enterprise AI Framework
Regression Suite
"""

# List all Test files in the "tests" folder:
# dir /b /s /a:-d | findstr /v /i "\__init__.py$ \.pyc$ \\__pycache__\\"

from __future__ import annotations

from dataclasses import dataclass

###############################################################################
# Test Case
###############################################################################
@dataclass(slots=True, frozen=True)
class TestCase:
    module: str
    category: str
    level: str
    estimated_seconds: int = 5

###############################################################################
# Regression Suite
###############################################################################
TESTS = [
    ###########################################################################
    # LLM SDK
    ###########################################################################
    TestCase(
        module="tests.llms.test_llm",
        category="LLM SDK",
        level="Component",
    ),
    TestCase(
        module="tests.llms.test_llm_json",
        category="LLM SDK",
        level="Component",
    ),
    TestCase(
        module="tests.llms.test_stream_chat",
        category="LLM SDK",
        level="Integration",
    ),

    ###########################################################################
    # Knowledge SDK
    ###########################################################################
    TestCase(
        module="tests.knowledge.test_text_loader",
        category="Knowledge SDK",
        level="Loader",
    ),
    TestCase(
        module="tests.knowledge.test_chunker",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_recursive_chunker",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_embedding_model",
        category="Knowledge SDK",
        level="Unit",
    ),
    TestCase(
        module="tests.knowledge.test_embedding_engine",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_batch_embeddings",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_faiss_vectorstore",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_vector_store_inspector",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_retriever",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_prompt_builder",
        category="Knowledge SDK",
        level="Component",
    ),
    TestCase(
        module="tests.knowledge.test_knowledge_pipeline",
        category="Knowledge SDK",
        level="Integration",
    ),
    TestCase(
        module="tests.knowledge.test_metadata_filter",
        category="Knowledge SDK",
        level="Integration",
    ),
    TestCase(
        module="tests.knowledge.test_pdf_loader",
        category="Knowledge SDK",
        level="Loader",
    ),

    ###########################################################################
    # PII
    ###########################################################################
    TestCase(
        module="tests.pii.test_pii_detector",
        category="PII",
        level="Component",
    ),
    TestCase(
        module="tests.pii.test_pii_masker",
        category="PII",
        level="Component",
    ),
    TestCase(
        module="tests.pii.test_pii_engine",
        category="PII",
        level="Integration",
    ),

    ###########################################################################
    # Prompt Injection
    ###########################################################################
    TestCase(
        module="tests.prompt_injection.test_classifier",
        category="Prompt Injection",
        level="Component",
    ),
    TestCase(
        module="tests.prompt_injection.test_detector",
        category="Prompt Injection",
        level="Component",
    ),
    TestCase(
        module="tests.prompt_injection.test_engine",
        category="Prompt Injection",
        level="Integration",
    ),

    ###########################################################################
    # Secrets
    ###########################################################################
    TestCase(
        module="tests.secrets.test_detector",
        category="Secrets",
        level="Component",
    ),
    TestCase(
        module="tests.secrets.test_entropy",
        category="Secrets",
        level="Unit",
    ),
    TestCase(
        module="tests.secrets.test_masker",
        category="Secrets",
        level="Component",
    ),
    TestCase(
        module="tests.secrets.test_engine",
        category="Secrets",
        level="Integration",
    ),

    ###########################################################################
    # Confidential
    ###########################################################################
    TestCase(
        module="tests.confidential.test_detector",
        category="Confidential",
        level="Component",
    ),
    TestCase(
        module="tests.confidential.test_masker",
        category="Confidential",
        level="Component",
    ),
    TestCase(
        module="tests.confidential.test_engine",
        category="Confidential",
        level="Integration",
    ),

    ###########################################################################
    # Applications
    ###########################################################################
    TestCase(
        module="tests.secure_chat.test_stream_chat_engine",
        category="Applications",
        level="Integration",
    ),
]
