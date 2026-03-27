"""
Application configuration via Pydantic Settings.
Reads from .env file in the backend root directory.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────
    DATABASE_URL: str  # e.g. postgresql+asyncpg://user:pass@host:5432/db

    # ── Plaid ─────────────────────────────────────────────────
    PLAID_CLIENT_ID: str = ""
    PLAID_SECRET: str = ""
    PLAID_ENV: str = "sandbox"  # sandbox | development | production

    # ── Gemini ────────────────────────────────────────────────
    GEMINI_API_KEY: str = ""

    # ── Frontend ──────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"


settings = Settings()  # type: ignore[call-arg]
