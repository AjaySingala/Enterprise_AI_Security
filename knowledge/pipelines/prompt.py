from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Prompt:
    system_prompt: str
    user_prompt: str
    full_prompt: str
