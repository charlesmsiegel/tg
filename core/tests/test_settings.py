"""Tests for Django settings configuration."""

import importlib
import os
import sys
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase, TestCase

import tg

SETTINGS_MODULES = (
    "tg.settings",
    "tg.settings.base",
    "tg.settings.development",
    "tg.settings.production",
)

PRODUCTION_ENV = {
    "DJANGO_ENVIRONMENT": "production",
    "SECRET_KEY": "test-secret-key-" + "x" * 40,
    "DJANGO_ALLOWED_HOSTS": "example.com",
}


def load_settings(env, dotenv=None):
    """Import ``tg.settings`` afresh under ``env`` and return the new module.

    ``env`` patches the process environment; a ``None`` value removes the
    variable. ``dotenv`` stands in for the ``.env`` file (so a developer's own
    file cannot change the result) and is recorded in ``load_settings.dotenv_paths``.
    The live settings modules are put back afterwards, so nothing leaks into the
    running test process.
    """
    saved = {name: sys.modules.pop(name) for name in SETTINGS_MODULES if name in sys.modules}
    saved_package = getattr(tg, "settings", None)
    load_settings.dotenv_paths = []

    def fake_load_dotenv(dotenv_path=None, **kwargs):
        load_settings.dotenv_paths.append(dotenv_path)
        for key, value in (dotenv or {}).items():
            os.environ.setdefault(key, value)
        return bool(dotenv)

    try:
        with patch.dict(os.environ), patch("dotenv.load_dotenv", fake_load_dotenv):
            for key, value in env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
            return importlib.import_module("tg.settings")
    finally:
        for name in SETTINGS_MODULES:
            sys.modules.pop(name, None)
        sys.modules.update(saved)
        tg.settings = saved_package


class SettingsSecurityTest(TestCase):
    """Tests for security-related settings."""

    def test_atomic_requests_enabled(self):
        """Test that ATOMIC_REQUESTS is enabled for database transactions."""
        self.assertTrue(
            settings.DATABASES["default"].get("ATOMIC_REQUESTS", False),
            "ATOMIC_REQUESTS should be enabled to wrap each request in a transaction",
        )

    def test_upload_size_limits_set(self):
        """Test that upload size limits are configured."""
        # DATA_UPLOAD_MAX_MEMORY_SIZE should be 5MB
        self.assertEqual(
            settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
            5 * 1024 * 1024,
            "DATA_UPLOAD_MAX_MEMORY_SIZE should be 5 MB",
        )
        # FILE_UPLOAD_MAX_MEMORY_SIZE should be 5MB
        self.assertEqual(
            settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
            5 * 1024 * 1024,
            "FILE_UPLOAD_MAX_MEMORY_SIZE should be 5 MB",
        )

    def test_password_reset_timeout_is_one_hour(self):
        """Password reset tokens expire in 1 hour unless the environment says otherwise."""
        module = load_settings({"PASSWORD_RESET_TIMEOUT": None})
        self.assertEqual(module.PASSWORD_RESET_TIMEOUT, 3600)

    def test_no_deprecated_xss_filter_setting(self):
        """Test that deprecated SECURE_BROWSER_XSS_FILTER is not set."""
        # This setting was deprecated in Django 4.0
        self.assertFalse(
            hasattr(settings, "SECURE_BROWSER_XSS_FILTER") and settings.SECURE_BROWSER_XSS_FILTER,
            "SECURE_BROWSER_XSS_FILTER should not be enabled (deprecated in Django 4.0)",
        )


class SettingsEnvironmentTest(SimpleTestCase):
    """DJANGO_ENVIRONMENT chooses the settings module, from the environment or .env."""

    def test_unset_environment_loads_development(self):
        module = load_settings({"DJANGO_ENVIRONMENT": None})
        self.assertTrue(module.DEBUG)

    def test_environment_is_case_insensitive(self):
        module = load_settings({**PRODUCTION_ENV, "DJANGO_ENVIRONMENT": "Production"})
        self.assertFalse(module.DEBUG)

    def test_empty_environment_raises(self):
        with self.assertRaisesRegex(ValueError, "Unknown DJANGO_ENVIRONMENT"):
            load_settings({"DJANGO_ENVIRONMENT": ""})

    def test_unknown_environment_raises(self):
        with self.assertRaisesRegex(ValueError, "Unknown DJANGO_ENVIRONMENT value: 'staging'"):
            load_settings({"DJANGO_ENVIRONMENT": "staging"})

    def test_environment_set_only_in_dotenv_is_honoured(self):
        """A DJANGO_ENVIRONMENT line in .env selects production (it used to be ignored)."""
        module = load_settings(
            dict.fromkeys(PRODUCTION_ENV),
            dotenv=PRODUCTION_ENV,
        )
        self.assertFalse(module.DEBUG)
        self.assertEqual(module.SECRET_KEY, PRODUCTION_ENV["SECRET_KEY"])

    def test_process_environment_wins_over_dotenv(self):
        module = load_settings({"DJANGO_ENVIRONMENT": "development"}, dotenv=PRODUCTION_ENV)
        self.assertTrue(module.DEBUG)

    def test_dotenv_is_read_from_the_repository_root(self):
        load_settings({"DJANGO_ENVIRONMENT": None})
        self.assertEqual(load_settings.dotenv_paths, [Path(settings.BASE_DIR) / ".env"])


class ProductionSettingsTest(SimpleTestCase):
    """Tests for production-specific settings."""

    def test_conn_max_age_set_in_production(self):
        """Production keeps database connections for 600 seconds by default."""
        module = load_settings({**PRODUCTION_ENV, "DB_CONN_MAX_AGE": None})
        self.assertEqual(module.DATABASES["default"]["CONN_MAX_AGE"], 600)

    def test_conn_max_age_from_environment(self):
        module = load_settings({**PRODUCTION_ENV, "DB_CONN_MAX_AGE": "30"})
        self.assertEqual(module.DATABASES["default"]["CONN_MAX_AGE"], 30)
