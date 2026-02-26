from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = "test"
    REDIS_URL: str
    # Sentry DSN / project key. Can be left empty for local development.
    SENTRY_DSN: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
