"""
===============================================================================
Testing the Secure Chat application's streaming behavior

Run:
python -m tests.secure_chat.test_stream_chat_engine
===============================================================================
"""

from applications.secure_chat.chat_engine import ChatEngine
from applications.secure_chat.chat_models import StreamEventType

engine = ChatEngine()
generator = engine.stream_chat(
    "Explain Retrieval Augmented Generation."
    # "Tell me a dad joke"
)

chat_result = None

for event in generator:

    if event.event == StreamEventType.START:
        continue

    elif event.event == StreamEventType.TOKEN:

        print(
            event.data,
            end="",
            flush=True,
        )

    elif event.event == StreamEventType.COMPLETE:

        chat_result = event.data

print()
print()

print(f"Total Tokens : {chat_result.total_tokens}")
print(f"Input Tokens : {chat_result.input_tokens}")
print(f"Output Tokens: {chat_result.output_tokens}")
