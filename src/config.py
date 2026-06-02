from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./cctp.db"

    anthropic_api_key: str = ""
    mistral_api_key: str = ""

    claude_model: str = "claude-sonnet-4-6"
    mistral_model: str = "mistral-large-latest"

    default_llm_provider: Literal["claude", "mistral"] = "mistral"

    chroma_persist_dir: str = "./chroma_data"
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    rag_n_results: int = 5


settings = Settings()
