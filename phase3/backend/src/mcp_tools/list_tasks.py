"""
List Tasks MCP Tool

This module implements the list_tasks MCP tool that allows AI agents
to retrieve a user's todo tasks from the system.
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from .base import mcp_tool, validate_user_access
from .errors import ValidationError, DatabaseError, create_success_response
from ..models.task_model import Task


class ListTasksInput(BaseModel):
    """Input model for the list_tasks tool."""
    user_id: str = Field(..., description="The ID of the user whose tasks to retrieve")
    status: str = Field("all", description="Filter tasks by completion status",
                       regex="^(all|pending|completed)$")


class TaskItem(BaseModel):
    """Model for a single task item in the response."""
    id: int
    title: str
    completed: bool


@mcp_tool(
    name="list_tasks",
    description="Retrieve todos for a user"
)
async def list_tasks(input_data: ListTasksInput, session: AsyncSession) -> Dict[str, Any]:
    """
    Retrieve tasks for a specific user based on status filter.

    Args:
        input_data: Input containing user_id and optional status filter
        session: Async database session

    Returns:
        Dict containing an array of task objects with id, title, and completed status
    """
    # Validate input data
    if not input_data.user_id:
        raise ValidationError("User ID is required",
                            field_errors={"user_id": "User ID cannot be empty"})

    # Validate user access
    await validate_user_access(session, input_data.user_id)

    try:
        # Build the query based on status filter
        query = select(Task).where(Task.user_id == input_data.user_id)

        # Apply status filter if specified
        if input_data.status == "pending":
            query = query.where(Task.completed == False)
        elif input_data.status == "completed":
            query = query.where(Task.completed == True)
        # If status is "all", no additional filter is needed

        # Execute the query
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Format the response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
            for task in tasks
        ]

        # Return success response with task list
        return create_success_response(
            message=f"Retrieved {len(task_list)} tasks for user {input_data.user_id}",
            data={
                "tasks": task_list
            }
        )
    except ValueError as e:
        # Handle conversion errors (e.g. user_id not a valid integer)
        raise ValidationError(f"Invalid input: {str(e)}", field_errors={"user_id": str(e)})
    except Exception as e:
        # Handle any other database errors
        raise DatabaseError(f"Failed to retrieve tasks: {str(e)}", original_error=e)