"""Tests for Django settings configuration."""

import importlib
import os
import sys
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.backends.django import DjangoTemplates
from django.template.loaders.cached import Loader as CachedLoader
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

    def test_development_allowed_hosts_are_trimmed(self):
        module = load_settings(
            {"DJANGO_ENVIRONMENT": "development", "DJANGO_ALLOWED_HOSTS": "localhost, tg.test"}
        )
        self.assertEqual(module.ALLOWED_HOSTS, ["localhost", "tg.test"])
        module = load_settings({"DJANGO_ENVIRONMENT": None, "DJANGO_ALLOWED_HOSTS": None})
        self.assertEqual(module.ALLOWED_HOSTS, ["localhost", "127.0.0.1"])

    def test_development_prints_sql_only_when_asked_regression(self):
        """DJANGO_LOG_SQL=True sends SQL (logged at DEBUG) to a DEBUG-level console handler."""
        module = load_settings({"DJANGO_ENVIRONMENT": "development", "DJANGO_LOG_SQL": None})
        self.assertEqual(module.LOGGING["loggers"]["django.db.backends"]["handlers"], ["null"])

        module = load_settings({"DJANGO_ENVIRONMENT": "development", "DJANGO_LOG_SQL": "True"})
        sql_logger = module.LOGGING["loggers"]["django.db.backends"]
        self.assertEqual(sql_logger["level"], "DEBUG")
        for name in sql_logger["handlers"]:
            with self.subTest(handler=name):
                self.assertEqual(module.LOGGING["handlers"][name]["level"], "DEBUG")

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

    def test_missing_secret_key_is_improperly_configured(self):
        for value in (None, ""):
            with self.subTest(SECRET_KEY=value):
                with self.assertRaisesRegex(ImproperlyConfigured, "SECRET_KEY"):
                    load_settings({**PRODUCTION_ENV, "SECRET_KEY": value})

    def test_allowed_hosts_are_trimmed(self):
        module = load_settings(
            {
                **PRODUCTION_ENV,
                "DJANGO_ALLOWED_HOSTS": "example.com, www.example.com ,",
                "CSRF_TRUSTED_ORIGINS": "https://example.com, https://www.example.com",
            }
        )
        self.assertEqual(module.ALLOWED_HOSTS, ["example.com", "www.example.com"])
        self.assertEqual(
            module.CSRF_TRUSTED_ORIGINS, ["https://example.com", "https://www.example.com"]
        )

    def test_missing_allowed_hosts_raises(self):
        for value in (None, "", " , "):
            with self.subTest(DJANGO_ALLOWED_HOSTS=value):
                with self.assertRaisesRegex(ValueError, "DJANGO_ALLOWED_HOSTS"):
                    load_settings({**PRODUCTION_ENV, "DJANGO_ALLOWED_HOSTS": value})

    def test_template_engine_builds_with_cached_loader_regression(self):
        """Production templates load (a "loaders" option beside APP_DIRS raised)."""
        module = load_settings(PRODUCTION_ENV)
        config = module.TEMPLATES[0]
        backend = DjangoTemplates(
            {
                "NAME": "production",
                "DIRS": config["DIRS"],
                "APP_DIRS": config["APP_DIRS"],
                "OPTIONS": {**config["OPTIONS"], "debug": module.DEBUG},
            }
        )
        loader = backend.engine.template_loaders[0]
        self.assertIsInstance(loader, CachedLoader)
        self.assertIn(
            "django.template.loaders.app_directories.Loader",
            [f"{type(inner).__module__}.{type(inner).__name__}" for inner in loader.loaders],
        )
        self.assertTrue(backend.get_template("core/tl_base.html"))

    def test_admin_emails_accept_names_regression(self):
        """``Name <address>`` entries used to crash the import with TypeError."""
        module = load_settings(
            {**PRODUCTION_ENV, "ADMIN_EMAILS": "Jane Doe <jane@example.com>, ops@example.com,"}
        )
        expected = [("Jane Doe", "jane@example.com"), ("Admin", "ops@example.com")]
        self.assertEqual(module.ADMINS, expected)
        self.assertEqual(module.MANAGERS, expected)

    def test_no_admin_emails(self):
        module = load_settings({**PRODUCTION_ENV, "ADMIN_EMAILS": None})
        self.assertEqual(module.ADMINS, [])

    def test_request_errors_are_mailed_to_admins_regression(self):
        """500s reach ADMINS: the project LOGGING had dropped Django's mail_admins handler."""
        module = load_settings(PRODUCTION_ENV)
        handler = module.LOGGING["handlers"]["mail_admins"]
        self.assertEqual(handler["class"], "django.utils.log.AdminEmailHandler")
        self.assertEqual(handler["level"], "ERROR")
        self.assertIn("require_debug_false", handler["filters"])
        for name in ("django", "django.request"):
            with self.subTest(logger=name):
                self.assertIn("mail_admins", module.LOGGING["loggers"][name]["handlers"])

    def test_production_logging_does_not_leak_into_development(self):
        load_settings(PRODUCTION_ENV)
        module = load_settings({"DJANGO_ENVIRONMENT": "development"})
        self.assertNotIn("mail_admins", module.LOGGING["handlers"])
