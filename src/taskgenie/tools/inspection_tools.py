"""UI element inspection and hierarchy analysis tools for Android automation."""

import sys
import uiautomator2 as u2
from typing import Optional, TypedDict, Dict, Any


# Type definitions for element info
class ElementInfo(TypedDict):
    text: str
    resourceId: str
    description: str
    className: str
    enabled: bool
    clickable: bool
    bounds: Dict[str, Any]
    selected: bool
    focused: bool


def register_inspection_tools(mcp):
    """Register all inspection related tools with the MCP server."""

    @mcp.tool(
        name="get_element_info",
        description="Get detailed information about a UI element including its properties, bounds, text, resource ID, class name, and interaction capabilities.",
    )
    def get_element_info(
        selector: str,
        selector_type: str = "text",
        timeout: float = 10.0,
        device_id: Optional[str] = None,
    ) -> ElementInfo:
        """Retrieve detailed information about a UI element.

        This function finds an element and returns comprehensive information about
        its properties, useful for debugging automation scripts or element inspection.

        Args:
            selector: The value to search for (text, resource ID, or content description)
            selector_type: The type of selector ('text', 'resourceId', or 'description')
            timeout: Maximum time in seconds to wait for the element (default: 10.0)
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            ElementInfo dictionary containing:
                - text: Visible text on the element
                - resourceId: Android resource ID
                - description: Content description/accessibility label
                - className: Android class name (e.g., "android.widget.Button")
                - enabled: Whether the element is enabled
                - clickable: Whether the element can be clicked
                - bounds: Element position and size {"left": x, "top": y, "right": x2, "bottom": y2}
                - selected: Whether the element is selected
                - focused: Whether the element has focus

            Returns empty dictionary if element not found.
        """
        try:
            d = u2.connect(device_id)
            if selector_type == "text":
                el = d(text=selector).wait(timeout=timeout)
            elif selector_type == "resourceId":
                el = d(resourceId=selector).wait(timeout=timeout)
            elif selector_type == "description":
                el = d(description=selector).wait(timeout=timeout)
            else:
                raise ValueError(f"Invalid selector_type: {selector_type}")

            if el and el.exists:
                info = el.info
                return {
                    "text": info.get("text", ""),
                    "resourceId": info.get("resourceId", ""),
                    "description": info.get("contentDescription", ""),
                    "className": info.get("className", ""),
                    "enabled": info.get("enabled", False),
                    "clickable": info.get("clickable", False),
                    "bounds": info.get("bounds", {}),
                    "selected": info.get("selected", False),
                    "focused": info.get("focused", False),
                }
            return {}
        except Exception as e:
            print(f"Failed to get element info for {selector}: {str(e)}", file=sys.stderr)
            return {}

    @mcp.tool(
        name="wait_for_element",
        description="Wait for a UI element to appear on the screen. Essential for handling loading screens, animations, and dynamic content.",
    )
    def wait_for_element(
        selector: str,
        selector_type: str = "text",
        timeout: float = 10.0,
        device_id: Optional[str] = None,
    ) -> bool:
        """Wait for a UI element to appear on the device screen.

        This function pauses execution until the specified element becomes visible
        or the timeout is reached. Essential for reliable automation.

        Args:
            selector: The value to search for (text, resource ID, or content description)
            selector_type: The type of selector ('text', 'resourceId', or 'description')
            timeout: Maximum time in seconds to wait (default: 10.0)
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            bool: True if the element appeared within the timeout, False otherwise

        Examples:
            >>> wait_for_element("Loading complete", "text", 30)  # Wait up to 30 seconds
            >>> wait_for_element("com.app:id/result", "resourceId")  # Wait for resource ID
            >>> wait_for_element("Submit button", "description")  # Wait by content description

        Note:
            Use this function when dealing with dynamic content, loading screens,
            or network-dependent elements that may take time to appear.
        """
        try:
            d = u2.connect(device_id)
            if selector_type == "text":
                return d(text=selector).wait(timeout=timeout)
            elif selector_type == "resourceId":
                return d(resourceId=selector).wait(timeout=timeout)
            elif selector_type == "description":
                el = d(description=selector).wait(timeout=timeout)
                return el is not None and el.exists
            else:
                raise ValueError(f"Invalid selector_type: {selector_type}")
        except Exception as e:
            print(f"Failed to wait for element {selector}: {str(e)}", file=sys.stderr)
            return False
