"""
Task API routes for the backend application.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ....database.database import get_async_session
from ....models.task_model import Task
from ....schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse, TaskCreateRequest
from ....services.task_service import create_task, get_tasks_by_user_id, get_task_by_id_and_user_id, update_task, delete_task, toggle_task_completion
from ....auth.dependencies import get_current_user_id

router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])


@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task_endpoint(
    user_id: str,
    task_create_request: TaskCreateRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for a user.
    """
    # Ensure the user_id in the request matches the user_id in the token
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match user ID in URL"
        )

    # Create the task using the service with the authenticated user's ID
    task_create = TaskCreate(
        title=task_create_request.title,
        description=task_create_request.description,
        completed=task_create_request.completed,
        user_id=current_user_id
    )

    # Create the task using the service
    created_task = await create_task(session, task_create)

    return created_task


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks_endpoint(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for a specific user.
    """
    # Ensure the user_id in the request matches the user_id in the token
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match user ID in URL"
        )

    # Get tasks for the authenticated user
    tasks = await get_tasks_by_user_id(session, current_user_id)

    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID for a user.
    """
    # Ensure the user_id in the request matches the user_id in the token
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match user ID in URL"
        )

    # Get the specific task
    task = await get_task_by_id_and_user_id(session, task_id, current_user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task by ID for a user.
    """
    # Ensure the user_id in the request matches the user_id in the token
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match user ID in URL"
        )

    updated_task = await update_task(session, task_id, current_user_id, task_update)

    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


@router.delete("/tasks/{task_id}", status_code=200)
async def delete_task_endpoint(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID for a user.
    """
    # Ensure the user_id in the request matches the user_id in the token
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match user ID in URL"
        )

    success = await delete_task(session, task_id, current_user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"success": True}


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task_endpoint(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task by ID for a user.
    """
    # Ensure the user_id in the request matches the user_id in the token
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match user ID in URL"
        )

    task = await toggle_task_completion(session, task_id, current_user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task