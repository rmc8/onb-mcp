from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="list_credentials",
        summary="List all stored credentials.",
        tags=("credentials", "list", "providers"),
        args={"provider": "Optional[str]"},
        returns="dict[str, Any]",
        example={"provider": "openai"},
        typical_bytes=2000,
    ),
    Capability(
        name="test_credential",
        summary="Test connection for a specific provider credential.",
        tags=("credentials", "test", "providers"),
        args={"credential_id": "str"},
        returns="dict[str, Any]",
        example={"credential_id": "cred:openai123"},
        typical_bytes=1000,
    ),
    Capability(
        name="discover_models",
        summary="Discover available models from a specific credential provider.",
        tags=("credentials", "discover", "models"),
        args={"credential_id": "str"},
        returns="dict[str, Any]",
        example={"credential_id": "cred:openai123"},
        typical_bytes=2000,
    ),
    Capability(
        name="register_models",
        summary="Register discovered models for use in the system.",
        tags=("credentials", "register", "models"),
        args={"credential_id": "str"},
        returns="dict[str, Any]",
        example={"credential_id": "cred:openai123"},
        typical_bytes=1000,
    ),
)


@mcp.tool()
async def list_credentials(provider: Optional[str] = None) -> dict[str, Any]:
    """List all stored provider credentials.

    Args:
        provider: Optional provider filter (e.g. 'openai')

    Returns:
        List of credentials
    """
    params = {}
    if provider is not None:
        params["provider"] = provider
    result = await make_request("GET", "/api/credentials", params=params)
    return {
        "request_id": generate_request_id(),
        "credentials": result,
    }


@mcp.tool()
async def test_credential(credential_id: str) -> dict[str, Any]:
    """Test connection using a specific provider credential.

    Args:
        credential_id: The ID of the credential to test

    Returns:
        Test result details
    """
    result = await make_request(
        "POST", f"/api/credentials/{credential_id}/test"
    )
    return {
        "request_id": generate_request_id(),
        "result": result,
    }


@mcp.tool()
async def discover_models(credential_id: str) -> dict[str, Any]:
    """Discover available models for a specific credential provider.

    Args:
        credential_id: The ID of the credential

    Returns:
        Discovered models list
    """
    result = await make_request(
        "POST", f"/api/credentials/{credential_id}/discover"
    )
    return {
        "request_id": generate_request_id(),
        "discovered_models": result,
    }


@mcp.tool()
async def register_models(credential_id: str) -> dict[str, Any]:
    """Register discovered models for the provider.

    Args:
        credential_id: The ID of the credential

    Returns:
        Registration status details
    """
    result = await make_request(
        "POST", f"/api/credentials/{credential_id}/register-models"
    )
    return {
        "request_id": generate_request_id(),
        "result": result,
    }
