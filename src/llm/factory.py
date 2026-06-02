from typing import Literal
from src.llm.base import BaseLLMProvider
from src.config import settings


def get_provider(provider: Literal["claude", "mistral"] | None = None) -> BaseLLMProvider:
    chosen = provider or settings.default_llm_provider

    if chosen == "claude":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY manquante dans .env")
        from src.llm.claude import ClaudeProvider
        return ClaudeProvider()

    if chosen == "mistral":
        if not settings.mistral_api_key:
            raise ValueError("MISTRAL_API_KEY manquante dans .env")
        from src.llm.mistral import MistralProvider
        return MistralProvider()

    raise ValueError(f"Fournisseur inconnu : {chosen}. Valeurs acceptées : 'claude', 'mistral'")
