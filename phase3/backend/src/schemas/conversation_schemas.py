"""
Schemas for conversation and message models.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ConversationCreate(BaseModel):
    """
    Schema for creating a new conversation.
    """
    user_id: str


class ConversationResponse(BaseModel):
    """
    Schema for conversation response.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    """
    Schema for creating a new message.
    """
    conversation_id: int
    user_id: str
    role: str
    content: str


class MessageResponse(BaseModel):
    """
    Schema for message response.
    """
    id: int
    conversation_id: int
    user_id: str
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """
    Schema for chat request from frontend.
    """
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """
    Schema for chat response to frontend.
    """
    response: str
    conversation_id: int
    tool_calls: List[dict]
    timestamp: datetime