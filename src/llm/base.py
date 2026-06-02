from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CCTPParams:
    lot_numero: str
    lot_nom: str
    type_projet: str
    usage: str
    zone_climatique: str
    zone_sismique: str
    pmr: bool
    specificites: str = ""
    type_erp: str = ""


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
