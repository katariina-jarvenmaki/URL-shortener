# app/core/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "URL Shortener"
    allowed_hosts: List[str] = ["*"]
    database_url: str

    # Server settings
    host: str = "0.0.0.0"
    port: int = 9995
    base_url: str = "http://localhost:9995"

    # Debug flag
    debug: bool = True
    
    # Optional future extensions
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Cached singleton-style access
@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Global settings instance
settings = get_settings()