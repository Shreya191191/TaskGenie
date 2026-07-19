"""Application management tools for Android automation."""

import sys

import uiautomator2 as u2
from typing import Optional, Dict, Any
import shutil


def register_app_tools(mcp):
    """Register all app management related tools with the MCP server."""

    @mcp.tool(
        name="get_installed_apps",
        description="Get a complete list of all installed applications on your Android device. Automatically connects to the first available device if no device_id is specified. Returns package names for all system and user-installed apps.",
    )
    def get_installed_apps(device_id: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve a comprehensive list of all installed applications on the device.

        This function enumerates all applications installed on the Android device,
        including both system pre-installed apps and user-installed applications.
        Automatically handles device connection and validation.

        Args:
            device_id: Optional device identifier. If not provided, connects to the first available device.

        Returns:
            Dictionary containing:
                - success: Boolean indicating if operation was successful
                - apps: List of package names (if successful)
                - count: Total number of installed apps (if successful)
                - error: Error message (if operation failed)
                - device_id: The device ID that was used

        Note:
            - This may take several seconds on devices with many installed applications
            - Returns package names only, not detailed app information
            - Includes both system apps and user-installed apps
            - Automatically validates device connection before proceeding
        """
        try:
            # Direct ADB check first
            adb_path = shutil.which("adb")
            if not adb_path:
                return {
                    "success": False,
                    "apps": [],
                    "count": 0,
                    "error": "ADB is not available in PATH",
                    "device_id": device_id,
                }

            # Connect directly to device
            d = u2.connect(device_id)

            # Get installed apps
            apps = d.app_list()

            return {
                "success": True,
                "apps": apps,
                "count": len(apps),
                "error": None,
                "device_id": d.serial or device_id,
            }
        except Exception as e:
            return {
                "success": False,
                "apps": [],
                "count": 0,
                "error": f"Failed to get installed apps: {str(e)}",
                "device_id": device_id,
            }

    @mcp.tool(
        name="get_current_app",
        description="Get detailed information about the currently active/foreground application including package name, activity, and version information",
    )
    def get_current_app(device_id: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve information about the application currently in the foreground.

        This function provides details about the app that the user is currently
        interacting with or which is running in the foreground.

        Args:
            device_id: Optional device identifier. If not provided, uses the first available device.

        Returns:
            Dictionary containing app information:
                - package: Package name of the foreground app
                - activity: Current activity name
                - pid: Process ID
                - Other app metadata as provided by uiautomator2
        """
        d = u2.connect(device_id)
        return d.app_current()
