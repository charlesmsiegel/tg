"""
Management command to identify and optionally archive inactive chronicles.

A chronicle is considered inactive if it has:
- No active scenes for X days
- No recent posts/journals for X days
- All characters Retired/Deceased
"""

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Max, Q
from django.utils.timezone import now
from game.models import Chronicle, Scene

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Identify and archive inactive chronicles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Consider chronicles inactive after this many days (default: 90)",
        )
        parser.add_argument(
            "--export-before-archive",
            action="store_true",
            help="Export chronicles to JSON before archiving",
        )
        parser.add_argument(
            "--mark-inactive",
            action="store_true",
            help="Add '[ARCHIVED]' prefix to chronicle names",
        )
        parser.add_argument(
            "--list-only",
            action="store_true",
            help="Only list inactive chronicles without taking action",
        )

    def handle(self, *args, **options):
        self.cutoff_date = now() - timedelta(days=options["days"])
        self.list_only = options["list_only"]

        self.stdout.write(
            self.style.SUCCESS(f"\nFinding chronicles inactive for {options['days']}+ days...\n")
        )

        # Find inactive chronicles
        inactive_chronicles = self.find_inactive_chronicles()

        if not inactive_chronicles:
            self.stdout.write(self.style.SUCCESS("No inactive chronicles found!"))
            return

        # Display findings
        self.display_inactive_chronicles(inactive_chronicles)

        # Take action if requested
        if not self.list_only:
            if options["export_before_archive"]:
                self.export_chronicles(inactive_chronicles)

            if options["mark_inactive"]:
                self.mark_as_archived(inactive_chronicles)

    def find_inactive_chronicles(self):
        """Find chronicles with no recent activity."""
        inactive = []

        for chronicle in Chronicle.objects.all():
            activity_info = self.check_chronicle_activity(chronicle)

            if activity_info["is_inactive"]:
                inactive.append(
                    {
                        "chronicle": chronicle,
                        "info": activity_info,
                    }
                )

        return inactive

    def check_chronicle_activity(self, chronicle):
        """Check various activity indicators for a chronicle."""
        info = {
            "is_inactive": False,
            "last_scene_date": None,
            "active_scene_count": 0,
            "total_scenes": 0,
            "active_character_count": 0,
            "total_characters": 0,
        }

        # Check scenes
        scenes = Scene.objects.filter(chronicle=chronicle)
        info["total_scenes"] = scenes.count()

        if info["total_scenes"] > 0:
            # Find last scene activity
            last_scene = scenes.order_by("-date_of_scene").first()
            if last_scene and last_scene.date_of_scene:
                info["last_scene_date"] = last_scene.date_of_scene

            # Count active scenes
            info["active_scene_count"] = scenes.filter(finished=False).count()

        # Check characters
        from characters.models.core.character import CharacterModel

        characters = CharacterModel.objects.filter(chronicle=chronicle)
        info["total_characters"] = characters.count()
        info["active_character_count"] = characters.filter(status__in=["Sub", "App"]).count()

        # Determine if inactive
        has_no_recent_scenes = (
            info["last_scene_date"] is None or info["last_scene_date"] < self.cutoff_date.date()
        )
        has_no_active_scenes = info["active_scene_count"] == 0
        has_no_active_characters = info["active_character_count"] == 0

        # Chronicle is inactive if it has no recent activity
        info["is_inactive"] = has_no_recent_scenes and (
            has_no_active_scenes or has_no_active_characters
        )

        return info

    def display_inactive_chronicles(self, inactive_chronicles):
        """Display information about inactive chronicles."""
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.WARNING(f"INACTIVE CHRONICLES: {len(inactive_chronicles)}"))
        self.stdout.write("=" * 70 + "\n")

        for item in inactive_chronicles:
            chronicle = item["chronicle"]
            info = item["info"]

            self.stdout.write(f"\n{chronicle.name} (ID: {chronicle.id})")
            self.stdout.write(f"  Storytellers: {chronicle.storyteller_list() or 'None'}")

            if info["last_scene_date"]:
                days_ago = (now().date() - info["last_scene_date"]).days
                self.stdout.write(f"  Last scene: {info['last_scene_date']} ({days_ago} days ago)")
            else:
                self.stdout.write("  Last scene: Never")

            self.stdout.write(
                f"  Scenes: {info['total_scenes']} total, {info['active_scene_count']} active"
            )
            self.stdout.write(
                f"  Characters: {info['total_characters']} total, "
                f"{info['active_character_count']} active"
            )

        self.stdout.write("\n" + "=" * 70 + "\n")

    def export_chronicles(self, inactive_chronicles):
        """Export inactive chronicles to JSON files."""
        import os

        from django.core.management import call_command

        self.stdout.write("\nExporting chronicles...")

        # Create exports directory
        os.makedirs("chronicle_archives", exist_ok=True)

        for item in inactive_chronicles:
            chronicle = item["chronicle"]

            # Safe filename
            safe_name = "".join(
                c if c.isalnum() or c in " _-" else "_" for c in chronicle.name
            ).strip()

            filename = f"chronicle_archives/archive_{chronicle.id}_{safe_name}.json"

            try:
                # Call export_chronicle command
                call_command("export_chronicle", chronicle.id, "--output", filename, "--pretty")
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Exported {chronicle.name} to {filename}")
                )
            except Exception as e:
                logger.error(f"Failed to export chronicle {chronicle.id}: {e}", exc_info=True)
                self.stdout.write(self.style.ERROR(f"  ✗ Failed to export {chronicle.name}: {e}"))

    def mark_as_archived(self, inactive_chronicles):
        """Mark chronicles as archived by prefixing name."""
        self.stdout.write("\nMarking chronicles as archived...")

        for item in inactive_chronicles:
            chronicle = item["chronicle"]

            if not chronicle.name.startswith("[ARCHIVED]"):
                chronicle.name = f"[ARCHIVED] {chronicle.name}"
                chronicle.save()
                self.stdout.write(self.style.SUCCESS(f"  ✓ Marked as archived: {chronicle.name}"))
            else:
                self.stdout.write(f"  - Already archived: {chronicle.name}")
