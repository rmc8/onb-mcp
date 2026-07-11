from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import MAX_LIMIT, generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="list_notebooks",
        summary="Get all notebooks with optional filtering and ordering.",
        tags=("notebooks", "list", "query"),
        args={"archived": "Optional[bool]", "order_by": "str", "limit": "int"},
        returns="dict[str, Any]",
        example={"archived": False, "order_by": "updated desc", "limit": 20},
        typical_bytes=2000,
    ),
    Capability(
        name="get_notebook",
        summary="Get a specific notebook by ID.",
        tags=("notebooks", "get", "read"),
        args={"notebook_id": "str"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123"},
        typical_bytes=500,
    ),
    Capability(
        name="create_notebook",
        summary="Create a new notebook.",
        tags=("notebooks", "create", "write"),
        args={"name": "str", "description": "Optional[str]"},
        returns="dict[str, Any]",
        example={"name": "My Research", "description": "AI research notebook"},
        typical_bytes=500,
    ),
    Capability(
        name="update_notebook",
        summary="Update a notebook.",
        tags=("notebooks", "update", "write"),
        args={
            "notebook_id": "str",
            "name": "Optional[str]",
            "description": "Optional[str]",
            "archived": "Optional[bool]",
        },
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123", "name": "Updated Name"},
        typical_bytes=500,
    ),
    Capability(
        name="delete_notebook",
        summary="Delete a notebook.",
        tags=("notebooks", "delete", "write"),
        args={"notebook_id": "str"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123"},
        typical_bytes=100,
    ),
)


@mcp.tool()
async def list_notebooks(
    archived: Optional[bool] = None,
    order_by: str = "updated desc",
    limit: int = 20,
) -> dict[str, Any]:
    """Get all notebooks with optional filtering and ordering.

    Args:
        archived: Filter by archived status (None = all, True = archived only, False = active only)
        order_by: Order by field and direction (e.g., 'created desc', 'name asc')
        limit: Maximum number of results (1-100)

    Returns:
        Dictionary with notebooks list and metadata
    """
    limit = max(1, min(limit, MAX_LIMIT))
    params = {"order_by": order_by}
    if archived is not None:
        params["archived"] = archived

    notebooks = await make_request("GET", "/api/notebooks", params=params)

    # Limit results
    if isinstance(notebooks, list):
        notebooks = notebooks[:limit]

    return {
        "request_id": generate_request_id(),
        "count": len(notebooks) if isinstance(notebooks, list) else 0,
        "notebooks": notebooks,
    }


@mcp.tool()
async def get_notebook(notebook_id: str) -> dict[str, Any]:
    """Get a specific notebook by ID.

    Args:
        notebook_id: Notebook ID (e.g., 'notebook:abc123')

    Returns:
        Notebook details
    """
    notebook = await make_request("GET", f"/api/notebooks/{notebook_id}")
    return {
        "request_id": generate_request_id(),
        "notebook": notebook,
    }


@mcp.tool()
async def create_notebook(
    name: str, description: Optional[str] = None
) -> dict[str, Any]:
    """Create a new notebook.

    Args:
        name: Notebook name
        description: Optional notebook description

    Returns:
        Created notebook details
    """
    data = {"name": name}
    if description is not None:
        data["description"] = description

    notebook = await make_request("POST", "/api/notebooks", json_data=data)
    return {
        "request_id": generate_request_id(),
        "notebook": notebook,
    }


@mcp.tool()
async def update_notebook(
    notebook_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    archived: Optional[bool] = None,
) -> dict[str, Any]:
    """Update a notebook.

    Args:
        notebook_id: Notebook ID
        name: Optional new name
        description: Optional new description
        archived: Optional archived status

    Returns:
        Updated notebook details
    """
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if archived is not None:
        data["archived"] = archived

    notebook = await make_request(
        "PUT", f"/api/notebooks/{notebook_id}", json_data=data
    )
    return {
        "request_id": generate_request_id(),
        "notebook": notebook,
    }


@mcp.tool()
async def delete_notebook(notebook_id: str) -> dict[str, Any]:
    """Delete a notebook.

    Args:
        notebook_id: Notebook ID

    Returns:
        Success message
    """
    result = await make_request("DELETE", f"/api/notebooks/{notebook_id}")
    return {
        "request_id": generate_request_id(),
        "result": result,
    }
