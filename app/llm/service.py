from app.llm.base import LLMProvider
from app.llm.mock import MockLLMProvider

class LLMService:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(self, prompt: str, max_new_tokens: int = 50) -> dict:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        if not 1 <= max_new_tokens <= 200:
            raise ValueError("Invalid output token limit")
        response = self.provider.generate(prompt=prompt, max_new_tokens=max_new_tokens)
        return {"provider": type(self.provider).__name__, "response": response, "max_new_tokens": max_new_tokens}

llm_service = LLMService(MockLLMProvider())
