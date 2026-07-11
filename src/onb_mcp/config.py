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
