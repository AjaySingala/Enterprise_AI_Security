"""
===============================================================================
Run:
python -m tests.knowledge.test_text_loader
===============================================================================
"""

from pathlib import Path

from knowledge.loaders.text_loader import TextLoader

def main():
    loader = TextLoader()
    document = loader.load(
        Path("data/text/rag_intro.txt")
    )

    print()
    print("=" * 80)
    print("Document")
    print("=" * 80)
    
    print(f"ID        : {document.document_id}")
    print(f"Source    : {document.source}")
    print(f"Characters: {len(document.content)}")
    print(f"Metadata  : {document.metadata}")
    print()
    print(document.content[:500])

if __name__ == "__main__":
    main()
