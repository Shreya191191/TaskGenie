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

    @mcp.tool(
        name="get_device_status",
        description="Get complete device status including connection, ADB availability, and basic device info. This is the recommended first step to ensure everything is working before performing other operations.",
    )
    def get_device_status() -> Dict[str, Any]:
        """Get comprehensive device status and connectivity information.

        This tool performs a complete check of the Android device setup including:
        - ADB availability and system status
        - Connected devices enumeration
        - Device connection and basic information
        - Screen state and readiness for automation

        Returns:
            Dictionary containing complete status information:
                - adb_available: Boolean indicating if ADB is accessible
                - connected_devices: List of available device IDs
                - device_connected: Boolean indicating if device connection succeeded
                - device_info: Basic device information (if connected)
                - screen_on: Boolean indicating if device screen is on
                - error: Any error messages (if applicable)
                - ready_for_automation: Boolean indicating if device is ready

        This is the perfect starting point for any Android automation workflow.
        It will guide you through any connection issues and provide clear next steps.
        """
        try:
            # Check ADB availability directly
            adb_path = shutil.which("adb")
            if not adb_path:
                return {
                    "adb_available": False,
                    "connected_devices": [],
                    "device_connected": False,
                    "device_info": {},
                    "screen_on": False,
                    "error": "ADB not available in PATH. Please install Android SDK platform-tools.",
                    "ready_for_automation": False,
                }

            # Check for connected devices
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
            except Exception as e:
                return {
                    "adb_available": True,
                    "connected_devices": [],
                    "device_connected": False,
                    "device_info": {},
                    "screen_on": False,
                    "error": f"Failed to check connected devices: {str(e)}",
                    "ready_for_automation": False,
                }

            status = {
                "adb_available": True,
                "connected_devices": devices,
                "device_connected": False,
                "device_info": {},
                "screen_on": False,
                "error": None,
                "ready_for_automation": False,
            }

            if not devices:
                status["error"] = (
                    "No devices connected. Please connect device and enable USB debugging."
                )
                return status

            # Try to connect and get basic info
            try:
                d = u2.connect()
                info = d.info
                device_info = {
                    "manufacturer": info.get("manufacturer", ""),
                    "model": info.get("model", ""),
                    "serial": info.get("serial", ""),
                    "version": info.get("version", {}).get("release", ""),
                    "sdk": info.get("version", {}).get("sdk", 0),
                }

                status["device_connected"] = True
                status["device_info"] = device_info

                # Check screen state
                status["screen_on"] = d.screen_on()
                status["ready_for_automation"] = True

            except Exception as e:
                status["error"] = f"Device connection failed: {str(e)}"

            return status
        except Exception as e:
            return {
                "adb_available": False,
                "connected_devices": [],
                "device_connected": False,
                "device_info": {},
                "screen_on": False,
                "error": f"Status check failed: {str(e)}",
                "ready_for_automation": False,
            }
