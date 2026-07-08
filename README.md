# Enterprise AI Gateway (EAIG)

# To install packages:
python -m pip install -r requirements.txt

# Why __init__.py?

It tells Python that the directory should be treated as a package (or explicitly marks it as one). While modern Python (3.3+) supports implicit namespace packages in many cases, including __init__.py is still a good practice for a structured project like ours because it:

Makes imports more predictable.
Lets you control what the package exports.
Allows package-level initialization if needed.
Improves compatibility with tools, IDEs, linters, and some packaging workflows.

# Demo 1 (Feature 1: Prompt Injection): demo01_prompt_injection.py
# Run from root folder:
python -m demos.demo01_prompt_injection

# Check OPENAI SDK version.
python -c "import openai; print(openai.__version__)"

# Run Regression Tests:
python -m tests.run_regression
python -m tests.run_regression
python -m tests.run_regression --verbose
python -m tests.run_regression -v
python -m tests.run_regression --quite
python -m tests.run_regression -q

# Run individual tests:
## Featuer 0: LLMs:
python -m tests.llms.test_llm
python -m tests.llms.test_llm_json

# Feature 1: Prompt Injection Detection:
python -m tests.prompt_injection.test_detector
python -m tests.prompt_injection.test_classifier
python -m tests.prompt_injection.test_engine

# Feature 2: PII Detection:
python -m tests.pii.test_pii_detector
python -m tests.pii.test_pii_masker
python -m tests.pii.test_pii_engine

# Feature 3: Secret Detection:
python -m tests.secrets.test_entropy
python -m tests.secrets.test_detector
python -m tests.secrets.test_masker
python -m tests.secrets.test_engine

# Feature 4: Confidential Data Detection:
python -m tests.confidential.test_detector
python -m tests.confidential.test_masker
python -m tests.confidential.test_engine

# Feature 5: Secure Chat:
python -m tests.secure_chat.test_stream_chat_engine
python -m tests.llms.test_stream_chat

# Feature 6: Knowledge Base and Chunking:
python -m tests.knowledge.test_text_loader
python -m tests.knowledge.test_chunker
python -m tests.knowledge.test_recursive_chunker

# If there is an spaCy related error, uninstall and reinstall spaCy:
pip uninstall spacy
pip install --no-cache-dir spacy==3.8.13

# Feture 7: Embeddings:
python -m tests.knowledge.test_embedding_model
python -m tests.knowledge.test_embedding_engine

# Feature 8: Batch Embeddings
python -m tests.knowledge.test_batch_embeddings
python -m tests.knowledge.test_prompt_builder


# Feature 9: Vector Store Abstraction and FAISS Vector Store.
python -m tests.knowledge.test_faiss_vectorstore
python -m tests.knowledge.test_vector_store_inspector

# Feature 10: Retrieval.
python -m tests.knowledge.test_retriever

# Feature 10: Knowledge Pipeline.
python -m tests.knowledge.test_knowledge_pipeline

