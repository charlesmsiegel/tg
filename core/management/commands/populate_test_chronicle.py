"""
Management command to populate a test chronicle with realistic data.

Creates:
- Characters with various statuses
- Scenes
- XP history
- Relationships
"""

from datetime import date, timedelta
from random import choice, randint

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from game.models import Chronicle


class Command(BaseCommand):
    help = "Populate a test chronicle with realistic data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chronicle",
            type=int,
            required=True,
            help="Chronicle ID to populate",
        )
        parser.add_argument(
            "--characters",
            type=int,
            default=10,
            help="Number of characters to create (default: 10)",
        )
        parser.add_argument(
            "--scenes",
            type=int,
            default=15,
            help="Number of scenes to create (default: 15)",
        )
        parser.add_argument(
            "--gameline",
            type=str,
            choices=["vtm", "wta", "mta", "wto", "ctd", "dtf"],
            default="vtm",
            help="Gameline for characters (default: vtm)",
        )

    def handle(self, *args, **options):
        # Get chronicle
        try:
            chronicle = Chronicle.objects.get(pk=options["chronicle"])
        except Chronicle.DoesNotExist:
            raise CommandError(f"Chronicle {options['chronicle']} not found")

        self.stdout.write(self.style.SUCCESS(f"\nPopulating test data for: {chronicle.name}\n"))

        # Create test user if needed
        test_user, created = User.objects.get_or_create(
            username="test_player",
            defaults={
                "email": "test@example.com",
            },
        )
        if created:
            test_user.set_password("test123")
            test_user.save()
            self.stdout.write("  ✓ Created test user (username: test_player, password: test123)")

        # Create characters
        characters = self.create_characters(
            chronicle, test_user, options["characters"], options["gameline"]
        )

        # Create scenes
        scenes = self.create_scenes(chronicle, characters, options["scenes"])

        # Summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("TEST DATA CREATED"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Chronicle: {chronicle.name}")
        self.stdout.write(f"Characters: {len(characters)}")
        self.stdout.write(f"Scenes: {len(scenes)}")
        self.stdout.write("=" * 70 + "\n")

    def create_characters(self, chronicle, user, count, gameline):
        """Create test characters."""
        self.stdout.write(f"\nCreating {count} test characters...")

        characters = []

        # Character name templates
        names = [
            "Marcus",
            "Isabella",
            "Vincent",
            "Elena",
            "Thomas",
            "Sophia",
            "Alexander",
            "Catherine",
            "Dominic",
            "Natalie",
            "Jonathan",
            "Victoria",
            "Sebastian",
            "Anastasia",
            "Gabriel",
        ]

        # Character concepts
        concepts = [
            "Former Detective",
            "Street Artist",
            "Corporate Lawyer",
            "Underground DJ",
            "Medical Student",
            "Philosophy Professor",
            "Club Owner",
            "Investigative Journalist",
            "Gang Member",
            "Social Worker",
            "Antique Dealer",
            "Hacker",
        ]

        statuses = ["App", "App", "App", "Sub", "Un"]  # Weighted towards approved

        for i in range(count):
            name = choice(names) + " " + choice(["Smith", "Jones", "Martinez", "Chen", "O'Brien"])
            concept = choice(concepts)
            status = choice(statuses)

            # Create character using Human model from core
            from characters.models.core.human import Human

            char = Human.objects.create(
                name=name,
                owner=user,
                chronicle=chronicle,
                concept=concept,
                status=status,
                xp=randint(0, 50),
            )

            characters.append(char)

        self.stdout.write(self.style.SUCCESS(f"  ✓ Created {len(characters)} character(s)"))

        return characters

    def create_scenes(self, chronicle, characters, count):
        """Create test scenes."""
        from game.models import Scene
        from locations.models.core.location import LocationModel

        self.stdout.write(f"\nCreating {count} test scenes...")

        # Create a test location
        location, _ = LocationModel.objects.get_or_create(
            name="The Elysium",
            chronicle=chronicle,
            defaults={
                "owner": characters[0].owner if characters else None,
                "status": "App",
                "description": "A neutral gathering place for supernatural beings",
            },
        )

        scenes = []

        scene_names = [
            "First Contact",
            "The Gathering",
            "Investigation Begins",
            "Confrontation",
            "The Reveal",
            "Unexpected Alliance",
            "Dark Secrets",
            "Power Play",
            "The Hunt",
            "Resolution",
        ]

        today = date.today()

        for i in range(count):
            scene_date = today - timedelta(days=count - i)
            finished = i < (count - 3)  # Last 3 scenes are active

            scene = Scene.objects.create(
                name=choice(scene_names) + f" #{i+1}",
                chronicle=chronicle,
                location=location,
                finished=finished,
                date_of_scene=scene_date,
                xp_given=finished,
            )

            # Add random participants
            participant_count = randint(2, min(5, len(characters)))
            participants = [characters[j] for j in range(participant_count)]

            for char in participants:
                scene.characters.add(char)

            scenes.append(scene)

        self.stdout.write(self.style.SUCCESS(f"  ✓ Created {len(scenes)} scene(s)"))

        return scenes
