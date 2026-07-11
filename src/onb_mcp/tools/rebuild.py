from __future__ import annotations
from typing import Any

from ..mcp_app import mcp
from ..config import generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="rebuild_embeddings",
        summary="Trigger a background job to rebuild the document vector embeddings.",
        tags=("embeddings", "rebuild", "index"),
        args={"notebook_id": "str"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123"},
        typical_bytes=1000,
    ),
)


@mcp.tool()
async def rebuild_embeddings(notebook_id: str) -> dict[str, Any]:
    """Trigger a background job to rebuild vector embeddings for a notebook.

    Args:
        notebook_id: The ID of the notebook to rebuild embeddings for

    Returns:
        Background job details
    """
    data = {
        "notebook_id": notebook_id,
    }
    result = await make_request("POST", "/api/rebuild", json_data=data)
    return {
        "request_id": generate_request_id(),
        "job": result,
    }
