"""
Task service functions for the backend application.
"""

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models.task_model import Task, TaskBase
from ..schemas.task_schemas import TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, task_create: TaskCreate) -> Task:
    """
    Create a new task in the database.
    """
    # Create a new Task instance from the input
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=task_create.user_id
    )

    # Add the task to the session
    session.add(task)

    # Commit the transaction
    await session.commit()

    # Refresh the task to get the generated ID and timestamps
    await session.refresh(task)

    return task


async def get_tasks_by_user_id(session: AsyncSession, user_id: str) -> List[Task]:
    """
    Get all tasks for a specific user.
    """
    # Create a query to get all tasks for the specified user_id
    statement = select(Task).where(Task.user_id == user_id)

    # Execute the query
    result = await session.execute(statement)

    # Return the list of tasks
    return result.scalars().all()


async def get_task_by_id_and_user_id(session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a specific task by its ID and user ID.
    """
    # Create a query to get a task by its ID and user ID
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)

    # Execute the query
    result = await session.execute(statement)

    # Return the task or None if not found
    return result.scalar_one_or_none()


async def update_task(session: AsyncSession, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update an existing task.
    """
    # Get the existing task
    existing_task = await get_task_by_id_and_user_id(session, task_id, user_id)

    if not existing_task:
        return None

    # Update the task with provided fields
    update_data = task_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_task, field, value)

    # Commit the changes
    await session.commit()

    # Refresh the task to get updated data
    await session.refresh(existing_task)

    return existing_task


async def delete_task(session: AsyncSession, task_id: int, user_id: str) -> bool:
    """
    Delete a task by its ID and user ID.
    """
    # Get the existing task
    existing_task = await get_task_by_id_and_user_id(session, task_id, user_id)

    if not existing_task:
        return False

    # Delete the task
    await session.delete(existing_task)

    # Commit the changes
    await session.commit()

    return True


async def toggle_task_completion(session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a task.
    """
    # Get the existing task
    existing_task = await get_task_by_id_and_user_id(session, task_id, user_id)

    if not existing_task:
        return None

    # Toggle the completion status
    existing_task.completed = not existing_task.completed

    # Commit the changes
    await session.commit()

    # Refresh the task to get updated data
    await session.refresh(existing_task)

    return existing_task