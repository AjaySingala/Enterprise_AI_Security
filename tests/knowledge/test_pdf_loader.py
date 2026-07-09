"""
Run:
python -m tests.knowledge.test_pdf_loader
"""
from knowledge.loaders.pdf_loader import PDFLoader

def test_pdf_loader():
    loader = PDFLoader()

    document = loader.load(
        "samples/pdfs/sample.pdf",
    )

    print(document.document_id)
    print(document.metadata.page_count)
    print(len(document.pages))
    print(document.content[:500])

    assert document.metadata.page_count > 0
    assert len(document.pages) == document.metadata.page_count
    assert len(document.content) > 0

if __name__ == "__main__":
    test_pdf_loader()
