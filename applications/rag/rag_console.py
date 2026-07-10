"""
===============================================================================
RAG Console

Run:
python -m applications.rag.rag_console
===============================================================================
"""

from common.services import services

###############################################################################
# Console display options.
###############################################################################

SHOW_CHUNK_NUMBER = True
SHOW_RELEVANCE_SCORE = True
SHOW_CONTEXT = True

###############################################################################
def format_context(
    text: str,
    max_length: int = 500,
) -> str:
    text = " ".join(
        text.split()
    )

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."

###############################################################################
def main():
    print()
    print("=" * 70)
    print("Enterprise RAG Console")
    print("=" * 70)

    #
    # Load persisted knowledge.
    #
    services.vector_store.load(
        "data/knowledge_index",
    )

    print()
    print("Knowledge base loaded.")
    print("Type 'exit' to quit.")

    while True:
        print()
        question = input("Question > ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            break

        response = services.knowledge_pipeline.ask(
            query=question,
        )

        print()
        print("-" * 70)
        print("Answer")
        print("-" * 70)

        print(response.llm_response.text)

        print()
        print(f"Elapsed : {response.elapsed_ms:.2f} ms")
        print()

        print("=" * 70)
        print("SOURCES USED")
        print("=" * 70)

        for index, result in enumerate(response.search_results, start=1):
            chunk = result.chunk

            print(type(chunk))
            print(chunk)
            print(vars(chunk) if hasattr(chunk, "__dict__") else "No __dict__")

            print()
            print(f"Source {index}")
            print("-" * 70)
            print(f"Document        : {chunk.metadata.filename}")

            if chunk.page_number is not None:
                print(f"Page            : {chunk.page_number}")

            #
            # Show chunk number only for debugging.
            #
            if SHOW_CHUNK_NUMBER:
                print(f"Chunk           : {chunk.chunk_index}")
            if SHOW_RELEVANCE_SCORE:
                print(f"Relevance Score : {result.score:.4f}")
            print()

            if SHOW_CONTEXT:
                print("Relevant Context")
                print("----------------")
                print(format_context(chunk.content,))

            print()
            print("=" * 70)

if __name__ == "__main__":
    main()

# Sample queries:
# What is the leave policy?
