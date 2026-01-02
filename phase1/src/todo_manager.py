"""Todo Manager for the Todo In-Memory Python Console App.

This module contains the TodoManager class which handles all CRUD operations for tasks.
"""

from typing import List, Optional
from .models import Task


class TodoManager:
    """Manages a collection of tasks in memory.

    Provides methods for creating, reading, updating, and deleting tasks.
    All operations are performed in-memory only.
    """

    def __init__(self):
        """Initialize the TodoManager with an empty task list and ID counter."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create a new task with an auto-incremented ID.

        Args:
            title: The title of the task (cannot be empty or whitespace-only)
            description: The description of the task (optional)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        if not title or title.isspace():
            raise ValueError("Task title cannot be empty or contain only whitespace")

        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in the manager.

        Returns:
            List of all Task objects
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Return the task with the specified ID or None if not found.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update the specified task with new values.

        Args:
            task_id: The ID of the task to update
            title: New title (only updates if provided and not None)
            description: New description (only updates if provided and not None)

        Returns:
            Updated Task object if successful, None if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        # Update title if provided and not None
        if title is not None:
            if not title or title.isspace():
                raise ValueError("Task title cannot be empty or contain only whitespace")
            task.title = title

        # Update description if provided and not None
        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete the task with the specified ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if deletion was successful, False if task not found
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle the completed status of the specified task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            Updated Task object if successful, None if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        task.completed = not task.completed
        return task