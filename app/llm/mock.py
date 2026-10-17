from app.llm.base import LLMProvider

class MockLLMProvider(LLMProvider):
    def generate(self, prompt: str, max_new_tokens: int = 50) -> str:
        return f"Mock LLM response: Received a prompt of {len(prompt)} characters."
