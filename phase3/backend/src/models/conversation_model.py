"""
Conversation and Message models for the chat functionality.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import sqlalchemy as sa
from .base import TimestampMixin


class ConversationBase(SQLModel):
    """
    Base class for Conversation with common fields.
    """
    user_id: str = Field(sa_column=sa.Column(sa.String, nullable=False))


class Conversation(ConversationBase, TimestampMixin, table=True):
    """
    Conversation model representing a chat session.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    # Add relationship if needed in the future
    # messages: List["Message"] = Relationship(back_populates="conversation")


class MessageBase(SQLModel):
    """
    Base class for Message with common fields.
    """
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    user_id: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    role: str = Field(sa_column=sa.Column(sa.String(20), nullable=False))  # 'user' or 'assistant'
    content: str = Field(sa_column=sa.Column(sa.Text, nullable=False))


class Message(MessageBase, TimestampMixin, table=True):
    """
    Message model representing individual chat messages.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    # Add relationship if needed in the future
    # conversation: Conversation = Relationship(back_populates="messages")