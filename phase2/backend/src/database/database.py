"""
Database engine and session management for the backend application.
"""

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from ..core.config import get_settings

# Get database URL from settings
settings = get_settings()
DATABASE_URL = settings.database_url

# Force SQLite for development if it's the default PostgreSQL URL
if DATABASE_URL == "postgresql+psycopg2://user:password@localhost/dbname":
    DATABASE_URL = "sqlite+aiosqlite:///./todo_app.db"  # Use aiosqlite for async support
elif DATABASE_URL.startswith("postgresql"):
    # Replace postgresql with postgresql+asyncpg for async support
    DATABASE_URL = DATABASE_URL.replace("postgresql+", "postgresql+asyncpg")
elif DATABASE_URL.startswith("sqlite") and not DATABASE_URL.startswith("sqlite+aiosqlite"):
    # For SQLite, we need to use aiosqlite for async support
    DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to True for SQL query logging
    pool_pre_ping=True  # Verify connections before use
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get async database session.
    """
    async with AsyncSessionLocal() as session:
        yield session