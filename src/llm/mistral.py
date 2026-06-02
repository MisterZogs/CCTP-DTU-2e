from mistralai import Mistral
from src.llm.base import BaseLLMProvider
from src.config import settings


class MistralProvider(BaseLLMProvider):
    def __init__(self):
        self._client = Mistral(api_key=settings.mistral_api_key)
        self._model = settings.mistral_model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = await self._client.chat.complete_async(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content

    @property
    def provider_name(self) -> str:
        return "mistral"

    @property
    def model_name(self) -> str:
        return self._model
