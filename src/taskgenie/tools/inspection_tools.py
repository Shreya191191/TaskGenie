"""UI element inspection and hierarchy analysis tools for Android automation."""

import uiautomator2 as u2
from typing import Optional, TypedDict, Dict, Any


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
    pass
