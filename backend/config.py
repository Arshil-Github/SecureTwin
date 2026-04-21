# backend/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Literal
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./securewealth.db"
    AI_PROVIDER: Literal["claude", "gemini"] = "claude"
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    SECRET_KEY: str = "your-secret-key-for-jwt"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATA_SOURCE: Literal["mock", "live"] = "mock"
    CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
