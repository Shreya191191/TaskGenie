"""
TaskGenie MCP Server Test Suite.

Unit, integration, and import verification tests for the TaskGenie server.
Corresponds to tests/test_server.py in the reference repository.
"""

import pytest
from unittest.mock import MagicMock


def test_server_can_be_imported():
    """Test that the main server can be imported."""
    try:
        from taskgenie import server

        assert hasattr(server, "mcp")
        assert server.mcp.name == "TaskGenie"
    except ImportError as e:
        pytest.fail(f"Failed to import server: {e}")


def test_server_has_mcp_instance():
    """Test that the server has a valid MCP instance."""
    from taskgenie import server

    # Verify the MCP instance exists
    assert server.mcp is not None
    assert server.mcp.name == "TaskGenie"


def test_server_instructions_exist():
    """Test that server has proper instructions for the AI."""
    from taskgenie import server

    assert server.mcp.instructions is not None
    assert len(server.mcp.instructions) > 0
    assert "Android" in server.mcp.instructions
    assert "automation" in server.mcp.instructions


def test_mcp_server_creation():
    """Test that MCP server can be created successfully."""
    from fastmcp import FastMCP

    # Create a test MCP server similar to our main server
    test_mcp = FastMCP(name="Test Server")

    # Should be able to register a simple test tool
    @test_mcp.tool(name="test_tool", description="Test tool")
    def test_tool():
        return "test"

    assert test_mcp is not None
    assert test_mcp.name == "Test Server"
