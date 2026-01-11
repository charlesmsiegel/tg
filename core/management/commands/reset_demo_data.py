"""
Management command to reset database to demo/test state.

WARNING: This command will delete existing data. Use with caution!
"""

from django.core.management.base import BaseCommand
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

    def handle(self, *args, **options):
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
            self.load_demo_data()

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

    def load_demo_data(self):
        """Load demo data."""

        from django.contrib.auth.models import User

        from game.models import Chronicle

        self.stdout.write("Loading demo data...")

        # Create demo users
        if not User.objects.filter(username="demo_st").exists():
            demo_st = User.objects.create_user(
                username="demo_st", email="demo_st@example.com", password="demo123"
            )
            self.stdout.write("  ✓ Created demo ST user (username: demo_st, password: demo123)")

        if not User.objects.filter(username="demo_player").exists():
            demo_player = User.objects.create_user(
                username="demo_player",
                email="demo_player@example.com",
                password="demo123",
            )
            self.stdout.write(
                "  ✓ Created demo player user (username: demo_player, password: demo123)"
            )

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
        self.stdout.write("\nDemo accounts created:")
        self.stdout.write("  ST: demo_st / demo123")
        self.stdout.write("  Player: demo_player / demo123")
