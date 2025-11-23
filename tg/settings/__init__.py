"""
Django settings module for tg project.

This module dynamically loads the appropriate settings based on the
DJANGO_SETTINGS_MODULE environment variable.

Environment options:
    - tg.settings.development (default) - Development settings with DEBUG=True
    - tg.settings.production - Production settings with all security features enabled

If DJANGO_SETTINGS_MODULE is not set, development settings are used by default.
"""

import os

# Determine which settings to use based on environment
# Default to development if not specified
environment = os.environ.get("DJANGO_ENVIRONMENT", "development").lower()

if environment == "production":
    from .production import *  # noqa: F403, F401
elif environment == "development":
    from .development import *  # noqa: F403, F401
else:
    # Fallback to development settings
    from .development import *  # noqa: F403, F401
