from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False)
    first_name: Optional[str] = Field(max_length=100)
    last_name: Optional[str] = Field(max_length=100)
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    created_at: datetime.datetime = Field(default=datetime.datetime.utcnow())
    updated_at: datetime.datetime = Field(default=datetime.datetime.utcnow(), sa_column_kwargs=dict(onupdate=datetime.datetime.utcnow))

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime.datetime = Field(default=datetime.datetime.utcnow())
    updated_at: datetime.datetime = Field(default=datetime.datetime.utcnow(), sa_column_kwargs=dict(onupdate=datetime.datetime.utcnow))

    # Relationship to user
    user: User = Relationship(back_populates="tasks")