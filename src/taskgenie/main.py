"""
TaskGenie entry point.

Loads configuration and starts the MCP server.
Corresponds to the `if __name__ == "__main__"` block in the
reference repository's server.py.
"""

from taskgenie.server import mcp, config


def main() -> None:
    """Start the TaskGenie MCP server using settings from configuration."""
    mcp.run(
        transport=config.server.transport,
        host=config.server.host,
        port=config.server.port,
    )


if __name__ == "__main__":
    main()
