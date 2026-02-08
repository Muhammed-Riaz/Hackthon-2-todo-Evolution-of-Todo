"""
Basic import tests for MCP tools

This test verifies that all MCP tools can be imported correctly.
"""
import pytest
from backend.src.mcp_tools import add_task, list_tasks, complete_task, update_task, delete_task


def test_tool_imports():
    """Test that all tools can be imported successfully."""
    assert add_task is not None
    assert list_tasks is not None
    assert complete_task is not None
    assert update_task is not None
    assert delete_task is not None
    print("All MCP tools imported successfully!")