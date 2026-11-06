import pytest

from app.llm.service import create_llm_service


def test_mock_is_default(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    service = create_llm_service()

    assert type(service.provider).__name__ == "MockLLMProvider"


def test_explicit_mock(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")

    service = create_llm_service()

    assert type(service.provider).__name__ == "MockLLMProvider"


def test_openai_provider_selection(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    service = create_llm_service()

    assert type(service.provider).__name__ == "OpenAIProvider"


def test_invalid_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "unknown")

    with pytest.raises(ValueError, match="Unsupported"):
        create_llm_service()
