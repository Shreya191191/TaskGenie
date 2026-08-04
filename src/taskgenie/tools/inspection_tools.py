import os
import shutil
import subprocess
import sys
import uiautomator2 as u2
from typing import Optional, TypedDict, Dict, Any


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
            d = get_device(device_id)
            if selector_type == "text":
                obj = d(text=selector)
            elif selector_type == "resourceId":
                obj = d(resourceId=selector)
            elif selector_type == "description":
                obj = d(description=selector)
            else:
                raise ValueError(f"Invalid selector_type: {selector_type}")

            if obj.wait(timeout=timeout) and obj.exists:
                info = obj.info
                return {
                    "text": str(info.get("text") or ""),
                    "resourceId": str(info.get("resourceId") or ""),
                    "description": str(info.get("contentDescription") or ""),
                    "className": str(info.get("className") or ""),
                    "enabled": bool(info.get("enabled", False)),
                    "clickable": bool(info.get("clickable", False)),
                    "bounds": info.get("bounds") or {},
                    "selected": bool(info.get("selected", False)),
                    "focused": bool(info.get("focused", False)),
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
            d = get_device(device_id)
            if selector_type == "text":
                return bool(d(text=selector).wait(timeout=timeout))
            elif selector_type == "resourceId":
                return bool(d(resourceId=selector).wait(timeout=timeout))
            elif selector_type == "description":
                return bool(d(description=selector).wait(timeout=timeout))
            else:
                raise ValueError(f"Invalid selector_type: {selector_type}")
        except Exception as e:
            print(f"Failed to wait for element {selector}: {str(e)}", file=sys.stderr)
            return False

    @mcp.tool(
        name="scroll_to",
        description="Scroll to make a UI element visible on the screen. Automatically finds scrollable containers and scrolls until the target element becomes visible.",
    )
    def scroll_to(
        selector: str, selector_type: str = "text", device_id: Optional[str] = None
    ) -> bool:
        """Scroll to make a UI element visible on the screen.

        This function automatically finds scrollable containers and scrolls until
        the target element becomes visible. Useful for long lists and pages.

        Args:
            selector: The value to search for (text, resource ID, or content description)
            selector_type: The type of selector ('text', 'resourceId', or 'description')
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            bool: True if the element was found and scrolled into view, False otherwise
        """
        try:
            d = get_device(device_id)

            def get_target():
                if selector_type == "text":
                    return d(text=selector)
                elif selector_type == "resourceId":
                    return d(resourceId=selector)
                elif selector_type == "description":
                    return d(description=selector)
                else:
                    raise ValueError(f"Invalid selector_type: {selector_type}")

            # Check if target is already visible
            target = get_target()
            if target and target.exists:
                return True

            # Attempt 1: Native UiScrollable scroll.to
            try:
                if selector_type == "text":
                    res = d(scrollable=True).scroll.to(text=selector)
                elif selector_type == "resourceId":
                    res = d(scrollable=True).scroll.to(resourceId=selector)
                elif selector_type == "description":
                    res = d(scrollable=True).scroll.to(description=selector)
                else:
                    res = False

                if res and get_target().exists:
                    return True
            except Exception:
                pass

            # Attempt 2: Fallback multi-swipe loop (swipes up to 10 times until target appears)
            w, h = d.window_size()
            start_x, start_y = w // 2, int(h * 0.8)
            end_x, end_y = w // 2, int(h * 0.2)

            for _ in range(10):
                if get_target().exists:
                    return True
                d.swipe(start_x, start_y, end_x, end_y, duration=0.3)
                if get_target().exists:
                    return True

            return get_target().exists
        except Exception as e:
            print(f"Failed to scroll to element {selector}: {str(e)}", file=sys.stderr)
            return False

    @mcp.tool(
        name="screenshot",
        description="Capture a screenshot of the device screen and save it to the specified file path. Essential for debugging and visual verification.",
    )
    def screenshot(filename: str, device_id: Optional[str] = None) -> bool:
        """Take a screenshot of the device screen and save it to a file.

        This function captures the current screen state and saves it as an image file,
        which is useful for debugging automation failures and creating visual documentation.

        Args:
            filename: The file path where the screenshot will be saved (e.g., "screenshot.png")
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            bool: True if the screenshot was saved successfully, False otherwise

        Examples:
            >>> screenshot("login_screen.png")  # Save as PNG
            >>> screenshot("/path/to/screenshots/error.png")  # Save with full path
            >>> screenshot(f"test_{timestamp}.jpg")  # Dynamic filename

        Note:
            Supported formats include PNG, JPG, and other common image formats.
            The directory must exist and be writable.
        """
        try:
            d = get_device(device_id)
            if not os.path.isabs(filename):
                project_root = os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(os.path.abspath(__file__))
                        )
                    )
                )
                filepath = os.path.abspath(os.path.join(project_root, filename))
            else:
                filepath = os.path.abspath(filename)

            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            d.screenshot(filepath)
            return True
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}", file=sys.stderr)
            return False

    @mcp.tool(
        name="dump_hierarchy",
        description="Dump the complete UI hierarchy of the current screen as XML. Essential for understanding screen structure, finding elements, and debugging automation issues.",
    )
    def dump_hierarchy(
        compressed: bool = False,
        pretty: bool = True,
        max_depth: int = 50,
        device_id: Optional[str] = None,
    ) -> str:
        """Export the current screen's UI hierarchy as XML.

        This function provides a complete XML representation of all UI elements
        currently visible on the screen, which is invaluable for:
        - Finding elements for automation
        - Understanding screen structure
        - Debugging automation failures
        - Analyzing app UI changes

        Args:
            compressed: If True, excludes less important nodes for smaller output (default: False)
            pretty: If True, formats the XML with proper indentation (default: True)
            max_depth: Maximum depth of XML hierarchy to include (default: 50)
            device_id: Optional device identifier. If not provided, uses the first available device

        Returns:
            str: XML string representing the complete UI hierarchy

        Examples:
            >>> dump_hierarchy()  # Full pretty-formatted hierarchy
            >>> dump_hierarchy(compressed=True)  # Smaller output for debugging
            >>> dump_hierarchy(max_depth=10)  # Limited depth for faster processing

        Note:
            The output can be very large for complex screens. Use compressed=True
            for quicker analysis when you don't need all details.
        """
        try:
            d = get_device(device_id)
            xml = d.dump_hierarchy(
                compressed=compressed, pretty=pretty, max_depth=max_depth
            )
            return xml
        except Exception as e:
            print(f"Failed to dump UI hierarchy: {str(e)}", file=sys.stderr)
            return ""
