"""
===============================================================================
Run:
python -m tests.llms.test_llm
===============================================================================
"""
from common.llm import llm

response = llm.generate(

    system_prompt="Reply with exactly the word Hello.",

    user_prompt="Say hello."

)

print()

print("TEXT")
print(response.text)

print()

print("MODEL")
print(response.model)

print()

print("REQUEST ID")
print(response.request_id)

print()

print("INPUT TOKENS")
print(response.input_tokens)

print()

print("OUTPUT TOKENS")
print(response.output_tokens)

print()

print("TOTAL TOKENS")
print(response.total_tokens)

print()

print("TIME")
print(response.elapsed_time)
