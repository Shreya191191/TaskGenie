"""Advanced automation tools (toast messages, activity waiting)."""

import shutil
import subprocess
import sys
import uiautomator2 as u2
from typing import Optional


def get_device(device_id: Optional[str] = None) -> u2.Device:
    """Connect to uiautomator2 device, auto-resolving first available device if device_id is None."""
    if not device_id:
        adb_path = shutil.which("adb")
        if adb_path:
            try:
                res = subprocess.run(
                    [adb_path, "devices"], capture_output=True, text=True
                )
                for line in res.stdout.strip().splitlines()[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2 and parts[1] == "device":
                            device_id = parts[0]
                            break
            except Exception:
                pass
    return u2.connect(device_id)


def register_advanced_tools(mcp):
    """Register all advanced tools with the MCP server."""

    @mcp.tool(
        name="get_toast",
        description="Retrieve the text of the last toast message displayed on the device. Useful for verifying notifications, error messages, and user feedback.",
    )
    def get_toast(device_id: Optional[str] = None) -> str:
        """Get the text content of the most recent toast message.

        This function captures toast messages (temporary popup notifications) that
        appear briefly on screen, which can be useful for verifying operations
        or capturing system messages.

        Args:
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            str: The text content of the last toast message, or empty string if none found

        Examples:
            >>> get_toast()  # Get the last toast message
            # Returns: "Download completed successfully"

        Note:
            Toast messages are temporary and may disappear quickly.
            Call this function promptly after the action that triggers the toast.
            The function waits up to 10 seconds for a toast message.
        """
        try:
            d = get_device(device_id)
            return d.toast.get_message(10.0) or ""
        except Exception as e:
            print(f"Failed to get toast message: {str(e)}", file=sys.stderr)
            return ""

    @mcp.tool(
        name="wait_activity",
        description="Wait for a specific Android activity to appear on the screen. Useful for navigation verification and app state validation.",
    )
    def wait_activity(
        activity: str, timeout: float = 10.0, device_id: Optional[str] = None
    ) -> bool:
        """Wait for a specific Android activity to become the current foreground activity.

        This function monitors the device and waits until the specified activity
        appears in the foreground, which is useful for verifying navigation
        and app state transitions.

        Args:
            activity: The full activity name to wait for (e.g., "com.example.app.MainActivity")
            timeout: Maximum time in seconds to wait (default: 10.0)
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            bool: True if the activity appeared within the timeout, False otherwise

        Examples:
            >>> wait_activity("com.android.settings.Settings")  # Wait for Settings
            >>> wait_activity("com.example.app.MainActivity", 30)  # Wait 30 seconds
            >>> wait_activity(".LoginActivity")  # Relative activity name

        Note:
            Activity names can be fully qualified (package + activity) or
            relative to the app package starting with a dot (.).
        """
        try:
            d = get_device(device_id)
            return d.wait_activity(activity, timeout=timeout)
        except Exception as e:
            print(f"Failed to wait for activity {activity}: {str(e)}", file=sys.stderr)
            return False
