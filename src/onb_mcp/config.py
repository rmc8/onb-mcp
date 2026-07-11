import os
import uuid
from typing import Optional

# Maximum number of items to return in list operations
MAX_LIMIT = 100

# Default timeout for HTTP requests (seconds)
DEFAULT_TIMEOUT_S = 30.0


def get_base_url() -> str:
    """Get the Open Notebook API base URL from environment."""
    return os.getenv("OPEN_NOTEBOOK_URL", "http://localhost:5055")


def get_auth_token() -> Optional[str]:
    """Get the authentication token from environment."""
    return os.getenv("OPEN_NOTEBOOK_PASSWORD")


def generate_request_id() -> str:
    """Generate a unique request ID for tracking."""
    return str(uuid.uuid4())


def get_cf_access_headers() -> dict[str, str]:
    """Return Cloudflare Access service-token headers if both env vars are set."""
    client_id = os.getenv("CF_ACCESS_CLIENT_ID")
    client_secret = os.getenv("CF_ACCESS_CLIENT_SECRET")
    if client_id and client_secret:
        return {
            "CF-Access-Client-Id": client_id,
            "CF-Access-Client-Secret": client_secret,
        }
    return {}
