"""
Add Task MCP Tool

This module implements the add_task MCP tool that allows AI agents
to create new todo tasks in the system.
"""
from typing import Dict, Any
from pydantic import BaseModel, Field
from sqlmodel import Session
from .base import mcp_tool, validate_user_access
from .errors import ValidationError, DatabaseError, create_success_response
from ..models.task_model import Task


class AddTaskInput(BaseModel):
    """Input model for the add_task tool."""
    user_id: str = Field(..., description="The ID of the user creating the task")
    title: str = Field(..., min_length=1, max_length=255, description="The title of the task")
    description: str = Field(None, description="Optional description of the task")


@mcp_tool(
    name="add_task",
    description="Create a new todo item"
)
async def add_task(input_data: AddTaskInput, session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new task in the database.

    Args:
        input_data: Input containing user_id, title, and optional description
        session: Async database session

    Returns:
        Dict containing task_id, status, and title of the created task
    """
    # Validate input data
    if not input_data.title.strip():
        raise ValidationError("Title is required and cannot be empty",
                            field_errors={"title": "Title cannot be empty"})

    # Validate user access
    await validate_user_access(session, input_data.user_id)

    try:
        # Create a new task instance
        new_task = Task(
            title=input_data.title,
            description=input_data.description,
            completed=False,  # Default to not completed
            user_id=input_data.user_id  # Use string as expected by the model
        )

        # Add the task to the session and commit
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)  # Refresh to get the generated ID

        # Return success response with required fields
        return create_success_response(
            message="Task created successfully",
            data={
                "task_id": new_task.id,
                "status": "created",
                "title": new_task.title
            }
        )
    except ValueError as e:
        # Handle conversion errors (e.g. user_id not a valid integer)
        raise ValidationError(f"Invalid input: {str(e)}", field_errors={"user_id": str(e)})
    except Exception as e:
        # Handle any other database errors
        await session.rollback()
        raise DatabaseError(f"Failed to create task: {str(e)}", original_error=e)