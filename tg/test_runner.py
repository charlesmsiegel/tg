"""Test database setup for local apps without migration files."""

from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.test.runner import DiscoverRunner


class LocalMigrationTestRunner(DiscoverRunner):
    """Synchronize local apps until they have real migrations."""

    def setup_databases(self, **kwargs):
        migration_modules = dict(getattr(settings, "MIGRATION_MODULES", {}))
        root = Path(settings.BASE_DIR).resolve()

        for app in apps.get_app_configs():
            app_path = Path(app.path).resolve()
            if not app_path.is_relative_to(root):
                continue
            migration_dir = app_path / "migrations"
            if migration_dir.is_dir() and not any(
                path.name != "__init__.py" for path in migration_dir.glob("*.py")
            ):
                migration_modules[app.label] = None

        settings.MIGRATION_MODULES = migration_modules
        return super().setup_databases(**kwargs)
