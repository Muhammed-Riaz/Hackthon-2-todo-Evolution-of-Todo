"""
Models module initialization for SQLModel metadata registration.
"""
from .user_model import User
from .task_model import Task
from .conversation_model import Conversation, Message

# Export all models so they are registered with SQLModel metadata
__all__ = ["User", "Task", "Conversation", "Message"]