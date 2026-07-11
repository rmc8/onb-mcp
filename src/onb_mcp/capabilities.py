# ruff: noqa: E402
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal

Detail = Literal["name", "summary", "full"]


@dataclass(frozen=True)
class Capability:
    name: str  # tool name
    summary: str  # one-liner
    tags: tuple[str, ...]  # searchable tags
    args: dict[str, str]  # param -> type (stringified)
    returns: str  # return type (stringified)
    example: dict[str, Any]  # example call args
    typical_bytes: int  # typical response size (rough)


# Import all capability sub-tuples from domain modules
from .tools.meta import CAPABILITIES_META as meta_caps
from .tools.notebooks import CAPABILITIES as notebooks_caps
from .tools.sources import CAPABILITIES as sources_caps
from .tools.notes import CAPABILITIES as notes_caps
from .tools.search import CAPABILITIES as search_caps
from .tools.models import CAPABILITIES as models_caps
from .tools.chat import CAPABILITIES as chat_caps
from .tools.settings import CAPABILITIES as settings_caps
from .tools.transformations import CAPABILITIES as transformations_caps
from .tools.podcasts import CAPABILITIES as podcasts_caps
from .tools.credentials import CAPABILITIES as credentials_caps
from .tools.rebuild import CAPABILITIES as rebuild_caps

# Aggregate all capabilities into a single source of truth tuple
CAPABILITIES: tuple[Capability, ...] = (
    *meta_caps,
    *notebooks_caps,
    *sources_caps,
    *notes_caps,
    *search_caps,
    *models_caps,
    *chat_caps,
    *settings_caps,
    *transformations_caps,
    *podcasts_caps,
    *credentials_caps,
    *rebuild_caps,
)
