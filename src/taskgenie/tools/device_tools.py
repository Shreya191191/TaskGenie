"""Device management tools for Android automation."""

import uiautomator2 as u2
from typing import Optional, Dict, Any
import shutil
import subprocess


def register_device_tools(mcp):
    """Register all device management related tools with the MCP server."""

    @mcp.tool(
        name="mcp_health",
        description="Simple health check tool to verify MCP server is running",
    )
    def mcp_health() -> str:
        """Check if the MCP server is running and responsive.

        Returns:
            A greeting message confirming the server is operational
        """
        return "Hello, world! MCP Android Device Operator server is running."
