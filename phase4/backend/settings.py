from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_db")
    db_echo_sql: bool = os.getenv("DB_ECHO_SQL", "False").lower() == "true"
    db_pool_recycle: int = int(os.getenv("DB_POOL_RECYCLE", "300"))
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Auth settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-token-with-at-least-32-characters-long")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key-if-not-set")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Frontend URL for CORS (in production, set this properly)
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # MCP Server settings
    MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8001"))
    MCP_LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"


settings = Settings()