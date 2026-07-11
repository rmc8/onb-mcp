from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import MAX_LIMIT, generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="list_sources",
        summary="Get all sources with optional filtering.",
        tags=("sources", "list", "query"),
        args={"notebook_id": "Optional[str]", "limit": "int", "offset": "int"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123", "limit": 20, "offset": 0},
        typical_bytes=3000,
    ),
    Capability(
        name="get_source",
        summary="Get a specific source by ID.",
        tags=("sources", "get", "read"),
        args={"source_id": "str"},
        returns="dict[str, Any]",
        example={"source_id": "source:abc123"},
        typical_bytes=2000,
    ),
    Capability(
        name="create_source",
        summary="Create a new source (link, upload, or text).",
        tags=("sources", "create", "write"),
        args={
            "notebook_id": "str",
            "type": "str",
            "url": "Optional[str]",
            "title": "Optional[str]",
            "embed": "bool",
        },
        returns="dict[str, Any]",
        example={
            "notebook_id": "notebook:abc123",
            "type": "link",
            "url": "https://example.com",
            "embed": True,
        },
        typical_bytes=2000,
    ),
    Capability(
        name="update_source",
        summary="Update a source.",
        tags=("sources", "update", "write"),
        args={
            "source_id": "str",
            "title": "Optional[str]",
            "topics": "Optional[list[str]]",
        },
        returns="dict[str, Any]",
        example={"source_id": "source:abc123", "title": "New Title"},
        typical_bytes=2000,
    ),
    Capability(
        name="delete_source",
        summary="Delete a source.",
        tags=("sources", "delete", "write"),
        args={"source_id": "str"},
        returns="dict[str, Any]",
        example={"source_id": "source:abc123"},
        typical_bytes=100,
    ),
)


@mcp.tool()
async def list_sources(
    notebook_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Get all sources with optional filtering.

    Args:
        notebook_id: Optional notebook ID to filter by
        limit: Maximum number of results (1-100)
        offset: Pagination offset

    Returns:
        Dictionary with sources list and metadata
    """
    limit = max(1, min(limit, MAX_LIMIT))
    params = {"limit": limit, "offset": offset}
    if notebook_id is not None:
        params["notebook_id"] = notebook_id

    sources = await make_request("GET", "/api/sources", params=params)
    return {
        "request_id": generate_request_id(),
        "count": len(sources) if isinstance(sources, list) else 0,
        "sources": sources,
    }


@mcp.tool()
async def get_source(source_id: str) -> dict[str, Any]:
    """Get a specific source by ID.

    Args:
        source_id: Source ID (e.g., 'source:abc123')

    Returns:
        Source details
    """
    source = await make_request("GET", f"/api/sources/{source_id}")
    return {
        "request_id": generate_request_id(),
        "source": source,
    }


@mcp.tool()
async def create_source(
    notebook_id: str,
    type: str,
    url: Optional[str] = None,
    title: Optional[str] = None,
    embed: bool = True,
) -> dict[str, Any]:
    """Create a new source (link, upload, or text).

    Args:
        notebook_id: Notebook ID to add source to
        type: Source type ('link', 'upload', or 'text')
        url: URL for link type sources
        title: Optional title
        embed: Whether to generate embeddings (default: True)

    Returns:
        Created source details
    """
    data = {
        "notebook_id": notebook_id,
        "type": type,
        "embed": embed,
    }
    if url is not None:
        data["url"] = url
    if title is not None:
        data["title"] = title

    source = await make_request("POST", "/api/sources/json", json_data=data)
    return {
        "request_id": generate_request_id(),
        "source": source,
    }


@mcp.tool()
async def update_source(
    source_id: str,
    title: Optional[str] = None,
    topics: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Update a source.

    Args:
        source_id: Source ID
        title: Optional new title
        topics: Optional list of topics

    Returns:
        Updated source details
    """
    data = {}
    if title is not None:
        data["title"] = title
    if topics is not None:
        data["topics"] = topics

    source = await make_request("PUT", f"/api/sources/{source_id}", json_data=data)
    return {
        "request_id": generate_request_id(),
        "source": source,
    }


@mcp.tool()
async def delete_source(source_id: str) -> dict[str, Any]:
    """Delete a source.

    Args:
        source_id: Source ID

    Returns:
        Success message
    """
    result = await make_request("DELETE", f"/api/sources/{source_id}")
    return {
        "request_id": generate_request_id(),
        "result": result,
    }
