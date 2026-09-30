"""
Django settings module for tg project.

This module dynamically loads the appropriate settings based on the
DJANGO_ENVIRONMENT environment variable.

Environment options:
    - tg.settings.development - Development settings with DEBUG=True (default)
    - tg.settings.production - Production settings with all security features enabled

If DJANGO_ENVIRONMENT is not set, defaults to 'development'.
Unknown values will raise an error to prevent accidental misconfiguration.

The repository's .env file is loaded first, so DJANGO_ENVIRONMENT (like every other
variable) may be set there; a variable already in the process environment wins.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# Determine which settings to use based on environment
# Default to development for convenience
environment = os.environ.get("DJANGO_ENVIRONMENT", "development").lower()

if environment == "production":
    from .production import *  # noqa: F403, F401
elif environment == "development":
    from .development import *  # noqa: F403, F401
else:
    # Unknown environment value - fail securely
    raise ValueError(
        f"Unknown DJANGO_ENVIRONMENT value: '{environment}'. "
        "Must be 'development' or 'production'."
    )
