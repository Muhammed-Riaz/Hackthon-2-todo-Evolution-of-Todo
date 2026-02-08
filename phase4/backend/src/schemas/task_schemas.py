"""
Pydantic schemas for Task entity in the backend application.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    """
    Base schema for Task with common fields.
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False
    user_id: str = Field(..., min_length=1)


class TaskCreateRequest(BaseModel):
    """
    Schema for creating a new Task (request only, without user_id).
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False  # Default to False when creating


class TaskCreate(TaskBase):
    """
    Schema for creating a new Task.
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False  # Default to False when creating
    user_id: str = Field(..., min_length=1)


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing Task.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """
    Schema for Task response with additional fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True