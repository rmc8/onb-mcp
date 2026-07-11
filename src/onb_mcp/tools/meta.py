from __future__ import annotations

import re
import uuid
from typing import Any

from ..mcp_app import mcp
from ..capabilities import Capability, Detail


def _normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _match_score(q: str, cap: Any) -> int:
    if not q:
        return 0
    qn = _normalize(q)
    hay = " ".join([cap.name, cap.summary, " ".join(cap.tags)])
    hn = _normalize(hay)
    score = 0
    for token in qn.split():
        if token in hn:
            score += 1
    return score


CAPABILITIES_META = (
    Capability(
        name="search_capabilities",
        summary="Search tools exposed by this server with progressive detail levels.",
        tags=("meta", "discovery", "progressive-disclosure"),
        args={
            "query": "str",
            "detail": "Literal['name','summary','full']",
            "limit": "int",
        },
        returns="dict[str, Any]",
        example={"query": "notebook", "detail": "summary", "limit": 10},
        typical_bytes=1200,
    ),
)


@mcp.tool()
def search_capabilities(
    query: str = "", detail: Detail = "summary", limit: int = 20
) -> dict[str, Any]:
    """Search tools exposed by this server with progressive detail levels.

    Args:
        query: Search query to filter tools
        detail: Level of detail - 'name' (minimal), 'summary' (default), or 'full' (complete)
        limit: Maximum number of results (1-50)

    Returns:
        Dictionary with request_id, query, detail, count, matches, and hint fields
    """
    from ..capabilities import CAPABILITIES

    request_id = str(uuid.uuid4())
    limit = max(1, min(int(limit), 50))

    scored = [(c, _match_score(query, c)) for c in CAPABILITIES]
    if query.strip():
        scored = [x for x in scored if x[1] > 0]
        scored.sort(key=lambda t: (-t[1], t[0].name))
    else:
        scored.sort(key=lambda t: t[0].name)

    matches = []
    for cap, _score in scored[:limit]:
        if detail == "name":
            matches.append({"name": cap.name})
        elif detail == "summary":
            matches.append(
                {"name": cap.name, "summary": cap.summary, "tags": list(cap.tags)}
            )
        else:
            matches.append(
                {
                    "name": cap.name,
                    "summary": cap.summary,
                    "tags": list(cap.tags),
                    "args": cap.args,
                    "returns": cap.returns,
                    "example": cap.example,
                    "typical_bytes": cap.typical_bytes,
                }
            )

    return {
        "request_id": request_id,
        "query": query,
        "detail": detail,
        "count": len(matches),
        "matches": matches,
        "hint": "Use detail='name' for minimal context; detail='full' only when implementing a call.",
    }
