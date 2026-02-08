from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from models.user_task_models import Task, User
from utils.auth import get_current_user
from database import get_session_dep

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[dict])
async def get_user_tasks(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    """Get all tasks for a specific user"""
    # Verify that the user is authorized to access these tasks
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    # Query tasks for the specified user
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    # Convert to dict to include user information
    tasks_dict = []
    for task in tasks:
        task_dict = task.dict()
        task_dict["user_email"] = current_user.email
        tasks_dict.append(task_dict)

    return tasks_dict


@router.post("/{user_id}/tasks", response_model=dict)
async def create_task(
    user_id: int,
    title: str,
    description: str = "",
    completed: bool = False,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    """Create a new task for a user"""
    # Verify that the user is authorized to create tasks for this user_id
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create new task
    task = Task(
        title=title,
        description=description,
        user_id=user_id,
        completed=completed
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    # Add user email to response
    task_dict = task.dict()
    task_dict["user_email"] = current_user.email
    return task_dict


@router.get("/{user_id}/tasks/{task_id}", response_model=dict)
async def get_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    """Get a specific task by ID"""
    # Verify that the user is authorized to access this task
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    # Get the task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Add user email to response
    task_dict = task.dict()
    task_dict["user_email"] = current_user.email
    return task_dict


@router.put("/{user_id}/tasks/{task_id}", response_model=dict)
async def update_task(
    user_id: int,
    task_id: int,
    title: str = None,
    description: str = None,
    completed: bool = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    """Update a specific task by ID"""
    # Verify that the user is authorized to update this task
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Get the task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields if provided
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    # Update the timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Add user email to response
    task_dict = task.dict()
    task_dict["user_email"] = current_user.email
    return task_dict


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    """Delete a specific task by ID"""
    # Verify that the user is authorized to delete this task
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    # Get the task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=dict)
async def complete_task(
    user_id: int,
    task_id: int,
    completed: bool = True,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    """Toggle the completion status of a task"""
    # Verify that the user is authorized to update this task
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Get the task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update completion status
    task.completed = completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Add user email to response
    task_dict = task.dict()
    task_dict["user_email"] = current_user.email
    return task_dict