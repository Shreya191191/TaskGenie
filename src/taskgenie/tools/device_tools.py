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

    @mcp.tool(
        name="check_adb_and_list_devices",
        description="Check if ADB (Android Debug Bridge) is available in the system PATH and list all connected Android devices with their status",
    )
    def check_adb_and_list_devices() -> Dict[str, Any]:
        """Verify ADB availability and enumerate connected Android devices.

        This utility function checks if ADB is properly installed and accessible,
        then lists all Android devices currently connected via USB or network.

        Returns:
            Dictionary containing:
                - adb_exists: Boolean indicating if ADB command is found in PATH
                - devices: List of device serial numbers that are ready for automation
                - error: Error message if ADB check fails, None otherwise

        The devices list only includes devices with "device" status (ready for commands).
        Devices in "unauthorized" or other states are excluded.
        """
        adb_path = shutil.which("adb")
        if not adb_path:
            return {
                "adb_exists": False,
                "devices": [],
                "error": "adb command not found in PATH",
            }
        try:
            result = subprocess.run(
                [adb_path, "devices"], capture_output=True, text=True, check=True
            )
            lines = result.stdout.strip().splitlines()
            devices = []
            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2 and parts[1] == "device":
                        devices.append(parts[0])
            return {"adb_exists": True, "devices": devices, "error": None}
        except Exception as e:
            return {"adb_exists": True, "devices": [], "error": str(e)}
