"""
Run:
python -m tests.knowledge.test_splitter
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

print("Creating splitter...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)

print("Splitting...")

chunks = splitter.split_text(
    "Hello world " * 200
)

print(len(chunks))
