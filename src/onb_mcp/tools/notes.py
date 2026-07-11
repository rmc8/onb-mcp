from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import MAX_LIMIT, generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="list_notes",
        summary="Get all notes with optional filtering.",
        tags=("notes", "list", "query"),
        args={"notebook_id": "Optional[str]", "limit": "int", "offset": "int"},
        returns="dict[str, Any]",
        example={"notebook_id": "notebook:abc123", "limit": 20, "offset": 0},
        typical_bytes=2000,
    ),
    Capability(
        name="get_note",
        summary="Get a specific note by ID.",
        tags=("notes", "get", "read"),
        args={"note_id": "str"},
        returns="dict[str, Any]",
        example={"note_id": "note:abc123"},
        typical_bytes=1500,
    ),
    Capability(
        name="create_note",
        summary="Create a new note.",
        tags=("notes", "create", "write"),
        args={
            "notebook_id": "str",
            "title": "str",
            "content": "str",
            "topics": "Optional[list[str]]",
        },
        returns="dict[str, Any]",
        example={
            "notebook_id": "notebook:abc123",
            "title": "My Note",
            "content": "Note content",
        },
        typical_bytes=1500,
    ),
    Capability(
        name="update_note",
        summary="Update a note.",
        tags=("notes", "update", "write"),
        args={
            "note_id": "str",
            "title": "Optional[str]",
            "content": "Optional[str]",
            "topics": "Optional[list[str]]",
        },
        returns="dict[str, Any]",
        example={"note_id": "note:abc123", "title": "Updated Title"},
        typical_bytes=1500,
    ),
    Capability(
        name="delete_note",
        summary="Delete a note.",
        tags=("notes", "delete", "write"),
        args={"note_id": "str"},
        returns="dict[str, Any]",
        example={"note_id": "note:abc123"},
        typical_bytes=100,
    ),
)


@mcp.tool()
async def list_notes(
    notebook_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Get all notes with optional filtering.

    Args:
        notebook_id: Optional notebook ID to filter by
        limit: Maximum number of results (1-100)
        offset: Pagination offset

    Returns:
        Dictionary with notes list and metadata
    """
    limit = max(1, min(limit, MAX_LIMIT))
    params = {"limit": limit, "offset": offset}
    if notebook_id is not None:
        params["notebook_id"] = notebook_id

    notes = await make_request("GET", "/api/notes", params=params)
    return {
        "request_id": generate_request_id(),
        "count": len(notes) if isinstance(notes, list) else 0,
        "notes": notes,
    }


@mcp.tool()
async def get_note(note_id: str) -> dict[str, Any]:
    """Get a specific note by ID.

    Args:
        note_id: Note ID (e.g., 'note:abc123')

    Returns:
        Note details
    """
    note = await make_request("GET", f"/api/notes/{note_id}")
    return {
        "request_id": generate_request_id(),
        "note": note,
    }


@mcp.tool()
async def create_note(
    notebook_id: str,
    title: str,
    content: str,
    topics: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Create a new note.

    Args:
        notebook_id: Notebook ID to add note to
        title: Note title
        content: Note content
        topics: Optional list of topics

    Returns:
        Created note details
    """
    data = {
        "notebook_id": notebook_id,
        "title": title,
        "content": content,
    }
    if topics is not None:
        data["topics"] = topics

    note = await make_request("POST", "/api/notes", json_data=data)
    return {
        "request_id": generate_request_id(),
        "note": note,
    }


@mcp.tool()
async def update_note(
    note_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    topics: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Update a note.

    Args:
        note_id: Note ID
        title: Optional new title
        content: Optional new content
        topics: Optional list of topics

    Returns:
        Updated note details
    """
    data = {}
    if title is not None:
        data["title"] = title
    if content is not None:
        data["content"] = content
    if topics is not None:
        data["topics"] = topics

    note = await make_request("PUT", f"/api/notes/{note_id}", json_data=data)
    return {
        "request_id": generate_request_id(),
        "note": note,
    }


@mcp.tool()
async def delete_note(note_id: str) -> dict[str, Any]:
    """Delete a note.

    Args:
        note_id: Note ID

    Returns:
        Success message
    """
    result = await make_request("DELETE", f"/api/notes/{note_id}")
    return {
        "request_id": generate_request_id(),
        "result": result,
    }
