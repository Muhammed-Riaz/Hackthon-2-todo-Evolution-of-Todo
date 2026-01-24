"""
Task model definition for the backend application.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import sqlalchemy as sa
from .base import TimestampMixin


class TaskBase(SQLModel):
    """
    Base class for Task with common fields.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(min_length=1)


class Task(TaskBase, TimestampMixin, table=True):
    """
    Task model with all required fields.
    """
    id: Optional[int] = Field(default=None, primary_key=True)