"""
Delete Task MCP Tool

This module implements the delete_task MCP tool that allows AI agents
to remove a task from the system.
"""
from typing import Dict, Any
from pydantic import BaseModel, Field
from sqlmodel import Session
from .base import mcp_tool, validate_user_access
from .errors import ValidationError, DatabaseError, NotFoundError, create_success_response
from ..models.task_model import Task


class DeleteTaskInput(BaseModel):
    """Input model for the delete_task tool."""
    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: int = Field(..., ge=1, description="The ID of the task to delete")


@mcp_tool(
    name="delete_task",
    description="Remove a task"
)
async def delete_task(input_data: DeleteTaskInput, session: AsyncSession) -> Dict[str, Any]:
    """
    Remove a task from the database.

    Args:
        input_data: Input containing user_id and task_id
        session: Async database session

    Returns:
        Dict containing task_id, status, and title of the deleted task
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

        # Store the task details before deletion for the response
        task_details = {
            "task_id": task.id,
            "title": task.title
        }

        # Delete the task from the database
        await session.delete(task)
        await session.commit()

        # Return success response with deleted task details
        return create_success_response(
            message=f"Task {input_data.task_id} deleted successfully",
            data={
                "task_id": task_details["task_id"],
                "status": "deleted",
                "title": task_details["title"]
            }
        )
    except ValueError as e:
        # Handle validation errors
        raise ValidationError(f"Invalid input: {str(e)}", field_errors={"input_data": str(e)})
    except Exception as e:
        # Handle any other database errors
        await session.rollback()
        raise DatabaseError(f"Failed to delete task: {str(e)}", original_error=e)