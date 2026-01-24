"""
Database session dependency for the Todo API.
This module provides the database session dependency that is used by the API routes.
"""

from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from settings import settings


# Create sync engine and session maker
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to True for SQL query logging
    pool_pre_ping=True  # Verify connections before use
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)


def get_session_dep():
    """
    Dependency to get sync database session.
    """
    with SessionLocal() as session:
        yield session