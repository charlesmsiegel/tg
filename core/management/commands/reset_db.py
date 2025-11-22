"""
Management command to delete the database and all migration files.

This is useful for completely resetting the database during development.
CAUTION: This will delete all data!
"""
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Delete db.sqlite3 and all migration files (CAUTION: Deletes all data!)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip confirmation prompt",
        )

    def handle(self, *args, **options):
        # Safety check - only allow in development
        if not settings.DEBUG:
            raise CommandError(
                "This command can only be run with DEBUG=True (development mode)"
            )

        # Confirmation prompt
        if not options["yes"]:
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️  WARNING: This will DELETE ALL DATA and migration files!\n"
                )
            )
            self.stdout.write("This action will:")
            self.stdout.write("  1. Delete db.sqlite3")
            self.stdout.write("  2. Delete all migration files from all apps")
            self.stdout.write(
                "     (keeping only __init__.py and __pycache__/ in migrations/)\n"
            )

            response = input("Are you sure you want to continue? [y/N]: ")
            if response.lower() not in ["y", "yes"]:
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

        deleted_count = 0

        # Delete database file
        db_path = Path("db.sqlite3")
        if db_path.exists():
            db_path.unlink()
            self.stdout.write(self.style.SUCCESS(f"✓ Deleted {db_path}"))
            deleted_count += 1
        else:
            self.stdout.write(self.style.WARNING(f"  {db_path} not found (skipped)"))

        # Find all Django apps with migrations
        apps_with_migrations = []
        for app_path in Path(".").iterdir():
            if app_path.is_dir():
                migrations_dir = app_path / "migrations"
                if migrations_dir.exists() and migrations_dir.is_dir():
                    apps_with_migrations.append((app_path.name, migrations_dir))

        if not apps_with_migrations:
            self.stdout.write(
                self.style.WARNING("  No migration directories found (skipped)")
            )
        else:
            self.stdout.write(
                f"\n✓ Found {len(apps_with_migrations)} app(s) with migrations:"
            )

            # Delete migration files
            migration_files_deleted = 0
            for app_name, migrations_dir in apps_with_migrations:
                app_deleted = 0
                for file in migrations_dir.glob("*.py"):
                    # Keep __init__.py
                    if file.name == "__init__.py":
                        continue

                    file.unlink()
                    app_deleted += 1
                    migration_files_deleted += 1

                if app_deleted > 0:
                    self.stdout.write(
                        f"  ✓ {app_name}: Deleted {app_deleted} migration file(s)"
                    )
                else:
                    self.stdout.write(f"  - {app_name}: No migration files to delete")

            deleted_count += migration_files_deleted

        # Summary
        self.stdout.write("\n" + "=" * 60)
        if deleted_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"✓ Successfully deleted {deleted_count} item(s)")
            )
            self.stdout.write("\nNext steps:")
            self.stdout.write("  1. Run: python manage.py makemigrations")
            self.stdout.write("  2. Run: python manage.py migrate")
            self.stdout.write("  3. Run: python manage.py populate_gamedata")
        else:
            self.stdout.write(self.style.WARNING("No items were deleted"))
        self.stdout.write("=" * 60 + "\n")
