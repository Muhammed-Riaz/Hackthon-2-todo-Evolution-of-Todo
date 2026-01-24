"""
Authentication-related Pydantic schemas for the backend application.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    """
    Schema for returning user information.
    """
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TokenResponse(BaseModel):
    """
    Schema for returning authentication tokens.
    """
    access_token: str
    token_type: str
    user: UserResponse