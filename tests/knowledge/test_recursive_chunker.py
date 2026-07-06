"""
===============================================================================
Run:
python -m tests.knowledge.test_recursive_chunker
===============================================================================
"""
print("Module loading...")
from pathlib import Path

from knowledge.chunking.recursive_chunker import RecursiveChunker
from knowledge.loaders.text_loader import TextLoader

def main():
    print("Starting...")
    loader = TextLoader()

    print("Loading document...")
    document = loader.load(
        Path("data/text/rag_intro.txt")
    )
    print("Document loaded...")

    chunker = RecursiveChunker(
        chunk_size=200,
        chunk_overlap=40,
    )
    print("Chunker created...")

    chunks = chunker.chunk(
        document
    )
    print("Chunking complete...")

    print()

    print("=" * 80)
    print("Chunking Test")
    print("=" * 80)

    print(f"Document ID : {document.document_id}")
    print(f"Chunks      : {len(chunks)}")

    print()

    for chunk in chunks:
        print("-" * 80)
        print(f"Chunk #{chunk.chunk_number}")
        print(f"Chunk ID : {chunk.chunk_id}")
        print(f"Length   : {len(chunk.content)}")
        print()
        print(chunk.content)
        print()

if __name__ == "__main__":
    main()
