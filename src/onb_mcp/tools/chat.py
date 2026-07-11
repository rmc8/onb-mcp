from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import MAX_LIMIT, generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="list_chat_sessions",
        summary="Get all chat sessions with optional filtering.",
        tags=("chat", "sessions", "list"),
        args={"notebook_id": "Optional[str]", "limit": "int"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123", "limit": 20},
        typical_bytes=2000,
    ),
    Capability(
        name="create_chat_session",
        summary="Create a new chat session.",
        tags=("chat", "sessions", "create", "write"),
        args={"notebook_id": "str", "title": "str"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123", "title": "Research Discussion"},
        typical_bytes=500,
    ),
    Capability(
        name="get_chat_session",
        summary="Get a specific chat session by ID.",
        tags=("chat", "sessions", "get", "read"),
        args={"session_id": "str"},
        returns="dict[str, Any]",
        example={"session_id": "session:abc123"},
        typical_bytes=3000,
    ),
    Capability(
        name="update_chat_session",
        summary="Update a chat session.",
        tags=("chat", "sessions", "update", "write"),
        args={"session_id": "str", "title": "Optional[str]"},
        returns="dict[str, Any]",
        example={"session_id": "session:abc123", "title": "Updated Title"},
        typical_bytes=500,
    ),
    Capability(
        name="delete_chat_session",
        summary="Delete a chat session.",
        tags=("chat", "sessions", "delete", "write"),
        args={"session_id": "str"},
        returns="dict[str, Any]",
        example={"session_id": "session:abc123"},
        typical_bytes=100,
    ),
    Capability(
        name="execute_chat",
        summary="Send a message in a chat session.",
        tags=("chat", "execute", "message", "ai"),
        args={"session_id": "str", "message": "str", "context": "Optional[dict]"},
        returns="dict[str, Any]",
        example={
            "session_id": "session:abc123",
            "message": "What are the key insights?",
        },
        typical_bytes=3000,
    ),
    Capability(
        name="get_chat_context",
        summary="Build context for a chat conversation.",
        tags=("chat", "context", "build"),
        args={"notebook_id": "str", "context_config": "Optional[dict]"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123"},
        typical_bytes=5000,
    ),
)


@mcp.tool()
async def list_chat_sessions(
    notebook_id: Optional[str] = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Get all chat sessions with optional filtering.

    Args:
        notebook_id: Optional notebook ID to filter by
        limit: Maximum number of results (1-100)

    Returns:
        Dictionary with sessions list and metadata
    """
    limit = max(1, min(limit, MAX_LIMIT))
    params = {}
    if notebook_id is not None:
        params["notebook_id"] = notebook_id

    sessions = await make_request("GET", "/api/chat/sessions", params=params)

    if isinstance(sessions, list):
        sessions = sessions[:limit]

    return {
        "request_id": generate_request_id(),
        "count": len(sessions) if isinstance(sessions, list) else 0,
        "sessions": sessions,
    }


@mcp.tool()
async def create_chat_session(notebook_id: str, title: str) -> dict[str, Any]:
    """Create a new chat session.

    Args:
        notebook_id: Notebook ID for the session
        title: Session title

    Returns:
        Created session details
    """
    data = {
        "notebook_id": notebook_id,
        "title": title,
    }

    session = await make_request("POST", "/api/chat/sessions", json_data=data)
    return {
        "request_id": generate_request_id(),
        "session": session,
    }


@mcp.tool()
async def get_chat_session(session_id: str) -> dict[str, Any]:
    """Get a specific chat session by ID.

    Args:
        session_id: Session ID (e.g., 'session:abc123')

    Returns:
        Session details with message history
    """
    session = await make_request("GET", f"/api/chat/sessions/{session_id}")
    return {
        "request_id": generate_request_id(),
        "session": session,
    }


@mcp.tool()
async def update_chat_session(
    session_id: str,
    title: Optional[str] = None,
) -> dict[str, Any]:
    """Update a chat session.

    Args:
        session_id: Session ID
        title: Optional new title

    Returns:
        Updated session details
    """
    data = {}
    if title is not None:
        data["title"] = title

    session = await make_request(
        "PUT", f"/api/chat/sessions/{session_id}", json_data=data
    )
    return {
        "request_id": generate_request_id(),
        "session": session,
    }


@mcp.tool()
async def delete_chat_session(session_id: str) -> dict[str, Any]:
    """Delete a chat session.

    Args:
        session_id: Session ID

    Returns:
        Success message
    """
    result = await make_request("DELETE", f"/api/chat/sessions/{session_id}")
    return {
        "request_id": generate_request_id(),
        "result": result,
    }


@mcp.tool()
async def execute_chat(
    session_id: str,
    message: str,
    context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Send a message in a chat session.

    Args:
        session_id: Session ID
        message: Message to send
        context: Optional context data for the conversation

    Returns:
        Chat response with AI message
    """
    data = {
        "session_id": session_id,
        "message": message,
    }
    if context is not None:
        data["context"] = context

    response = await make_request("POST", "/api/chat/execute", json_data=data)
    return {
        "request_id": generate_request_id(),
        "response": response,
    }


@mcp.tool()
async def get_chat_context(
    notebook_id: str,
    context_config: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Build context for a chat conversation.

    Args:
        notebook_id: Notebook ID
        context_config: Optional context configuration

    Returns:
        Built context data
    """
    data = {
        "notebook_id": notebook_id,
    }
    if context_config is not None:
        data["context_config"] = context_config

    context = await make_request("POST", "/api/chat/context", json_data=data)
    return {
        "request_id": generate_request_id(),
        "context": context,
    }
