"""
Base SQLModel with common fields for all models.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import sqlalchemy as sa


class BaseSQLModel(SQLModel):
    """
    Base class for all SQLModel models with common fields.
    """
    pass


# Define the timestamp mixin as a class that can be inherited
class TimestampMixin():
    """
    Mixin class to add created_at and updated_at timestamp fields.
    """
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)