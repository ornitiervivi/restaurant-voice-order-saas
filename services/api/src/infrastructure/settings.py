"""Application settings for the FastAPI backend."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    app_name: str = "Restaurant Voice Order API"
    environment: str = "local"
    api_version: str = "0.1.0"
    database_url: str = "postgresql://restaurant_voice_order:restaurant_voice_order_dev_password@localhost:5432/restaurant_voice_order"

    model_config = SettingsConfigDict(env_prefix="API_", env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings for dependency injection."""

    return Settings()
