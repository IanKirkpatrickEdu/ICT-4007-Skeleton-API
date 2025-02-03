"""App configuration file."""

import logging
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), "..", ".env")


class Settings(BaseSettings):
    """Application environment variables Settings object."""
    model_config = SettingsConfigDict(
        env_file=DOTENV,
        extra="ignore",
        str_strip_whitespace=True,
    )

    # General API Information to display
    API_NAME: str | None = "Denver University ICT-4007"
    API_VERSION: str | None = "0.1.0"
    API_DESCRIPTION: str | None = "Example API starter for ICT-4007"

    # Where to run our API
    APP_HOST: str | None = "0.0.0.0"
    APP_PORT: int | None = 80

    # General logging information
    LOG_TO_FILE: bool | None = False
    LOG_LEVEL: str | int | None = logging.INFO # change to see more/less logs
    LOG_RETENTION: str | int | None = "10 minutes"
    LOG_ROTATION: str | None = "1 minute"
    LOG_DIAGNOSE: bool | None = False  # DO NOT SET TO TRUE IN PROD

    # Where to run ReDoc/Swagger (currently using FastAPI's Default)
    REDOC_URL: str | None = "/redoc"
    SWAGGER_URL: str | None = "/docs"

@lru_cache
def get_settings() -> Settings:
    """Get applications settings (cached)."""
    return Settings()
