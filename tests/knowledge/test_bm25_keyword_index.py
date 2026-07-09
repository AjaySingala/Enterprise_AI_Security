"""
Run:
python -m tests.knowledge.test_bm25_keyword_index
"""
from knowledge.chunking.chunk import Chunk
from knowledge.keyword.bm25_keyword_index import BM25KeywordIndex

###############################################################################
def test_bm25_keyword_index():
    index = BM25KeywordIndex()
    chunks = [
        Chunk(
            document_id="doc1",
            chunk_index=0,
            content="Python supports object oriented programming.",
        ),
        Chunk(
            document_id="doc2",
            chunk_index=0,
            content="Retrieval Augmented Generation uses vector databases.",
        ),
        Chunk(
            document_id="doc3",
            chunk_index=0,
            content="Artificial Intelligence is transforming software.",
        ),
    ]

    index.add(
        chunks,
    )

    print()
    print(
        f"Indexed Chunks : {index.count()}"
    )

    results = index.search(
        "retrieval generation",
        k=3,
    )

    print()
    print("Results")
    print("-------")

    for result in results:
        print(
            result.rank,
            result.score,
            result.chunk.document_id,
            result.chunk.content,
        )

    assert len(results) >= 1
    assert (
        results[0]
        .chunk
        .document_id
        == "doc2"
    )

if __name__ == "__main__":
    test_bm25_keyword_index()
