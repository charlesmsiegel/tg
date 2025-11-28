"""
Django development settings for tg project.

These settings are suitable for local development only.
DO NOT use these settings in production.
"""

import os

from .base import *  # noqa: F403, F401

# SECURITY WARNING: keep the secret key used in production secret!
# For development, we can use a default key if not provided
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-dev-key-change-this-in-production-8x7@k#f9$m2n!q5w"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]"
).split(",")

# Development-specific email backend (prints to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Additional development settings
# ================================

# Show detailed error pages
DEBUG_PROPAGATE_EXCEPTIONS = False

# Enable Django Debug Toolbar if installed
try:
    import debug_toolbar  # noqa: F401

    INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware"
    ] + MIDDLEWARE  # noqa: F405
    INTERNAL_IPS = ["127.0.0.1", "::1"]

    def show_toolbar_callback(request):
        """Only show debug toolbar to authenticated staff/superusers."""
        if not hasattr(request, "user"):
            return False
        return (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": "tg.settings.development.show_toolbar_callback",
    }
except ImportError:
    pass

# Development logging configuration
# ===================================
# More verbose logging for development with DEBUG level for all apps

# Enable DEBUG level for Django core (useful for development)
LOGGING["loggers"]["django"]["level"] = "INFO"  # noqa: F405
LOGGING["loggers"]["django.db.backends"]["handlers"] = ["console_debug"]  # noqa: F405
LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"  # noqa: F405  # Shows SQL queries

# Set all app loggers to DEBUG in development
LOGGING["loggers"]["tg"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["accounts"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["characters"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["game"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["items"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["locations"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["core"]["level"] = "DEBUG"  # noqa: F405

# Add console_debug handler for verbose output in development
for logger_name in ["tg", "accounts", "characters", "game", "items", "locations", "core"]:
    if "console_debug" not in LOGGING["loggers"][logger_name]["handlers"]:  # noqa: F405
        LOGGING["loggers"][logger_name]["handlers"].append("console_debug")  # noqa: F405

# Cache Configuration for Development
# ====================================
# Use local memory cache for development (no Redis required)
# This provides caching functionality without external dependencies
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "TIMEOUT": 300,  # Default timeout: 5 minutes
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
        },
    }
}
