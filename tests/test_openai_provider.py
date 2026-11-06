import pytest
from types import SimpleNamespace
from unittest.mock import Mock

from app.llm.openai_provider import (
    OpenAIProvider,
    LLMProviderError,
)
from app.llm.service import LLMService


def make_provider(text="Hello from OpenAI"):
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(
        output_text=text
    )
    return OpenAIProvider(client=client), client


def test_successful_generation():
    provider, client = make_provider()
    result = provider.generate("Hello", max_new_tokens=50)

    assert result == "Hello from OpenAI"
    client.responses.create.assert_called_once_with(
        model="gpt-4.1-mini",
        input="Hello",
        max_output_tokens=50,
        store=False,
    )


def test_custom_model():
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(
        output_text="Custom model response"
    )

    provider = OpenAIProvider(
        client=client,
        model="test-model",
    )

    assert provider.generate("Hello") == "Custom model response"
    assert client.responses.create.call_args.kwargs["model"] == "test-model"


def test_empty_prompt_rejected():
    provider, client = make_provider()

    with pytest.raises(ValueError):
        provider.generate("   ")

    client.responses.create.assert_not_called()


@pytest.mark.parametrize("limit", [0, 201, -1, True, "50"])
def test_invalid_token_limit(limit):
    provider, client = make_provider()

    with pytest.raises(ValueError):
        provider.generate("Hello", max_new_tokens=limit)

    client.responses.create.assert_not_called()


def test_empty_model_response():
    provider, _ = make_provider("")

    with pytest.raises(LLMProviderError, match="no usable text"):
        provider.generate("Hello")


def test_provider_error_is_sanitized():
    provider, client = make_provider()
    client.responses.create.side_effect = RuntimeError(
        "Sensitive provider diagnostic"
    )

    with pytest.raises(LLMProviderError) as error:
        provider.generate("Hello")

    assert "Sensitive provider diagnostic" not in str(error.value)
    assert error.value.__cause__ is None


def test_service_integration():
    provider, _ = make_provider("Secure response")
    service = LLMService(provider)

    result = service.generate(
        "Explain Kubernetes security",
        max_new_tokens=40,
    )

    assert result["provider"] == "OpenAIProvider"
    assert result["response"] == "Secure response"
    assert result["max_new_tokens"] == 40


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="not configured"):
        OpenAIProvider()


def test_invalid_model_name():
    with pytest.raises(ValueError):
        OpenAIProvider(client=Mock(), model=" ")
