"""
app/config.py
─────────────────────────────────────────────────────────────────
Application settings loaded from environment variables / .env file.

Why Pydantic Settings?
  - Type-safe environment variable parsing
  - Automatic validation (raises on startup if a required var is missing)
  - Cached singleton via @lru_cache → read .env once, reuse everywhere
─────────────────────────────────────────────────────────────────
"""
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, field_validator


class Settings(BaseSettings):
    # ── Application ─────────────────────────────────────────
    APP_NAME: str = "HealthGuard AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"           # development | staging | production

    # ── Database ─────────────────────────────────────────────
    DATABASE_URL: str                          # postgresql://user:pass@host:port/db

    # ── Security / JWT ────────────────────────────────────────
    SECRET_KEY: str                            # openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ─────────────────────────────────────────────────
    # Stored as comma-separated string in .env, parsed to list
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v: str) -> str:
        return v  # kept as string; split in property below

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    # ── AWS S3 (Phase 8) ──────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "healthguard-reports"

    # ── Logging ───────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton of the application settings."""
    return Settings()


# Module-level convenience alias
settings = get_settings()
