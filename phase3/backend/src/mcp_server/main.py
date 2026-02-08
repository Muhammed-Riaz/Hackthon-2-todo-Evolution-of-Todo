"""
Main entry point for the MCP Server

This module ties together all the components of the MCP server
and provides the main execution entry point.
"""
from .server import server, initialize_server, run_server
from ..mcp_tools.add_task import add_task  # Import to register the tool
from ..mcp_tools.list_tasks import list_tasks  # Import to register the tool
from ..mcp_tools.complete_task import complete_task  # Import to register the tool
from ..mcp_tools.update_task import update_task  # Import to register the tool
from ..mcp_tools.delete_task import delete_task  # Import to register the tool
import asyncio
import logging
from backend.settings import settings


# Configure logging based on settings
logging.basicConfig(level=getattr(logging, settings.MCP_LOG_LEVEL.upper()))


async def startup():
    """Initialize the MCP server with all tools."""
    await initialize_server()


def main():
    """Main entry point for the MCP server."""
    # Register all tools by importing them
    # Run the server
    run_server(host=settings.MCP_SERVER_HOST, port=settings.MCP_SERVER_PORT)


if __name__ == "__main__":
    main()