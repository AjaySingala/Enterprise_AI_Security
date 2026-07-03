from applications.secure_chat.chat_engine import ChatEngine

engine = ChatEngine()
generator = engine.stream_chat(
    "Explain Retrieval Augmented Generation."
)

try:
    while True:
        token = next(generator)
        print(
            token,
            end="",
            flush=True,
        )
except StopIteration as result:
    chat_result = result.value

print()
print()
print(chat_result.total_tokens)
