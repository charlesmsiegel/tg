"""
Django base settings for tg project.

This file contains settings common to all environments.
Environment-specific settings are in development.py and production.py.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition

INSTALLED_APPS = [
    "daphne",  # Must be before django.contrib.staticfiles for ASGI
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "accounts",
    "characters",
    "game",
    "items",
    "locations",
    "polymorphic",
    "core",
    "widgets",  # Reusable form widgets (replaces chained_select)
    "chained_select",  # Deprecated - backward compatibility only
    "django.contrib.humanize",
    "crispy_forms",
    "crispy_bootstrap4",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.UserListMiddleware",
    "core.middleware.auth_error_handler.AuthErrorHandlerMiddleware",
]

ROOT_URLCONF = "tg.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.all_chronicles",
                "core.context_processors.add_special_user_flag",
                "accounts.context_processors.theme_context",
                "accounts.context_processors.notification_count",
            ],
        },
    },
]

WSGI_APPLICATION = "tg.wsgi.application"
ASGI_APPLICATION = "tg.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {"NAME": BASE_DIR / "db_test.sqlite3"},
        "ATOMIC_REQUESTS": True,  # Wrap each request in a transaction
    }
}

# Upload Size Limits
# ==================
# Limit upload sizes to prevent denial-of-service attacks
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "collected_static"
STATICFILES_DIRS = [BASE_DIR / "source_static"]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "user"
LOGOUT_REDIRECT_URL = "home"

# Email Configuration
# ====================
# Production email settings (configure via environment variables)
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "25"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "False") == "True"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "30"))

# Default sender for password resets and other system emails
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@tellurian-games.com")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

# Password reset token expiration (in seconds, default 1 hour = 3600)
# Reduced from 3 days for improved security - password reset links should be used promptly
PASSWORD_RESET_TIMEOUT = int(os.environ.get("PASSWORD_RESET_TIMEOUT", "3600"))

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TINYMCE_DEFAULT_CONFIG = {
    "height": 400,
    "width": 1000,
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    "selector": "textarea",
    "browser_spellcheck": "true",
    "theme": "modern",
    "plugins": """
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            """,
    "toolbar1": """
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample
            """,
    "toolbar2": """
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            """,
    "contextmenu": "formats | link image",
    "menubar": True,
    "statusbar": True,
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Gameline Configuration
# ====================
# Centralized configuration for all World of Darkness gamelines
# This replaces hardcoded gameline strings throughout the codebase
GAMELINES = {
    "wod": {
        "name": "World of Darkness",
        "short": "",
        "app_name": "wod",
    },
    "vtm": {
        "name": "Vampire: the Masquerade",
        "short": "VtM",
        "app_name": "vampire",
    },
    "wta": {
        "name": "Werewolf: the Apocalypse",
        "short": "WtA",
        "app_name": "werewolf",
    },
    "mta": {
        "name": "Mage: the Ascension",
        "short": "MtA",
        "app_name": "mage",
    },
    "wto": {
        "name": "Wraith: the Oblivion",
        "short": "WtO",
        "app_name": "wraith",
    },
    "ctd": {
        "name": "Changeling: the Dreaming",
        "short": "CtD",
        "app_name": "changeling",
    },
    "dtf": {
        "name": "Demon: the Fallen",
        "short": "DtF",
        "app_name": "demon",
    },
    "mtr": {
        "name": "Mummy: the Resurrection",
        "short": "MtR",
        "app_name": "mummy",
    },
    "htr": {
        "name": "Hunter: the Reckoning",
        "short": "HtR",
        "app_name": "hunter",
    },
    "orp": {
        "name": "Orpheus",
        "short": "Orp",
        "app_name": "orpheus",
    },
}

# Helper to get gameline choices for model fields
GAMELINE_CHOICES = [(key, val["name"]) for key, val in GAMELINES.items()]

# Logging Configuration
# ======================
# Comprehensive logging setup with per-app loggers and multiple handlers
# Environment-specific overrides are in development.py and production.py

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {module}.{funcName}:{lineno} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[{levelname}] {name} - {message}",
            "style": "{",
        },
        "detailed": {
            "format": "[{levelname}] {asctime} [{process:d}:{thread:d}] {name} {pathname}:{lineno} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        # Console handler for all output (INFO and above)
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        # Debug console handler (only in DEBUG mode)
        "console_debug": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["require_debug_true"],
        },
        # General file handler for all logs
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "debug.log",
            "formatter": "verbose",
        },
        # Error file handler for ERROR and above
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "error.log",
            "formatter": "detailed",
        },
        # Warning file handler for WARNING and above
        "warning_file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "warning.log",
            "formatter": "verbose",
        },
        # Null handler to suppress logs when needed
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        # Django core logger
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        # Django request logger (useful for debugging request/response issues)
        "django.request": {
            "handlers": ["error_file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        # Django database logger (can be noisy, set to INFO to see queries)
        "django.db.backends": {
            "handlers": ["null"],
            "level": "INFO",
            "propagate": False,
        },
        # Django security logger
        "django.security": {
            "handlers": ["error_file", "console"],
            "level": "WARNING",
            "propagate": False,
        },
        # Django template logger
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        # Root project logger
        "tg": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Per-app loggers
        "accounts": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "characters": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "game": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "items": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "locations": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "core": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

CRISPY_TEMPLATE_PACK = "bootstrap4"

# Channel Layers Configuration
# ============================
# Default to InMemoryChannelLayer for development
# Production should override this to use Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}
