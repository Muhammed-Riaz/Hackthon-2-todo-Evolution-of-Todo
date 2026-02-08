"""
Error Handling and Structured Response System for MCP Tools

This module provides standardized error responses and exception handling
for all MCP tools in the todo system.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging


# Set up logging
logger = logging.getLogger(__name__)


class ToolError(Exception):
    """Base exception for MCP tool errors."""

    def __init__(self, message: str, error_code: str = "TOOL_ERROR", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary for structured response."""
        return {
            "success": False,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details
        }


class ValidationError(ToolError):
    """Exception raised for validation errors."""

    def __init__(self, message: str, field_errors: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={"field_errors": field_errors or {}}
        )


class AuthorizationError(ToolError):
    """Exception raised for authorization errors."""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR"
        )


class NotFoundError(ToolError):
    """Exception raised when a resource is not found."""

    def __init__(self, resource_type: str, resource_id: Any):
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(
            message=message,
            error_code="NOT_FOUND_ERROR",
            details={
                "resource_type": resource_type,
                "resource_id": resource_id
            }
        )


class DatabaseError(ToolError):
    """Exception raised for database errors."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details={
                "original_error": str(original_error) if original_error else None
            }
        )


def create_success_response(message: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a standardized success response."""
    return {
        "success": True,
        "message": message,
        "data": data
    }


def create_error_response(error: ToolError) -> Dict[str, Any]:
    """Create a standardized error response from a ToolError."""
    return error.to_dict()


def handle_tool_exception(exc: Exception) -> Dict[str, Any]:
    """Handle an exception and convert it to a structured response."""
    if isinstance(exc, ToolError):
        return create_error_response(exc)

    # Log the unexpected error
    logger.error(f"Unexpected error in MCP tool: {str(exc)}", exc_info=True)

    # Return a generic error response
    return ToolError(
        message="An unexpected error occurred while executing the tool",
        error_code="UNEXPECTED_ERROR",
        details={"original_error": str(exc)}
    ).to_dict()