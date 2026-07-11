from __future__ import annotations
from typing import Any, Optional

from ..mcp_app import mcp
from ..config import generate_request_id
from ..client import make_request
from ..capabilities import Capability

CAPABILITIES = (
    Capability(
        name="search",
        summary="Search content using vector or text search.",
        tags=("search", "query", "vector"),
        args={
            "query": "str",
            "type": "str",
            "notebook_id": "Optional[str]",
            "limit": "int",
        },
        returns="dict[str, Any]",
        example={"query": "AI research", "type": "vector", "limit": 10},
        typical_bytes=3000,
    ),
    Capability(
        name="ask_question",
        summary="Ask a question about your content with detailed control.",
        tags=("search", "ask", "ai", "question"),
        args={
            "question": "str",
            "strategy_model": "str",
            "answer_model": "str",
            "final_answer_model": "str",
        },
        returns="dict[str, Any]",
        example={
            "question": "What are the main AI applications?",
            "strategy_model": "model:abc",
            "answer_model": "model:abc",
            "final_answer_model": "model:abc",
        },
        typical_bytes=5000,
    ),
    Capability(
        name="ask_simple",
        summary="Ask a question about your content with simplified interface.",
        tags=("search", "ask", "ai", "question", "simple"),
        args={
            "question": "str",
            "strategy_model": "str",
            "answer_model": "str",
            "final_answer_model": "str",
        },
        returns="dict[str, Any]",
        example={
            "question": "Summarize my AI research",
            "strategy_model": "model:abc",
            "answer_model": "model:abc",
            "final_answer_model": "model:abc",
        },
        typical_bytes=4000,
    ),
)


@mcp.tool()
async def search(
    query: str,
    type: str = "vector",
    notebook_id: Optional[str] = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Search content using vector or text search.

    Args:
        query: Search query
        type: Search type ('vector' or 'text')
        notebook_id: Optional notebook ID to limit search
        limit: Maximum number of results (1-50)

    Returns:
        Search results
    """
    limit = max(1, min(limit, 50))
    data = {
        "query": query,
        "type": type,
        "limit": limit,
    }
    if notebook_id is not None:
        data["notebook_id"] = notebook_id

    results = await make_request("POST", "/api/search", json_data=data)
    return {
        "request_id": generate_request_id(),
        "results": results,
    }


@mcp.tool()
async def ask_question(
    question: str,
    strategy_model: str,
    answer_model: str,
    final_answer_model: str,
    notebook_id: Optional[str] = None,
) -> dict[str, Any]:
    """Ask a question about your content with detailed control.

    Args:
        question: Question to ask
        strategy_model: Model ID for strategy generation
        answer_model: Model ID for answering
        final_answer_model: Model ID for final answer synthesis
        notebook_id: Optional notebook ID to limit context

    Returns:
        Answer with sources and reasoning
    """
    data = {
        "question": question,
        "strategy_model": strategy_model,
        "answer_model": answer_model,
        "final_answer_model": final_answer_model,
    }
    if notebook_id is not None:
        data["notebook_id"] = notebook_id

    result = await make_request("POST", "/api/search/ask", json_data=data)
    return {
        "request_id": generate_request_id(),
        "result": result,
    }


@mcp.tool()
async def ask_simple(
    question: str,
    strategy_model: str,
    answer_model: str,
    final_answer_model: str,
    notebook_id: Optional[str] = None,
) -> dict[str, Any]:
    """Ask a question about your content with simplified interface.

    Args:
        question: Question to ask
        strategy_model: Model ID for strategy generation
        answer_model: Model ID for answering
        final_answer_model: Model ID for final answer synthesis
        notebook_id: Optional notebook ID to limit context

    Returns:
        Simple answer
    """
    data = {
        "question": question,
        "strategy_model": strategy_model,
        "answer_model": answer_model,
        "final_answer_model": final_answer_model,
    }
    if notebook_id is not None:
        data["notebook_id"] = notebook_id

    result = await make_request("POST", "/api/search/ask/simple", json_data=data)
    return {
        "request_id": generate_request_id(),
        "result": result,
    }
