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

        search_start = 0
        chunks: list[Chunk] = []

        for index, piece in enumerate(pieces):
            #
            # Find where this chunk occurs in the original document.
            #
            position = document.content.find(
                piece,
                search_start,
            )

            if position == -1:
                position = search_start

            search_start = position + len(piece)

            #
            # Determine the page number.
            #
            page_number = None

            if document.page_offsets:
                page_number = self._find_page_number(
                    position,
                    document.page_offsets,
                )

            chunks.append(
                Chunk(
                    document_id=document.document_id,
                    content=piece,
                    chunk_index=index,
                    page_number=page_number,
                    metadata=document.metadata,
                )
            )

        return chunks
    
    ###############################################################################
    def _find_page_number(
        self,
        position: int,
        page_offsets: list[int],
    ) -> int:
        """
        Determine which PDF page contains a character position.
        """
        page_number = 1

        for index, offset in enumerate(page_offsets):
            if position < offset:
                break

            page_number = index + 1

        return page_number
    