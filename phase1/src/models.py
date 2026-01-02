"""Data models for the Todo In-Memory Python Console App."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a task in the todo list.

    Attributes:
        id: Unique identifier for the task (auto-incremented)
        title: Required title of the task
        description: Optional description of the task
        completed: Status of the task (default: False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False