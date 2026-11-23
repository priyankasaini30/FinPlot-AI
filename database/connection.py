"""
Database connection and configuration manager for FinPlot AI.
Manages Supabase client lifecycle, environment variable verification,
and local development fallback state reporting.
"""

import os
from typing import Any, Dict, Optional, Tuple
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv()

PLACEHOLDER_MARKERS = [
    "your-project-ref",
    "your-supabase",
    "your-anon-key",
    "placeholder",
    "example",
]


def is_placeholder_or_empty(val: Optional[str]) -> bool:
    """Checks if a configuration value is empty or remains a template placeholder."""
    if not val:
        return True
    val_clean = val.strip().lower()
    return any(marker in val_clean for marker in PLACEHOLDER_MARKERS)


def check_supabase_configuration() -> Tuple[bool, Dict[str, Any]]:
    """
    Validates whether valid Supabase environment variables are present.
    Returns:
        (is_configured, status_metadata)
    """
    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_key = os.getenv("SUPABASE_KEY", "").strip()

    missing = []
    if is_placeholder_or_empty(supabase_url):
        missing.append("SUPABASE_URL")
    if is_placeholder_or_empty(supabase_key):
        missing.append("SUPABASE_KEY")

    if missing:
        return False, {
            "mode": "local_sqlite",
            "is_connected": False,
            "url": supabase_url or "Not configured",
            "missing": missing,
            "message": (
                f"Missing or placeholder configuration for: {', '.join(missing)}. "
                "Operating in Local Development Mode (SQLite persistence) without fabricating cloud sync."
            ),
        }

    return True, {
        "mode": "supabase",
        "is_connected": True,
        "url": supabase_url,
        "missing": [],
        "message": f"Connected to Supabase Cloud endpoint ({supabase_url})",
    }


def get_supabase_client() -> Tuple[Optional[Any], Dict[str, Any]]:
    """
    Initializes and returns a Supabase client if configured.
    Falls back gracefully if credentials are not configured or client library fails.
    """
    is_configured, status = check_supabase_configuration()
    if not is_configured:
        return None, status

    try:
        from supabase import create_client, Client  # type: ignore

        url = os.environ["SUPABASE_URL"].strip()
        key = os.environ["SUPABASE_KEY"].strip()

        client: Client = create_client(url, key)
        return client, status

    except Exception as exc:
        status["is_connected"] = False
        status["message"] = f"Supabase initialization error: {str(exc)}"
        status["mode"] = "local_sqlite"
        return None, status
