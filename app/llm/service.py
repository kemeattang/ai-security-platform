import os

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

        response = self.provider.generate(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
        )

        return {
            "provider": type(self.provider).__name__,
            "response": response,
            "max_new_tokens": max_new_tokens,
        }


def create_llm_service() -> LLMService:
    provider_name = os.getenv("LLM_PROVIDER", "mock").lower().strip()

    if provider_name == "mock":
        provider = MockLLMProvider()

    elif provider_name == "openai":
        from app.llm.openai_provider import OpenAIProvider

        provider = OpenAIProvider(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: {provider_name}"
        )

    return LLMService(provider)


llm_service = create_llm_service()
