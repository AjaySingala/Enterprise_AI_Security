from __future__ import annotations

from openai import OpenAI

from config.config import settings
from common.tracing.trace_decorator import trace

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding import Embedding
from knowledge.embeddings.embedding_provider import EmbeddingProvider

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.api_key,
        )
        self.model = settings.text_embedding_model

    ##########################################################################
    @trace
    def embed(
        self,
        chunk: Chunk,
    ) -> Embedding:
        response = self.client.embeddings.create(
            model=self.model,
            input=chunk.content,
        )

        item = response.data[0]

        usage = getattr(
            response,
            "usage",
            None,
        )

        return Embedding(
            chunk=chunk,
            vector=item.embedding,
            model=self.model,
            input_tokens=(
                usage.prompt_tokens
                if usage
                else 0
            ),
        )

    ##########################################################################
    @trace
    def embed_batch(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        if not chunks:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=[
                chunk.content
                for chunk in chunks
            ],
        )

        usage = getattr(
            response,
            "usage",
            None,
        )

        embeddings = []

        for chunk, item in zip(
            chunks,
            response.data,
        ):
            embeddings.append(
                Embedding(
                    chunk=chunk,
                    vector=item.embedding,
                    model=self.model,
                    input_tokens=(
                        usage.prompt_tokens
                        if usage
                        else 0
                    ),
                )
            )

        return embeddings
    