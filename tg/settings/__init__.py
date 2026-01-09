"""
Django settings module for tg project.

This module dynamically loads the appropriate settings based on the
DJANGO_ENVIRONMENT environment variable.

Environment options:
    - tg.settings.development - Development settings with DEBUG=True
    - tg.settings.production - Production settings with all security features enabled

IMPORTANT: DJANGO_ENVIRONMENT must be explicitly set to either 'development' or
'production'. Unknown values will raise an error to prevent accidental
misconfiguration.
"""

import os

# Determine which settings to use based on environment
# Fail securely: require explicit environment configuration
environment = os.environ.get("DJANGO_ENVIRONMENT", "").lower()

if environment == "production":
    from .production import *  # noqa: F403, F401
elif environment == "development":
    from .development import *  # noqa: F403, F401
elif environment == "":
    # No environment specified - fail with helpful message
    raise ValueError(
        "DJANGO_ENVIRONMENT must be set to 'development' or 'production'. "
        "Set this environment variable before running Django."
    )
else:
    # Unknown environment value - fail securely
    raise ValueError(
        f"Unknown DJANGO_ENVIRONMENT value: '{environment}'. "
        "Must be 'development' or 'production'."
    )
