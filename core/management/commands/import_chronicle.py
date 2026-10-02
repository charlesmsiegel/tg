"""
Management command to import a chronicle from an export_chronicle JSON file.

Imports only the chronicle record (name, theme, mood, year, headings), its
storytellers, its setting elements and, unless --skip-users, missing users (with
unusable passwords). Characters, items, locations, scenes, journals and XP requests
in the file are counted and reported but not imported.
"""

import json
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from game.models import Chronicle, SettingElement

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Import a chronicle record, its storytellers, setting elements and users from an "
        "export_chronicle file. Characters, items, locations, scenes, journals and XP "
        "requests are NOT imported."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "filename",
            type=str,
            help="JSON file to import",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be imported without actually importing",
        )
        parser.add_argument(
            "--skip-users",
            action="store_true",
            help="Skip user import (use existing users)",
        )
        parser.add_argument(
            "--remap-users",
            type=str,
            help="JSON file mapping old usernames to new usernames",
        )

    def handle(self, *args, **options):
        filename = options["filename"]

        # Load import file
        try:
            with open(filename) as f:
                import_data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f"File not found: {filename}") from None
        except json.JSONDecodeError as e:
            raise CommandError(f"Invalid JSON file: {e}") from e

        # Validate import data
        if "chronicle" not in import_data:
            raise CommandError("Invalid import file: missing chronicle data")

        # Load user remapping if provided
        user_map = {}
        if options["remap_users"]:
            with open(options["remap_users"]) as f:
                user_map = json.load(f)

        # Display summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("IMPORT SUMMARY"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Export Date: {import_data.get('export_date', 'Unknown')}")
        self.stdout.write(f"Export Version: {import_data.get('export_version', 'Unknown')}")
        self.stdout.write(f"Characters: {len(import_data.get('characters', []))}")
        self.stdout.write(f"Items: {len(import_data.get('items', []))}")
        self.stdout.write(f"Locations: {len(import_data.get('locations', []))}")
        self.stdout.write(f"Scenes: {len(import_data.get('scenes', []))}")
        self.stdout.write(f"Journals: {len(import_data.get('journals', []))}")
        self.stdout.write("=" * 70 + "\n")

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("[DRY RUN] No data was actually imported"))
            return

        # Perform import in a transaction
        try:
            with transaction.atomic():
                self.import_data(import_data, options, user_map)
        except Exception as e:
            logger.error(f"Chronicle import failed: {e}", exc_info=True)
            raise CommandError(f"Import failed: {e}") from e

        self.stdout.write(self.style.SUCCESS("\n✓ Import complete!\n"))

    def import_data(self, data, options, user_map):
        """Import users, the chronicle and its setting elements."""
        # Import users first if included and not skipped
        if "users" in data and not options["skip_users"]:
            self.import_users(data["users"], user_map)

        # Import chronicle
        chronicle = self.import_chronicle(data["chronicle"], user_map)

        # Import setting elements
        if "setting_elements" in data:
            self.import_setting_elements(data["setting_elements"], chronicle)

        self.report_not_imported(data)

    def import_users(self, users_data, user_map):
        """Import users, applying username remapping if provided."""
        self.stdout.write("Importing users...")

        for user_json in users_data:
            # Apply user remapping
            old_username = user_json["fields"]["username"]
            new_username = user_map.get(old_username, old_username)

            # Check if user already exists
            if User.objects.filter(username=new_username).exists():
                self.stdout.write(
                    self.style.WARNING(f"  User {new_username} already exists, skipping")
                )
                continue

            # Create user with an unusable password: the owner resets it to log in
            User.objects.create_user(
                username=new_username,
                email=user_json["fields"].get("email", ""),
                password=None,
                first_name=user_json["fields"].get("first_name", ""),
                last_name=user_json["fields"].get("last_name", ""),
            )
            self.stdout.write(f"  Created user: {new_username}")

    def import_chronicle(self, chronicle_data, user_map):
        """Import the chronicle."""
        self.stdout.write("Importing chronicle...")

        # Create chronicle
        fields = chronicle_data["fields"]
        chronicle = Chronicle.objects.create(
            name=fields.get("name", "Imported Chronicle"),
            theme=fields.get("theme", ""),
            mood=fields.get("mood", ""),
            year=fields.get("year", 2022),
            headings=fields.get("headings", "wod_heading"),
        )

        # Add storytellers
        if "storytellers" in chronicle_data:
            for username in chronicle_data["storytellers"]:
                mapped_username = user_map.get(username, username)
                try:
                    user = User.objects.get(username=mapped_username)
                    chronicle.storytellers.add(user)
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"  Storyteller {mapped_username} not found, skipping")
                    )

        chronicle.save()
        self.stdout.write(f"  Created chronicle: {chronicle.name} (ID: {chronicle.id})")

        return chronicle

    def import_setting_elements(self, elements_data, chronicle):
        """Import setting elements."""
        self.stdout.write(f"Importing {len(elements_data)} setting elements...")

        for element_json in elements_data:
            fields = element_json["fields"]
            element, created = SettingElement.objects.get_or_create(
                name=fields.get("name", ""),
                defaults={"description": fields.get("description", "")},
            )
            chronicle.common_knowledge_elements.add(element)

    def report_not_imported(self, data):
        """Say which sections of the file this command does not import."""
        xp_requests = data.get("xp_requests", {})
        counts = {
            "characters": len(data.get("characters", [])),
            "items": len(data.get("items", [])),
            "locations": len(data.get("locations", [])),
            "scenes": len(data.get("scenes", [])),
            "journals": len(data.get("journals", [])),
            "XP requests": len(xp_requests.get("weekly", [])) + len(xp_requests.get("story", [])),
        }
        skipped = ", ".join(f"{count} {name}" for name, count in counts.items() if count)
        if skipped:
            self.stdout.write(
                self.style.WARNING(f"Not imported (recreate them by hand): {skipped}")
            )
