"""
Update Task MCP Tool

This module implements the update_task MCP tool that allows AI agents
to update a task's title and/or description in the system.
"""
from typing import Dict, Any
from pydantic import BaseModel, Field
from sqlmodel import Session
from .base import mcp_tool, validate_user_access
from .errors import ValidationError, DatabaseError, NotFoundError, create_success_response
from ..models.task_model import Task


class UpdateTaskInput(BaseModel):
    """Input model for the update_task tool."""
    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: int = Field(..., ge=1, description="The ID of the task to update")
    title: str = Field(None, min_length=1, max_length=255, description="New title for the task (optional)")
    description: str = Field(None, description="New description for the task (optional)")


@mcp_tool(
    name="update_task",
    description="Update task title and/or description"
)
async def update_task(input_data: UpdateTaskInput, session: AsyncSession) -> Dict[str, Any]:
    """
    Update a task's title and/or description.

    Args:
        input_data: Input containing user_id, task_id, and optional fields to update
        session: Async database session

    Returns:
        Dict containing task_id, status, and updated title
    """
    # Validate input data
    if not input_data.user_id:
        raise ValidationError("User ID is required",
                            field_errors={"user_id": "User ID cannot be empty"})

    if input_data.task_id <= 0:
        raise ValidationError("Task ID must be a positive integer",
                            field_errors={"task_id": "Task ID must be greater than 0"})

    # Check if at least one field is provided to update
    if input_data.title is None and input_data.description is None:
        raise ValidationError("At least one field (title or description) must be provided to update",
                            field_errors={"update_fields": "Either title or description must be provided"})

    # Validate user access to the specific task
    await validate_user_access(session, input_data.user_id, input_data.task_id)

    try:
        # Get the task from the database
        result = await session.execute(select(Task).where(Task.id == input_data.task_id))
        task = result.scalar_one_or_none()

        if not task:
            raise NotFoundError("Task", input_data.task_id)

        # Update the fields that were provided
        if input_data.title is not None:
            task.title = input_data.title
        if input_data.description is not None:
            task.description = input_data.description

        # Commit the changes
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Return success response with updated task details
        return create_success_response(
            message=f"Task {input_data.task_id} updated successfully",
            data={
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
        )
    except ValueError as e:
        # Handle validation errors
        raise ValidationError(f"Invalid input: {str(e)}", field_errors={"input_data": str(e)})
    except Exception as e:
        # Handle any other database errors
        await session.rollback()
        raise DatabaseError(f"Failed to update task: {str(e)}", original_error=e)