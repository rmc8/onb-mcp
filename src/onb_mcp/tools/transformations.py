from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="list_transformations",
        summary="List all custom transformation prompts.",
        tags=("transformations", "list", "prompts"),
        args={},
        returns="dict[str, Any]",
        example={},
        typical_bytes=1000,
    ),
    Capability(
        name="create_transformation",
        summary="Create a new custom transformation prompt template.",
        tags=("transformations", "create", "prompts"),
        args={
            "name": "str",
            "prompt": "str",
            "description": "Optional[str]",
        },
        returns="dict[str, Any]",
        example={
            "name": "Extract Key Findings",
            "prompt": "Extract the main findings from: {content}",
            "description": "Extracts the main findings",
        },
        typical_bytes=1500,
    ),
    Capability(
        name="apply_transformation",
        summary="Apply a transformation prompt template to a source to extract insights.",
        tags=("transformations", "apply", "run", "insights"),
        args={
            "source_id": "str",
            "transformation_id": "str",
        },
        returns="dict[str, Any]",
        example={
            "source_id": "source:abc123",
            "transformation_id": "trans:xyz789",
        },
        typical_bytes=4000,
    ),
)


@mcp.tool()
async def list_transformations() -> dict[str, Any]:
    """List available custom transformation prompts.

    Returns:
        List of transformations
    """
    result = await make_request("GET", "/api/transformations")
    return {
        "request_id": generate_request_id(),
        "transformations": (
            result.get("transformations", [])
            if isinstance(result, dict)
            else result
        ),
    }


@mcp.tool()
async def create_transformation(
    name: str,
    prompt: str,
    description: Optional[str] = None,
) -> dict[str, Any]:
    """Create a new custom transformation prompt.

    Args:
        name: Name of the transformation
        prompt: The prompt template (e.g., 'Summarize: {content}')
        description: Optional description of the transformation

    Returns:
        Created transformation details
    """
    data = {
        "name": name,
        "prompt": prompt,
    }
    if description is not None:
        data["description"] = description

    result = await make_request("POST", "/api/transformations", json_data=data)
    return {
        "request_id": generate_request_id(),
        "transformation": result,
    }


@mcp.tool()
async def apply_transformation(
    source_id: str,
    transformation_id: str,
) -> dict[str, Any]:
    """Apply a transformation template to a specific source to extract insights.

    Args:
        source_id: The ID of the source (e.g., 'source:abc123')
        transformation_id: The ID of the transformation (e.g., 'trans:xyz789')

    Returns:
        Extracted insights
    """
    data = {
        "transformation_id": transformation_id,
    }
    result = await make_request(
        "POST", f"/api/sources/{source_id}/insights", json_data=data
    )
    return {
        "request_id": generate_request_id(),
        "insights": (
            result.get("insights") if isinstance(result, dict) else result
        ),
    }
