import logging
from typing import Any, Optional
import httpx

from .config import get_base_url, get_auth_token, get_cf_access_headers, DEFAULT_TIMEOUT_S

log = logging.getLogger("onb-mcp")


async def make_request(
    method: str,
    endpoint: str,
    *,
    json_data: Optional[dict[str, Any]] = None,
    params: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Make an HTTP request to the Open Notebook API."""
    base_url = get_base_url()
    url = f"{base_url}{endpoint}"

    headers = {"Content-Type": "application/json"}
    auth_token = get_auth_token()
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    headers.update(get_cf_access_headers())

    async with httpx.AsyncClient(
        follow_redirects=True, timeout=DEFAULT_TIMEOUT_S
    ) as client:
        try:
            if method == "GET":
                r = await client.get(url, headers=headers, params=params)
            elif method == "POST":
                r = await client.post(
                    url, headers=headers, json=json_data, params=params
                )
            elif method == "PUT":
                r = await client.put(
                    url, headers=headers, json=json_data, params=params
                )
            elif method == "DELETE":
                r = await client.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            r.raise_for_status()

            if not r.text:
                return {"message": "Success"}

            try:
                return r.json()
            except (ValueError, Exception) as json_err:
                log.warning(f"Non-JSON response from {endpoint}: {json_err}")
                return {"message": "Success", "content": r.text}

        except httpx.HTTPError as e:
            error_msg = str(e)
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg = error_detail.get("detail", error_msg)
                except (ValueError, AttributeError):
                    error_msg = e.response.text or error_msg

            raise Exception(f"API request failed: {error_msg}")
