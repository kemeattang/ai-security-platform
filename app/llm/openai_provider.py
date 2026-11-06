import os

from app.llm.base import LLMProvider


class LLMProviderError(RuntimeError):
    """A sanitized error safe for application-level handling."""


class OpenAIProvider(LLMProvider):
    def __init__(
        self,
        client=None,
        model: str = "gpt-4.1-mini",
    ):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("Model name is required")

        self.model = model

        if client is not None:
            self.client = client
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY is not configured"
                )

            from openai import OpenAI

            self.client = OpenAI(
                api_key=api_key,
                timeout=20.0,
                max_retries=1,
            )

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 50,
    ) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        if (
            isinstance(max_new_tokens, bool)
            or not isinstance(max_new_tokens, int)
            or not 1 <= max_new_tokens <= 200
        ):
            raise ValueError("Invalid output token limit")

        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                max_output_tokens=max_new_tokens,
                store=False,
            )

            text = response.output_text

            if not isinstance(text, str) or not text.strip():
                raise LLMProviderError(
                    "Model returned no usable text"
                )

            return text

        except LLMProviderError:
            raise
        except Exception:
            raise LLMProviderError(
                "LLM provider request failed"
            ) from None
