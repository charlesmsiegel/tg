"""
Management command to reset database to demo/test state.

WARNING: This command will delete existing data. It refuses to run unless
settings.DEBUG is true or --force is given.
"""

import secrets

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Reset database to demo/test state (WARNING: Deletes existing data!)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--preserve-users",
            action="store_true",
            help="Preserve existing user accounts",
        )
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Confirm that you want to delete all data",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Run even when DEBUG is false (never on a real installation)",
        )
        parser.add_argument(
            "--password",
            help="Password for the demo accounts (default: a random one, printed once)",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "reset_demo_data deletes all game data and only runs with DEBUG=True "
                "(pass --force to override)"
            )

        if not options["confirm"]:
            self.stdout.write(
                self.style.ERROR("\nWARNING: This command will DELETE ALL GAME DATA!\n")
            )
            self.stdout.write(
                "To proceed, run with --confirm flag:\n"
                "  python manage.py reset_demo_data --confirm\n"
            )
            return

        self.stdout.write(self.style.WARNING("\nResetting database to demo state...\n"))

        with transaction.atomic():
            # Delete game data
            self.delete_game_data()

            # Preserve or delete users
            if not options["preserve_users"]:
                self.delete_users()
            else:
                self.stdout.write("Preserving user accounts...")

            # Load demo data
            self.load_demo_data(options["password"] or secrets.token_urlsafe(12))

        self.stdout.write(self.style.SUCCESS("\n✓ Demo data loaded successfully!"))

    def delete_game_data(self):
        """Delete all game-related data."""
        from characters.models.core.character import CharacterModel
        from game.models import Chronicle, Scene, StoryXPRequest, Week, WeeklyXPRequest
        from items.models.core.item import ItemModel
        from locations.models.core.location import LocationModel

        self.stdout.write("Deleting existing game data...")

        # Delete in order to respect foreign keys
        WeeklyXPRequest.objects.all().delete()
        StoryXPRequest.objects.all().delete()
        Week.objects.all().delete()
        Scene.objects.all().delete()

        CharacterModel.objects.all().delete()
        ItemModel.objects.all().delete()
        LocationModel.objects.all().delete()

        Chronicle.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("  ✓ Game data deleted"))

    def delete_users(self):
        """Delete all users except superusers."""
        from django.contrib.auth.models import User

        self.stdout.write("Deleting non-superuser accounts...")

        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS("  ✓ User accounts deleted"))

    def load_demo_data(self, password):
        """Load demo data; new demo accounts get ``password``."""

        from django.contrib.auth.models import User

        from game.models import Chronicle

        self.stdout.write("Loading demo data...")

        # Create demo users; existing accounts keep their password
        created = []
        for username in ("demo_st", "demo_player"):
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username, email=f"{username}@example.com", password=password
                )
                created.append(username)
                self.stdout.write(f"  ✓ Created demo user {username}")

        # Create demo chronicle
        chronicle = Chronicle.objects.create(
            name="Demo Chronicle: Nights of Seattle",
            theme="Political intrigue and ancient mysteries",
            mood="Dark, suspenseful, with moments of dark humor",
            year=2025,
            headings="vtm_heading",
        )
        chronicle.storytellers.add(User.objects.get(username="demo_st"))
        chronicle.save()

        self.stdout.write(f"  ✓ Created demo chronicle: {chronicle.name} (ID: {chronicle.id})")

        self.stdout.write(self.style.SUCCESS("\n✓ Demo data loaded!"))
        if created:
            self.stdout.write(f"\nPassword for {', '.join(created)}: {password}")
