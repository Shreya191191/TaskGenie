"""User input and gesture tools for Android automation."""

import sys
import uiautomator2 as u2
from typing import Optional


def register_input_tools(mcp):
    """Register all input and gesture related tools with the MCP server."""

    @mcp.tool(
        name="press_key",
        description="Press a hardware or software key on the device. Common keys include: home, back, menu, volume_up, volume_down, power, enter, delete",
    )
    def press_key(key: str, device_id: Optional[str] = None) -> bool:
        """Simulate pressing a key on the Android device.

        This function sends a key event to the device, simulating both hardware
        button presses and software key presses.

        Args:
            key: The key to press. Common values include:
                - 'home': Home button
                - 'back': Back button
                - 'menu': Menu button
                - 'volume_up', 'volume_down': Volume buttons
                - 'power': Power button
                - 'enter': Enter key
                - 'delete': Delete/backspace key
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            bool: True if the key press was sent successfully, False otherwise

        Examples:
            >>> press_key("home")  # Press home button
            >>> press_key("back")  # Go back
        """
        try:
            d = u2.connect(device_id)
            d.press(key)
            return True
        except Exception as e:
            print(f"Failed to press key {key}: {str(e)}", file=sys.stderr)
            return False

    @mcp.tool(
        name="send_text",
        description="Send text input to the currently focused UI element. Can optionally clear existing text before sending. Perfect for form filling, search boxes, and text fields.",
    )
    def send_text(
        text: str, clear: bool = True, device_id: Optional[str] = None
    ) -> bool:
        """Send text to the currently focused input element on the device.

        This function types text into whatever UI element currently has focus,
        such as text fields, search boxes, or forms.

        Args:
            text: The text to send to the focused element
            clear: Whether to clear any existing text before sending (default: True)
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            bool: True if the text was sent successfully, False otherwise

        Examples:
            >>> send_text("Hello World")  # Clear field and type "Hello World"
            >>> send_text("additional text", clear=False)  # Append to existing text
            >>> send_text("user@example.com")  # Type an email address

        Note:
            Make sure the target text field is focused before calling this function.
            Use click() to focus a text field if needed.
        """
        try:
            d = u2.connect(device_id)
            d.send_keys(text, clear=clear)
            return True
        except Exception as e:
            print(f"Failed to send text: {str(e)}", file=sys.stderr)
            return False
