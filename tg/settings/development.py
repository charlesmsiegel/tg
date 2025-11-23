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
except ImportError:
    pass

# Simplified logging for development
LOGGING["loggers"]["django"]["level"] = "INFO"  # noqa: F405
LOGGING["loggers"]["tg"]["level"] = "DEBUG"  # noqa: F405
