"""
===============================================================================
Enterprise AI Gateway (EAIG)

Knowledge SDK

Recursive Chunker

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge.chunking.base_chunker import BaseChunker
from knowledge.chunking.chunk import Chunk
from knowledge.loaders.document import Document

from common.tracing.trace_decorator import trace

###############################################################################
# Recursive Chunker
###############################################################################
class RecursiveChunker(BaseChunker):
    ###########################################################################
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    ###########################################################################
    @trace
    def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:
        pieces = self._splitter.split_text(
            document.content
        )

        chunks: list[Chunk] = []

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    document_id=document.document_id,
                    content=piece,
                    chunk_index=index + 1,
                    metadata={
                        "source": str(document.source),
                        "loader": document.metadata.get(
                            "loader"
                        ),
                    },
                )
            )

        return chunks
    