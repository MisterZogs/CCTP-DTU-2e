import anthropic
from src.llm.base import BaseLLMProvider
from src.config import settings


class ClaudeProvider(BaseLLMProvider):
    def __init__(self):
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._model = settings.claude_model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        message = await self._client.messages.create(
            model=self._model,
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text

    @property
    def provider_name(self) -> str:
        return "claude"

    @property
    def model_name(self) -> str:
        return self._model
