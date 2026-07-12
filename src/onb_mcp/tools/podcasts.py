from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    # ── Speaker Profile CRUD ──────────────────────────────────────────
    Capability(
        name="list_speaker_profiles",
        summary="List all speaker profiles.",
        tags=("speaker-profiles", "list", "query"),
        args={},
        returns="dict[str, Any]",
        example={},
        typical_bytes=2000,
    ),
    Capability(
        name="get_speaker_profile",
        summary="Get a specific speaker profile by ID.",
        tags=("speaker-profiles", "get", "read"),
        args={"profile_id": "str"},
        returns="dict[str, Any]",
        example={"profile_id": "speaker_profile:abc123"},
        typical_bytes=500,
    ),
    Capability(
        name="create_speaker_profile",
        summary="Create a new speaker profile.",
        tags=("speaker-profiles", "create", "write"),
        args={
            "name": "str",
            "description": "Optional[str]",
            "voice_model": "str",
            "speakers": "list",
            "tts_provider": "Optional[str]",
            "tts_model": "Optional[str]",
        },
        returns="dict[str, Any]",
        example={
            "name": "Expert Interview",
            "description": "Professional interview format",
            "voice_model": "model:abc123",
            "speakers": [{"name": "Guest", "backstory": "", "personality": ""}],
        },
        typical_bytes=500,
    ),
    Capability(
        name="update_speaker_profile",
        summary="Update an existing speaker profile.",
        tags=("speaker-profiles", "update", "write"),
        args={
            "profile_id": "str",
            "name": "Optional[str]",
            "description": "Optional[str]",
            "voice_model": "Optional[str]",
            "speakers": "Optional[list]",
            "tts_provider": "Optional[str]",
            "tts_model": "Optional[str]",
        },
        returns="dict[str, Any]",
        example={"profile_id": "speaker_profile:abc123", "name": "Updated Name"},
        typical_bytes=500,
    ),
    Capability(
        name="delete_speaker_profile",
        summary="Delete a speaker profile.",
        tags=("speaker-profiles", "delete", "write"),
        args={"profile_id": "str"},
        returns="dict[str, Any]",
        example={"profile_id": "speaker_profile:abc123"},
        typical_bytes=100,
    ),
    # ── Episode Profile CRUD ──────────────────────────────────────────
    Capability(
        name="list_episode_profiles",
        summary="List all episode profiles.",
        tags=("episode-profiles", "list", "query"),
        args={},
        returns="dict[str, Any]",
        example={},
        typical_bytes=2000,
    ),
    Capability(
        name="get_episode_profile",
        summary="Get a specific episode profile by ID.",
        tags=("episode-profiles", "get", "read"),
        args={"profile_id": "str"},
        returns="dict[str, Any]",
        example={"profile_id": "episode_profile:abc123"},
        typical_bytes=500,
    ),
    Capability(
        name="create_episode_profile",
        summary="Create a new episode profile.",
        tags=("episode-profiles", "create", "write"),
        args={
            "name": "str",
            "description": "Optional[str]",
            "speaker_config": "Optional[str]",
            "outline_llm": "Optional[str]",
            "transcript_llm": "Optional[str]",
            "language": "Optional[str]",
            "default_briefing": "Optional[str]",
            "num_segments": "Optional[int]",
            "max_tokens": "Optional[int]",
            "outline_provider": "Optional[str]",
            "outline_model": "Optional[str]",
            "transcript_provider": "Optional[str]",
            "transcript_model": "Optional[str]",
        },
        returns="dict[str, Any]",
        example={
            "name": "Academic Presentation",
            "description": "Formal academic podcast format",
            "language": "ja",
            "num_segments": 3,
            "max_tokens": 4000,
        },
        typical_bytes=500,
    ),
    Capability(
        name="update_episode_profile",
        summary="Update an existing episode profile.",
        tags=("episode-profiles", "update", "write"),
        args={
            "profile_id": "str",
            "name": "Optional[str]",
            "description": "Optional[str]",
            "speaker_config": "Optional[str]",
            "outline_llm": "Optional[str]",
            "transcript_llm": "Optional[str]",
            "language": "Optional[str]",
            "default_briefing": "Optional[str]",
            "num_segments": "Optional[int]",
            "max_tokens": "Optional[int]",
            "outline_provider": "Optional[str]",
            "outline_model": "Optional[str]",
            "transcript_provider": "Optional[str]",
            "transcript_model": "Optional[str]",
        },
        returns="dict[str, Any]",
        example={"profile_id": "episode_profile:abc123", "name": "Updated Name"},
        typical_bytes=500,
    ),
    Capability(
        name="delete_episode_profile",
        summary="Delete an episode profile.",
        tags=("episode-profiles", "delete", "write"),
        args={"profile_id": "str"},
        returns="dict[str, Any]",
        example={"profile_id": "episode_profile:abc123"},
        typical_bytes=100,
    ),
    # ── Podcast Generation (existing) ─────────────────────────────────
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


# ── Speaker Profile CRUD ──────────────────────────────────────────────


@mcp.tool()
async def list_speaker_profiles() -> dict[str, Any]:
    """List all speaker profiles.

    Returns:
        Dictionary with speaker profiles list and metadata
    """
    profiles = await make_request("GET", "/api/speaker-profiles")
    return {
        "request_id": generate_request_id(),
        "count": len(profiles) if isinstance(profiles, list) else 0,
        "speaker_profiles": profiles,
    }


@mcp.tool()
async def get_speaker_profile(profile_id: str) -> dict[str, Any]:
    """Get a specific speaker profile by ID.

    Args:
        profile_id: Speaker profile ID (e.g., 'speaker_profile:abc123')

    Returns:
        Speaker profile details
    """
    profile = await make_request("GET", f"/api/speaker-profiles/{profile_id}")
    return {
        "request_id": generate_request_id(),
        "speaker_profile": profile,
    }


@mcp.tool()
async def create_speaker_profile(
    name: str,
    description: Optional[str] = None,
    voice_model: str = "",
    speakers: Optional[list[dict[str, str]]] = None,
    tts_provider: Optional[str] = None,
    tts_model: Optional[str] = None,
) -> dict[str, Any]:
    """Create a new speaker profile.

    Args:
        name: Speaker profile name (e.g., 'Expert Interview')
        description: Optional description
        voice_model: Voice model ID
        speakers: List of speaker definitions with name, backstory, personality
        tts_provider: TTS provider name (e.g., 'openai')
        tts_model: TTS model name (e.g., 'gpt-4o-mini-tts')

    Returns:
        Created speaker profile details
    """
    data: dict[str, Any] = {
        "name": name,
        "voice_model": voice_model,
        "speakers": speakers or [],
    }
    if description is not None:
        data["description"] = description
    if tts_provider is not None:
        data["tts_provider"] = tts_provider
    if tts_model is not None:
        data["tts_model"] = tts_model

    profile = await make_request("POST", "/api/speaker-profiles", json_data=data)
    return {
        "request_id": generate_request_id(),
        "speaker_profile": profile,
    }


@mcp.tool()
async def update_speaker_profile(
    profile_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    voice_model: Optional[str] = None,
    speakers: Optional[list[dict[str, str]]] = None,
    tts_provider: Optional[str] = None,
    tts_model: Optional[str] = None,
) -> dict[str, Any]:
    """Update an existing speaker profile.

    Args:
        profile_id: Speaker profile ID
        name: Optional new name
        description: Optional new description
        voice_model: Optional new voice model ID
        speakers: Optional new speakers list
        tts_provider: Optional new TTS provider
        tts_model: Optional new TTS model

    Returns:
        Updated speaker profile details
    """
    data: dict[str, Any] = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if voice_model is not None:
        data["voice_model"] = voice_model
    if speakers is not None:
        data["speakers"] = speakers
    if tts_provider is not None:
        data["tts_provider"] = tts_provider
    if tts_model is not None:
        data["tts_model"] = tts_model

    profile = await make_request(
        "PUT", f"/api/speaker-profiles/{profile_id}", json_data=data
    )
    return {
        "request_id": generate_request_id(),
        "speaker_profile": profile,
    }


@mcp.tool()
async def delete_speaker_profile(profile_id: str) -> dict[str, Any]:
    """Delete a speaker profile.

    Args:
        profile_id: Speaker profile ID

    Returns:
        Success message
    """
    result = await make_request("DELETE", f"/api/speaker-profiles/{profile_id}")
    return {
        "request_id": generate_request_id(),
        "result": result,
    }


# ── Episode Profile CRUD ──────────────────────────────────────────────


@mcp.tool()
async def list_episode_profiles() -> dict[str, Any]:
    """List all episode profiles.

    Returns:
        Dictionary with episode profiles list and metadata
    """
    profiles = await make_request("GET", "/api/episode-profiles")
    return {
        "request_id": generate_request_id(),
        "count": len(profiles) if isinstance(profiles, list) else 0,
        "episode_profiles": profiles,
    }


@mcp.tool()
async def get_episode_profile(profile_id: str) -> dict[str, Any]:
    """Get a specific episode profile by ID.

    Args:
        profile_id: Episode profile ID (e.g., 'episode_profile:abc123')

    Returns:
        Episode profile details
    """
    profile = await make_request("GET", f"/api/episode-profiles/{profile_id}")
    return {
        "request_id": generate_request_id(),
        "episode_profile": profile,
    }


@mcp.tool()
async def create_episode_profile(
    name: str,
    description: Optional[str] = None,
    speaker_config: Optional[str] = None,
    outline_llm: Optional[str] = None,
    transcript_llm: Optional[str] = None,
    language: Optional[str] = None,
    default_briefing: Optional[str] = None,
    num_segments: Optional[int] = None,
    max_tokens: Optional[int] = None,
    outline_provider: Optional[str] = None,
    outline_model: Optional[str] = None,
    transcript_provider: Optional[str] = None,
    transcript_model: Optional[str] = None,
) -> dict[str, Any]:
    """Create a new episode profile.

    Args:
        name: Episode profile name (e.g., 'Academic Presentation')
        description: Optional description
        speaker_config: Optional speaker configuration dict
        outline_llm: Optional outline system prompt
        transcript_llm: Optional transcript system prompt
        language: Language code (e.g., 'ja', 'en')
        default_briefing: Optional default briefing text
        num_segments: Number of segments (default 3)
        max_tokens: Max tokens per segment (default 4000)
        outline_provider: Optional outline LLM provider
        outline_model: Optional outline LLM model
        transcript_provider: Optional transcript LLM provider
        transcript_model: Optional transcript LLM model

    Returns:
        Created episode profile details
    """
    data: dict[str, Any] = {"name": name}
    if description is not None:
        data["description"] = description
    if speaker_config is not None:
        data["speaker_config"] = speaker_config
    if outline_llm is not None:
        data["outline_llm"] = outline_llm
    if transcript_llm is not None:
        data["transcript_llm"] = transcript_llm
    if language is not None:
        data["language"] = language
    if default_briefing is not None:
        data["default_briefing"] = default_briefing
    if num_segments is not None:
        data["num_segments"] = num_segments
    if max_tokens is not None:
        data["max_tokens"] = max_tokens
    if outline_provider is not None:
        data["outline_provider"] = outline_provider
    if outline_model is not None:
        data["outline_model"] = outline_model
    if transcript_provider is not None:
        data["transcript_provider"] = transcript_provider
    if transcript_model is not None:
        data["transcript_model"] = transcript_model

    profile = await make_request("POST", "/api/episode-profiles", json_data=data)
    return {
        "request_id": generate_request_id(),
        "episode_profile": profile,
    }


@mcp.tool()
async def update_episode_profile(
    profile_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    speaker_config: Optional[str] = None,
    outline_llm: Optional[str] = None,
    transcript_llm: Optional[str] = None,
    language: Optional[str] = None,
    default_briefing: Optional[str] = None,
    num_segments: Optional[int] = None,
    max_tokens: Optional[int] = None,
    outline_provider: Optional[str] = None,
    outline_model: Optional[str] = None,
    transcript_provider: Optional[str] = None,
    transcript_model: Optional[str] = None,
) -> dict[str, Any]:
    """Update an existing episode profile.

    Args:
        profile_id: Episode profile ID
        name: Optional new name
        description: Optional new description
        speaker_config: Optional new speaker configuration
        outline_llm: Optional new outline system prompt
        transcript_llm: Optional new transcript system prompt
        language: Optional new language code
        default_briefing: Optional new default briefing
        num_segments: Optional new segment count
        max_tokens: Optional new max tokens
        outline_provider: Optional new outline LLM provider
        outline_model: Optional new outline LLM model
        transcript_provider: Optional new transcript LLM provider
        transcript_model: Optional new transcript LLM model

    Returns:
        Updated episode profile details
    """
    data: dict[str, Any] = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if speaker_config is not None:
        data["speaker_config"] = speaker_config
    if outline_llm is not None:
        data["outline_llm"] = outline_llm
    if transcript_llm is not None:
        data["transcript_llm"] = transcript_llm
    if language is not None:
        data["language"] = language
    if default_briefing is not None:
        data["default_briefing"] = default_briefing
    if num_segments is not None:
        data["num_segments"] = num_segments
    if max_tokens is not None:
        data["max_tokens"] = max_tokens
    if outline_provider is not None:
        data["outline_provider"] = outline_provider
    if outline_model is not None:
        data["outline_model"] = outline_model
    if transcript_provider is not None:
        data["transcript_provider"] = transcript_provider
    if transcript_model is not None:
        data["transcript_model"] = transcript_model

    profile = await make_request(
        "PUT", f"/api/episode-profiles/{profile_id}", json_data=data
    )
    return {
        "request_id": generate_request_id(),
        "episode_profile": profile,
    }


@mcp.tool()
async def delete_episode_profile(profile_id: str) -> dict[str, Any]:
    """Delete an episode profile.

    Args:
        profile_id: Episode profile ID

    Returns:
        Success message
    """
    result = await make_request("DELETE", f"/api/episode-profiles/{profile_id}")
    return {
        "request_id": generate_request_id(),
        "result": result,
    }


# ── Podcast Generation (existing) ─────────────────────────────────────


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
