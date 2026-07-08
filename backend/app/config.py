from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-First CRM HCP Module"
    environment: str = "development"
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="gemma2-9b-it", alias="GROQ_MODEL")
    groq_context_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_CONTEXT_MODEL")
    frontend_origin: str = Field(default="http://localhost:5173", alias="FRONTEND_ORIGIN")

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("frontend_origin")
    @classmethod
    def clean_origin(cls, value: str) -> str:
        return value.rstrip("/")

    @field_validator("database_url", mode="before")
    @classmethod
    def clean_database_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        database_url = str(value).strip()
        if not database_url:
            return None
        if "postgresql://" in database_url:
            database_url = database_url[database_url.index("postgresql://") :]
        elif "postgres://" in database_url:
            database_url = database_url[database_url.index("postgres://") :]
        database_url = database_url.strip("'\"")
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_origin, "http://127.0.0.1:5173", "http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
