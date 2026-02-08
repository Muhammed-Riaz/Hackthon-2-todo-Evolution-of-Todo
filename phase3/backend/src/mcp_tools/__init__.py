"""
MCP Tools Package for the Todo Application

This package contains all the Model Context Protocol (MCP) tools
that allow AI agents to interact with the todo system.
"""
import logging

# Configure logging for MCP tool calls
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler for tool call logging
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

# Import all tools to register them with the server
from . import add_task
from . import list_tasks
from . import complete_task
from . import update_task
from . import delete_task
from . import base
from . import errors