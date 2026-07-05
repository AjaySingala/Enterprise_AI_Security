"""
===============================================================================
Test : Streaming Chat

Run:
python -m tests.llms.test_stream_chat
===============================================================================
"""

from common.llm import llm

def main():
    messages = [
        {
            "role": "user",
            "content": "Tell me a joke about Python.",
        }
    ]

    print()
    print("=" * 80)
    print("Streaming Response")
    print("=" * 80)
    print()

    generator = llm.stream_chat(messages)
    try:
        while True:
            token = next(generator)
            print(
                token,
                end="",
                flush=True,
            )

    except StopIteration as result:
        response = result.value

    print()
    print()
    print("=" * 80)
    print("Statistics")
    print("=" * 80)

    print(f"Model          : {response.model}")
    print(f"Request ID     : {response.request_id}")
    print(f"Input Tokens   : {response.input_tokens}")
    print(f"Output Tokens  : {response.output_tokens}")
    print(f"Total Tokens   : {response.total_tokens}")
    print(f"Elapsed Time   : {response.elapsed_time} sec")

if __name__ == "__main__":
    main()
