"""
Base Classes and Decorators for MCP Tools

This module provides base functionality and decorators for creating
MCP tools that interact with the todo system.
"""
from typing import Callable, Any, Dict
from functools import wraps
import logging
from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.database import get_async_session
from sqlmodel import select
import inspect
from .errors import NotFoundError


# Set up logging
logger = logging.getLogger(__name__)


class ToolResponse(BaseModel):
    """Base response model for all MCP tools."""
    success: bool
    message: str
    data: Dict[str, Any] = {}


def mcp_tool(name: str, description: str):
    """
    Decorator to register an MCP tool with the server.

    NOTE: The actual MCP registration is deferred until the server module imports this,
    to avoid circular import issues with the MCP library.

    Args:
        name: Name of the tool
        description: Description of what the tool does
    """
    def decorator(func: Callable) -> Callable:
        # Store tool metadata for later registration by the server
        if not hasattr(func, '_mcp_metadata'):
            func._mcp_metadata = {'name': name, 'description': description}

        # Define the async wrapper without immediate registration
        @wraps(func)  # Use functools.wraps instead of manual copy
        async def wrapper(**kwargs):
            logger.info(f"Executing tool '{name}' with params: {kwargs}")

            # Extract function signature to validate inputs
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(**kwargs)
            bound_args.apply_defaults()

            async with get_async_session() as session:
                try:
                    # Execute the tool function with an async database session
                    result = await func(session=session, **bound_args.arguments)
                    await session.commit()  # Ensure transaction is committed

                    logger.info(f"Tool '{name}' completed successfully")
                    return result
                except Exception as e:
                    logger.error(f"Tool '{name}' failed: {str(e)}")
                    await session.rollback()  # Rollback on error
                    return {
                        "success": False,
                        "message": f"Tool execution failed: {str(e)}",
                        "data": {}
                    }

        # Add metadata to the wrapper as well
        wrapper._mcp_metadata = {'name': name, 'description': description}
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper
    return decorator


async def validate_user_access(session: AsyncSession, user_id: str, task_id: int = None):
    """
    Validate that the user has access to the requested resources.

    Args:
        session: Async database session
        user_id: ID of the user making the request
        task_id: Optional task ID to validate ownership

    Returns:
        bool: True if access is valid, raises exception otherwise
    """
    # This function would contain the logic to validate user access
    # For now, we'll implement a basic check - in a real system,
    # this would verify the user exists and has access rights
    from ..models.user_model import User

    # Input validation to prevent injection attacks
    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("Invalid user_id: user_id cannot be empty")

    # Fetch user from database using string user_id
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError(f"Invalid user_id: {user_id}")

    # If a task_id is provided, verify ownership
    if task_id:
        from ..models.task_model import Task
        task_result = await session.execute(select(Task).where(Task.id == task_id))
        task = task_result.scalar_one_or_none()

        # Check if task exists and if user owns the task
        if not task:
            raise NotFoundError("Task", task_id)

        if task.user_id != user_id:
            raise PermissionError(f"User {user_id} does not have access to task {task_id}")

    return True