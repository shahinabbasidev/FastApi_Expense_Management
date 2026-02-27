from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = 'sqlite:///:memory:'
    JWT_SECRET_KEY: str = "test"
    REDIS_URL: str = "redis://redis:6379"
    # Sentry DSN / project key. Can be left empty for local development.
    SENTRY_DSN: str = "https://5052d08d8859c013ec9c3942d74b2158@sentry.hamravesh.com/9811"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
