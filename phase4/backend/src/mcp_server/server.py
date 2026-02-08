"""
MCP Server for Todo Operations

This module initializes the Model Context Protocol (MCP) server that exposes
todo operations as tools for AI agents.
"""
import asyncio
from mcp.server import Server
from mcp.server.models import InitializationOptions
import uvicorn
from typing import Dict, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create the MCP server instance
server = Server("todo-mcp-server")


def register_mcp_tools():
    """
    Register all MCP tools for todo operations.

    This function registers the tools that AI agents can use to interact
    with the todo system: add_task, list_tasks, complete_task, update_task, delete_task.
    """
    # Import the MCP server only when we're ready to register tools
    try:
        from mcp.server import server as mcp_server

        # Import all tool modules to get their decorated functions
        import sys
        import os
        # Add the project root to the Python path to enable proper imports
        project_root = os.path.join(os.path.dirname(__file__), '..', '..')
        abs_project_root = os.path.abspath(project_root)
        if abs_project_root not in sys.path:
            sys.path.insert(0, abs_project_root)

        # Import the tools - this will load the functions with their metadata
        import backend.src.mcp_tools.add_task
        import backend.src.mcp_tools.list_tasks
        import backend.src.mcp_tools.complete_task
        import backend.src.mcp_tools.update_task
        import backend.src.mcp_tools.delete_task

        # Register each tool using the stored metadata
        tools_to_register = [
            backend.src.mcp_tools.add_task.add_task,
            backend.src.mcp_tools.list_tasks.list_tasks,
            backend.src.mcp_tools.complete_task.complete_task,
            backend.src.mcp_tools.update_task.update_task,
            backend.src.mcp_tools.delete_task.delete_task,
        ]

        for tool_func in tools_to_register:
            if hasattr(tool_func, '_mcp_metadata'):
                metadata = tool_func._mcp_metadata
                # Register the async wrapper version of the function
                @mcp_server.tool(
                    name=metadata['name'],
                    description=metadata['description'],
                )
                async def tool_wrapper(**kwargs):
                    # We need to create a wrapper that calls the stored async function
                    # For now, let's use the approach from the base module
                    import logging
                    from backend.src.database.session import get_session
                    from sqlmodel import Session
                    import inspect

                    logger = logging.getLogger(__name__)

                    # Extract function signature to validate inputs
                    sig = inspect.signature(tool_func)
                    bound_args = sig.bind_partial(**kwargs)
                    bound_args.apply_defaults()

                    try:
                        # Execute the tool function with a database session
                        with next(get_session()) as session:
                            result = tool_func(session=session, **bound_args.arguments)

                        logger.info(f"Tool '{metadata['name']}' completed successfully")
                        return result
                    except Exception as e:
                        logger.error(f"Tool '{metadata['name']}' failed: {str(e)}")
                        return {
                            "success": False,
                            "message": f"Tool execution failed: {str(e)}",
                            "data": {}
                        }

        print(f"Registered {len(tools_to_register)} MCP tools successfully")

    except ImportError:
        print("Warning: MCP server library not available. Tools loaded but not registered.")
        print("Install the 'mcp' package to enable server functionality.")


async def initialize_server():
    """
    Initialize the MCP server with all required tools.
    """
    logger.info("Initializing MCP server for todo operations")

    # Register all todo operation tools
    register_mcp_tools()

    logger.info("MCP server initialized successfully")


def run_server(host: str = "localhost", port: int = 8001):
    """
    Run the MCP server.

    Args:
        host: Host to bind the server to
        port: Port to run the server on
    """
    async def lifespan():
        async with server.install() as (send_request, results):
            await initialize_server()
            yield

    # Configure the server
    config = uvicorn.Config(
        app=server.app,
        host=host,
        port=port,
        lifespan="on"
    )
    server_instance = uvicorn.Server(config)

    logger.info(f"Starting MCP server at {host}:{port}")
    server_instance.run()


if __name__ == "__main__":
    run_server()