"""
Instead of:
---
100 Chunks
↓
100 OpenAI API Calls
↓
100 HTTPS Connections

We do:
---
100 Chunks
↓
1 OpenAI API Call
↓
100 Embeddings

Run:
python -m tests.knowledge.test_batch_embeddings
"""
from time import perf_counter

from knowledge.chunking.chunk import Chunk
from knowledge.embeddings.embedding_engine import EmbeddingEngine
from knowledge.embeddings.openai_embedding_provider import OpenAIEmbeddingProvider

def main():
    chunks = [
        Chunk(
            document_id="doc-001",
            content="Retrieval Augmented Generation",
            chunk_index=0,
        ),

        Chunk(
            document_id="doc-001",
            content="Vector databases store embeddings.",
            chunk_index=1,
        ),

        Chunk(
            document_id="doc-001",
            content="Prompt injection is a security risk.",
            chunk_index=2,
        ),

    ]

    provider = OpenAIEmbeddingProvider()
    engine = EmbeddingEngine(
        provider=provider,
    )

    ###########################################################################
    # Individual Embeddings
    ###########################################################################
    print()
    print("=" * 80)
    print("INDIVIDUAL EMBEDDINGS")
    print("=" * 80)

    start = perf_counter()
    single_embeddings = []

    for chunk in chunks:
        embedding = engine.embed(chunk)      # Can use embed() as well.
        single_embeddings.append(embedding)

    single_elapsed = (perf_counter() - start) * 1000

    print()
    print(f"Generated : {len(single_embeddings)} embeddings")
    print(f"Time      : {single_elapsed:.2f} ms")
    print()

    ###########################################################################
    # Batch Embeddings
    ###########################################################################
    print("=" * 80)
    print("BATCH EMBEDDINGS")
    print("=" * 80)

    start = perf_counter()
    
    batch_embeddings = engine.embed_batch(chunks)

    batch_elapsed = (perf_counter() - start) * 1000

    print()
    print(f"Generated : {len(batch_embeddings)} embeddings")
    print(f"Time      : {batch_elapsed:.2f} ms")
    print()

    ###########################################################################
    # Comparison
    ###########################################################################

    print("=" * 80)
    print("COMPARISON")
    print("=" * 80)
    print()

    for i, (single, batch) in enumerate(
        zip(single_embeddings, batch_embeddings),
        start=1,
    ):
        print(f"Chunk {i}")
        print(
            f"  Dimensions     : {single.dimensions}"
        )
        print(
            f"  Vector Length  : {len(single.vector)}"
        )
        print(
            f"  Same Dimension : {single.dimensions == batch.dimensions}"
        )

        #
        # Compare the vectors.
        #
        identical = single.vector == batch.vector
        print(
            f"  Same Vector    : {identical}"
        )
        print()

    print("=" * 80)
    print(f"Individual : {single_elapsed:.2f} ms")
    print(f"Batch      : {batch_elapsed:.2f} ms")

    if batch_elapsed > 0:
        speedup = single_elapsed / batch_elapsed
        print(f"Speed-up   : {speedup:.2f}x")

    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
