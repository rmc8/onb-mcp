from __future__ import annotations

import os
from .mcp_app import mcp
from .capabilities import CAPABILITIES
from .tools.meta import search_capabilities
from . import tools  # noqa: F401

__all__ = ["mcp", "CAPABILITIES", "search_capabilities", "main"]


def main() -> None:
    """Main entry point for the MCP server."""
    # Default: stdio (Codex/local)
    transport = os.getenv("MCP_TRANSPORT", "stdio").strip().lower()

    if transport == "stdio":
        mcp.run(transport="stdio")
        return

    # Streamable HTTP (prod/remote)
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    path = os.getenv("MCP_PATH", "/mcp")
    stateless_http = os.getenv("STATELESS_HTTP", "1") == "1"
    json_response = os.getenv("JSON_RESPONSE", "1") == "1"

    # Configure server settings dynamically before running
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.settings.streamable_http_path = path
    mcp.settings.stateless_http = stateless_http
    mcp.settings.json_response = json_response

    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
