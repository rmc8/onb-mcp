from __future__ import annotations
from typing import Any

from ..mcp_app import mcp
from ..config import generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="get_settings",
        summary="Get application settings.",
        tags=("settings", "get", "config"),
        args={},
        returns="dict[str, Any]",
        example={},
        typical_bytes=1000,
    ),
    Capability(
        name="update_settings",
        summary="Update application settings.",
        tags=("settings", "update", "write", "config"),
        args={"settings": "dict"},
        returns="dict[str, Any]",
        example={"settings": {"theme": "dark"}},
        typical_bytes=1000,
    ),
)


@mcp.tool()
async def get_settings() -> dict[str, Any]:
    """Get application settings.

    Returns:
        Application settings
    """
    settings = await make_request("GET", "/api/settings")
    return {
        "request_id": generate_request_id(),
        "settings": settings,
    }


@mcp.tool()
async def update_settings(settings: dict[str, Any]) -> dict[str, Any]:
    """Update application settings.

    Args:
        settings: Settings dictionary to update

    Returns:
        Updated settings
    """
    result = await make_request("PUT", "/api/settings", json_data=settings)
    return {
        "request_id": generate_request_id(),
        "settings": result,
    }
