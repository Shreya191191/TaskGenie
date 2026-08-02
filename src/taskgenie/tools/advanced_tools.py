"""Advanced automation tools (toast messages, activity waiting)."""

import sys
import uiautomator2 as u2
from typing import Optional


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
            d = u2.connect(device_id)
            return d.toast.get_message(10.0) or ""
        except Exception as e:
            print(f"Failed to get toast message: {str(e)}", file=sys.stderr)
            return ""
