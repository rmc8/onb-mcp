from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="generate_podcast",
        summary="Generate a new podcast episode asynchronously from selected sources.",
        tags=("podcasts", "generate", "audio", "async"),
        args={
            "notebook_id": "str",
            "episode_name": "str",
            "episode_profile": "str",
            "speaker_profile": "str",
            "content": "Optional[str]",
            "briefing_suffix": "Optional[str]",
        },
        returns="dict[str, Any]",
        example={
            "notebook_id": "notebook:abc123",
            "episode_name": "AI Safety Debate",
            "episode_profile": "Academic Presentation",
            "speaker_profile": "Expert Interview",
        },
        typical_bytes=1000,
    ),
    Capability(
        name="retry_podcast",
        summary="Retry a failed podcast episode generation job.",
        tags=("podcasts", "retry", "audio", "async"),
        args={
            "episode_id": "str",
        },
        returns="dict[str, Any]",
        example={
            "episode_id": "episode:xyz987",
        },
        typical_bytes=1000,
    ),
    Capability(
        name="get_podcast_job_status",
        summary="Get the status of an asynchronous podcast generation job.",
        tags=("podcasts", "status", "job", "track"),
        args={
            "job_id": "str",
        },
        returns="dict[str, Any]",
        example={
            "job_id": "job:cmd123",
        },
        typical_bytes=1500,
    ),
)


@mcp.tool()
async def generate_podcast(
    notebook_id: str,
    episode_name: str,
    episode_profile: str,
    speaker_profile: str,
    content: Optional[str] = None,
    briefing_suffix: Optional[str] = None,
) -> dict[str, Any]:
    """Generate a new podcast episode asynchronously.

    Args:
        notebook_id: The ID of the notebook
        episode_name: The name/title of the generated episode
        episode_profile: Name of the EpisodeProfile configuration (e.g. 'Academic Presentation')
        speaker_profile: Name of the SpeakerProfile configuration
        content: Optional custom text content override
        briefing_suffix: Optional briefing suffix text

    Returns:
        Job command details
    """
    data = {
        "notebook_id": notebook_id,
        "episode_name": episode_name,
        "episode_profile": episode_profile,
        "speaker_profile": speaker_profile,
    }
    if content is not None:
        data["content"] = content
    if briefing_suffix is not None:
        data["briefing_suffix"] = briefing_suffix

    result = await make_request("POST", "/api/podcasts/generate", json_data=data)
    return {
        "request_id": generate_request_id(),
        "command": result,
    }


@mcp.tool()
async def retry_podcast(episode_id: str) -> dict[str, Any]:
    """Retry a failed podcast episode generation job.

    Args:
        episode_id: The ID of the failed episode

    Returns:
        Job command details
    """
    result = await make_request(
        "POST", f"/api/podcasts/episodes/{episode_id}/retry"
    )
    return {
        "request_id": generate_request_id(),
        "command": result,
    }


@mcp.tool()
async def get_podcast_job_status(job_id: str) -> dict[str, Any]:
    """Get the status of an asynchronous podcast generation job.

    Args:
        job_id: The ID of the generation job

    Returns:
        Job status details
    """
    result = await make_request("GET", f"/api/podcasts/jobs/{job_id}")
    return {
        "request_id": generate_request_id(),
        "status": result,
    }
