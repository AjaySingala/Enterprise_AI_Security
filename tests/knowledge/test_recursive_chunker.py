"""
===============================================================================
Run:
python -m tests.knowledge.test_recursive_chunker
===============================================================================
"""
from pathlib import Path

from knowledge.chunking.recursive_chunker import RecursiveChunker
from knowledge.loaders.text_loader import TextLoader

def main():
    loader = TextLoader()

    document = loader.load(
        Path("data/text/rag_intro.txt")
    )

    chunker = RecursiveChunker(
        chunk_size=200,
        chunk_overlap=40,
    )

    chunks = chunker.chunk(
        document
    )

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
