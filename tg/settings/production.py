"""
Django production settings for tg project.

These settings include all necessary security configurations for production deployment.
All sensitive values MUST be provided via environment variables.
"""

import os

from .base import *  # noqa: F403, F401

# SECURITY WARNING: SECRET_KEY must be set in environment variables for production
# This will raise an ImproperlyConfigured error if SECRET_KEY is not set
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: DEBUG must be False in production
DEBUG = False

# ALLOWED_HOSTS must be configured via environment variable
# Example: DJANGO_ALLOWED_HOSTS=example.com,www.example.com,api.example.com
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    raise ValueError("DJANGO_ALLOWED_HOSTS must be set in production environment")

# Security Settings
# =================

# HTTPS/SSL Configuration
# Force HTTPS for all requests
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True") == "True"

# Use secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS)
# Tells browsers to only access the site via HTTPS for the specified time period
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "True") == "True"

# Content Security
# Prevent browsers from guessing content types
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable browser XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Prevent site from being framed (clickjacking protection)
X_FRAME_OPTIONS = "DENY"

# Redirect HTTP to HTTPS at proxy level
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF Protection
# ===============

# Require CSRF token for unsafe HTTP methods
CSRF_COOKIE_HTTPONLY = False  # Must be False for AJAX requests to read it
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_NAME = "csrftoken"

# Trusted origins for CSRF (for cross-origin requests)
# Set this to your actual domain(s)
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
if CSRF_TRUSTED_ORIGINS == [""]:
    CSRF_TRUSTED_ORIGINS = []

# Session Security
# ================

# Session cookies
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = int(os.environ.get("SESSION_COOKIE_AGE", "1209600"))  # 2 weeks default

# Close session when browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = os.environ.get("SESSION_EXPIRE_AT_BROWSER_CLOSE", "False") == "True"

# Additional Security Headers
# ===========================

# Referrer Policy - control how much referrer information is sent
SECURE_REFERRER_POLICY = "same-origin"

# Database Configuration for Production
# ======================================
# Override the SQLite database with PostgreSQL or MySQL for production
# Uncomment and configure based on your database choice:

# PostgreSQL example:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("DB_NAME"),
#         "USER": os.environ.get("DB_USER"),
#         "PASSWORD": os.environ.get("DB_PASSWORD"),
#         "HOST": os.environ.get("DB_HOST", "localhost"),
#         "PORT": os.environ.get("DB_PORT", "5432"),
#         "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "600")),
#         "OPTIONS": {
#             "sslmode": os.environ.get("DB_SSLMODE", "require"),
#         },
#     }
# }

# MySQL example:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.environ.get("DB_NAME"),
#         "USER": os.environ.get("DB_USER"),
#         "PASSWORD": os.environ.get("DB_PASSWORD"),
#         "HOST": os.environ.get("DB_HOST", "localhost"),
#         "PORT": os.environ.get("DB_PORT", "3306"),
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
#             "charset": "utf8mb4",
#         },
#     }
# }

# Static and Media Files for Production
# ======================================

# Consider using a CDN or cloud storage for static/media files in production
# For AWS S3 example, install django-storages and boto3, then configure:
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Logging Configuration for Production
# =====================================

# Update logging to use different handlers for production
LOGGING["handlers"]["file"]["level"] = "WARNING"  # noqa: F405
LOGGING["loggers"]["django"]["level"] = "WARNING"  # noqa: F405
LOGGING["loggers"]["tg"]["level"] = "INFO"  # noqa: F405

# Add error logging to file
LOGGING["handlers"]["error_file"] = {  # noqa: F405
    "level": "ERROR",
    "class": "logging.FileHandler",
    "filename": BASE_DIR / "error.log",  # noqa: F405
    "formatter": "verbose",
}

LOGGING["loggers"]["django"]["handlers"].append("error_file")  # noqa: F405
LOGGING["loggers"]["tg"]["handlers"].append("error_file")  # noqa: F405

# Admin Email Notifications
# =========================
# Configure ADMINS to receive error notifications via email
ADMINS = []
admin_emails = os.environ.get("ADMIN_EMAILS", "")
if admin_emails:
    for email in admin_emails.split(","):
        email = email.strip()
        if email:
            # Format: "Name <email@example.com>" or just "email@example.com"
            if "<" in email:
                ADMINS.append(tuple(email.split("<")[0].strip(), email.split("<")[1].rstrip(">")))
            else:
                ADMINS.append(("Admin", email))

MANAGERS = ADMINS

# Cache Configuration
# ===================
# Use Redis or Memcached for production caching
# Redis example (requires django-redis):
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1"),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# Performance Optimizations
# =========================

# Template caching
if not DEBUG:  # noqa: F405
    TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa: F405
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        ),
    ]
