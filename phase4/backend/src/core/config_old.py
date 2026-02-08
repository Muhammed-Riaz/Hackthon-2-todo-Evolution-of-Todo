"""
Configuration management for the backend application.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    database_url: str = "postgresql+psycopg2://user:password@localhost/dbname"
    environment: str = "development"
    log_level: str = "info"
    secret_key: str = "your-super-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days
    db_echo_sql: bool = True
    db_pool_recycle: int = 300

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    """
    Get application settings instance.
    """
    return Settings()