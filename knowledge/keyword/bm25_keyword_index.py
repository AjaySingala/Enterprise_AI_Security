from knowledge.chunking.chunk import Chunk
from knowledge.keyword.base_keyword_index import BaseKeywordIndex

class BM25KeywordIndex(BaseKeywordIndex):
    def __init__(self):
        self._chunks: list[Chunk] = []
        self._documents: list[list[str]] = []
        self._bm25 = None
