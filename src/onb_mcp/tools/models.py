from __future__ import annotations
from typing import Any

from ..mcp_app import mcp
from ..config import MAX_LIMIT, generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="list_models",
        summary="Get all configured AI models.",
        tags=("models", "list", "ai"),
        args={"limit": "int"},
        returns="dict[str, Any]",
        example={"limit": 50},
        typical_bytes=2000,
    ),
    Capability(
        name="get_model",
        summary="Get a specific model by ID.",
        tags=("models", "get", "read", "ai"),
        args={"model_id": "str"},
        returns="dict[str, Any]",
        example={"model_id": "model:abc123"},
        typical_bytes=500,
    ),
    Capability(
        name="create_model",
        summary="Create a new AI model configuration.",
        tags=("models", "create", "write", "ai"),
        args={"name": "str", "provider": "str", "type": "str"},
        returns="dict[str, Any]",
        example={"name": "gpt-4", "provider": "openai", "type": "language"},
        typical_bytes=500,
    ),
    Capability(
        name="delete_model",
        summary="Delete a model configuration.",
        tags=("models", "delete", "write", "ai"),
        args={"model_id": "str"},
        returns="dict[str, Any]",
        example={"model_id": "model:abc123"},
        typical_bytes=100,
    ),
    Capability(
        name="get_default_models",
        summary="Get default model configurations.",
        tags=("models", "defaults", "ai"),
        args={},
        returns="dict[str, Any]",
        example={},
        typical_bytes=1000,
    ),
)


@mcp.tool()
async def list_models(limit: int = 50) -> dict[str, Any]:
    """Get all configured AI models.

    Args:
        limit: Maximum number of results (1-100)

    Returns:
        Dictionary with models list and metadata
    """
    limit = max(1, min(limit, MAX_LIMIT))
    models = await make_request("GET", "/api/models")

    if isinstance(models, list):
        models = models[:limit]

    return {
        "request_id": generate_request_id(),
        "count": len(models) if isinstance(models, list) else 0,
        "models": models,
    }


@mcp.tool()
async def get_model(model_id: str) -> dict[str, Any]:
    """Get a specific model by ID.

    Args:
        model_id: Model ID (e.g., 'model:abc123')

    Returns:
        Model details
    """
    model = await make_request("GET", f"/api/models/{model_id}")
    return {
        "request_id": generate_request_id(),
        "model": model,
    }


@mcp.tool()
async def create_model(name: str, provider: str, type: str) -> dict[str, Any]:
    """Create a new AI model configuration.

    Args:
        name: Model name (e.g., 'gpt-4', 'claude-3-opus')
        provider: Provider name (e.g., 'openai', 'anthropic')
        type: Model type (e.g., 'language', 'embedding')

    Returns:
        Created model details
    """
    data = {
        "name": name,
        "provider": provider,
        "type": type,
    }

    model = await make_request("POST", "/api/models", json_data=data)
    return {
        "request_id": generate_request_id(),
        "model": model,
    }


@mcp.tool()
async def delete_model(model_id: str) -> dict[str, Any]:
    """Delete a model configuration.

    Args:
        model_id: Model ID

    Returns:
        Success message
    """
    result = await make_request("DELETE", f"/api/models/{model_id}")
    return {
        "request_id": generate_request_id(),
        "result": result,
    }


@mcp.tool()
async def get_default_models() -> dict[str, Any]:
    """Get default model configurations.

    Returns:
        Default models configuration
    """
    defaults = await make_request("GET", "/api/models/defaults")
    return {
        "request_id": generate_request_id(),
        "defaults": defaults,
    }
