# app/core/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "URL Shortener API"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    base_url: str = "http://localhost:8000"

    # Database
    database_url: str = "sqlite:///./urls.db"

    # Optional future extensions
    allowed_hosts: list[str] = ["*"]
    rate_limit_per_minute: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Singleton-style access
settings = get_settings()