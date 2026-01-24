"""
User model for the backend application.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    """
    Base model for user fields.
    """
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


from uuid import uuid4

class User(UserBase, table=True):
    """
    User model for the database.
    """
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Add the __tablename__ property to customize the table name
    __tablename__ = "users"


class UserRead(UserBase):
    """
    Model for reading user data (without sensitive information).
    """
    id: str
    created_at: datetime
    updated_at: datetime