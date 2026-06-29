from common.llm import llm

response = llm.generate_json(

    system_prompt="""
Return ONLY JSON.
{
    "language":"Python",
    "version":"3.13"
}
""",

    user_prompt="Return the JSON."
)

print()
print(type(response))
print()
print(response)
print()
print(response["language"])
