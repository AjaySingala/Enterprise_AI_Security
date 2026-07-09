"""
What is BM25?

BM25 (Best Matching 25) is the most widely used keyword ranking algorithm in Information Retrieval.

When you search:
"retrieval augmented generation"

BM25 ranks documents based on how relevant they are to those keywords.

Unlike vector search, it does not use embeddings or AI.

It simply looks at:
- Which words appear
- How often they appear
- How rare/common those words are
- How long the document is

---
What is BM25Okapi?
BM25Okapi is the Python implementation of the BM25 algorithm provided by the rank-bm25 library.

Install:
pip install rank-bm25
"""

import re

from common.tracing.trace_decorator import trace
from knowledge.chunking.chunk import Chunk
from knowledge.keyword.base_keyword_index import BaseKeywordIndex

from rank_bm25 import BM25Okapi

class BM25KeywordIndex(BaseKeywordIndex):
    def __init__(self):
        self._chunks: list[Chunk] = []
        self._documents: list[list[str]] = []
        self._bm25 = None

###############################################################################
def _tokenize(
    self,
    text: str,
) -> list[str]:
    """
    Tokenize text for BM25.

    Version 1:
        - lowercase
        - remove punctuation
        - split on whitespace
    """
    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
    )

    return text.split()

###############################################################################
@trace
def add(
    self,
    chunks: list[Chunk],
) -> None:
    """
    Add chunks to the BM25 index.
    """
    for chunk in chunks:
        self._chunks.append(chunk)
        self._documents.append(
            self._tokenize(
                chunk.content,
            )
        )

    self._bm25 = BM25Okapi(
        self._documents,
    )

###############################################################################
def count(
    self,
) -> int:
    return len(
        self._chunks,
    )

###############################################################################
def clear(
    self,
) -> None:
    self._chunks.clear()
    self._documents.clear()
    self._bm25 = None
