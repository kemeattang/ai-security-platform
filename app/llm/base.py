from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_new_tokens: int = 50) -> str:
        raise NotImplementedError
