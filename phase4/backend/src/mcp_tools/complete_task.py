"""
Complete Task MCP Tool

This module implements the complete_task MCP tool that allows AI agents
to mark a task as completed in the system.
"""
from typing import Dict, Any
from pydantic import BaseModel, Field
from sqlmodel import Session
from .base import mcp_tool, validate_user_access
from .errors import ValidationError, DatabaseError, NotFoundError, create_success_response
from ..models.task_model import Task


class CompleteTaskInput(BaseModel):
    """Input model for the complete_task tool."""
    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: int = Field(..., ge=1, description="The ID of the task to complete")


@mcp_tool(
    name="complete_task",
    description="Mark a task as completed"
)
async def complete_task(input_data: CompleteTaskInput, session: AsyncSession) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        input_data: Input containing user_id and task_id
        session: Async database session

    Returns:
        Dict containing task_id, status, and title of the completed task
    """
    # Validate input data
    if not input_data.user_id:
        raise ValidationError("User ID is required",
                            field_errors={"user_id": "User ID cannot be empty"})

    if input_data.task_id <= 0:
        raise ValidationError("Task ID must be a positive integer",
                            field_errors={"task_id": "Task ID must be greater than 0"})

    # Validate user access to the specific task
    await validate_user_access(session, input_data.user_id, input_data.task_id)

    try:
        # Get the task from the database
        result = await session.execute(select(Task).where(Task.id == input_data.task_id))
        task = result.scalar_one_or_none()

        if not task:
            raise NotFoundError("Task", input_data.task_id)

        # Check if task is already completed (idempotent behavior)
        if task.completed:
            # Still return success for idempotent behavior
            return create_success_response(
                message=f"Task {input_data.task_id} was already completed",
                data={
                    "task_id": task.id,
                    "status": "completed",
                    "title": task.title
                }
            )

        # Mark the task as completed
        task.completed = True

        # Commit the changes
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Return success response with task details
        return create_success_response(
            message=f"Task {input_data.task_id} marked as completed",
            data={
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
        )
    except ValueError as e:
        # Handle conversion errors or other value errors
        raise ValidationError(f"Invalid input: {str(e)}", field_errors={"input_data": str(e)})
    except Exception as e:
        # Handle any other database errors
        await session.rollback()
        raise DatabaseError(f"Failed to complete task: {str(e)}", original_error=e)