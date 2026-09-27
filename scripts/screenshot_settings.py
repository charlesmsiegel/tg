"""Settings for scripts/template_screenshots.py: development settings on a throwaway DB.

The database path comes from ``TG_SCREENSHOT_DB``. The debug toolbar is hidden
and SQL logging is silenced so screenshots only show application markup.
"""

import os

from tg.settings.development import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("TG_SCREENSHOT_DB", "/tmp/tg-screenshots.sqlite3"),
        "ATOMIC_REQUESTS": True,
    }
}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: False}
LOGGING["loggers"]["django.db.backends"]["level"] = "WARNING"  # noqa: F405
for _name in ["tg", "accounts", "characters", "game", "items", "locations", "core", "django"]:
    LOGGING["loggers"][_name]["level"] = "WARNING"  # noqa: F405
# Like tg.test_runner: local apps without migration files are created by syncdb.
MIGRATION_MODULES = {
    app: None for app in ("accounts", "characters", "core", "game", "items", "locations", "widgets")
}
