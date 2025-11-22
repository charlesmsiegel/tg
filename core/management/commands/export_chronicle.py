"""
Management command to export a chronicle and all its related data to JSON.

Exports:
- Chronicle metadata
- Characters
- Items
- Locations
- Scenes and stories
- Journals
- XP requests
- Setting elements
"""
import json
from datetime import date, datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import serialize
from django.db.models import Q
from game.models import (
    Chronicle,
    Journal,
    Scene,
    Story,
    StoryXPRequest,
    WeeklyXPRequest,
)


class Command(BaseCommand):
    help = "Export a chronicle and all related data to JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "chronicle_id",
            type=int,
            help="ID of the chronicle to export",
        )
        parser.add_argument(
            "--output",
            type=str,
            help="Output filename (default: chronicle_<id>_<date>.json)",
        )
        parser.add_argument(
            "--include-users",
            action="store_true",
            help="Include user data (for migration between systems)",
        )
        parser.add_argument(
            "--exclude-scenes",
            action="store_true",
            help="Exclude scene data (useful for large chronicles)",
        )
        parser.add_argument(
            "--pretty",
            action="store_true",
            help="Pretty-print JSON output",
        )

    def handle(self, *args, **options):
        chronicle_id = options["chronicle_id"]

        # Get chronicle
        try:
            chronicle = Chronicle.objects.get(pk=chronicle_id)
        except Chronicle.DoesNotExist:
            raise CommandError(f"Chronicle with ID {chronicle_id} does not exist")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nExporting chronicle: {chronicle.name} (ID: {chronicle_id})\n"
            )
        )

        # Build export data
        export_data = {
            "export_date": datetime.now().isoformat(),
            "export_version": "1.0",
            "chronicle": self.export_chronicle(chronicle),
        }

        # Export related data
        export_data["characters"] = self.export_characters(chronicle)
        export_data["items"] = self.export_items(chronicle)
        export_data["locations"] = self.export_locations(chronicle)
        export_data["setting_elements"] = self.export_setting_elements(chronicle)

        if not options["exclude_scenes"]:
            export_data["scenes"] = self.export_scenes(chronicle)
            export_data["journals"] = self.export_journals(chronicle)

        export_data["xp_requests"] = self.export_xp_requests(chronicle)

        if options["include_users"]:
            export_data["users"] = self.export_users(chronicle)

        # Generate filename
        if options["output"]:
            filename = options["output"]
        else:
            safe_name = "".join(c if c.isalnum() else "_" for c in chronicle.name)
            filename = f"chronicle_{chronicle_id}_{safe_name}_{date.today()}.json"

        # Write to file
        with open(filename, "w") as f:
            if options["pretty"]:
                json.dump(export_data, f, indent=2, default=str)
            else:
                json.dump(export_data, f, default=str)

        # Summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("EXPORT SUMMARY"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Chronicle: {chronicle.name}")
        self.stdout.write(f"Characters: {len(export_data['characters'])}")
        self.stdout.write(f"Items: {len(export_data['items'])}")
        self.stdout.write(f"Locations: {len(export_data['locations'])}")
        if not options["exclude_scenes"]:
            self.stdout.write(f"Scenes: {len(export_data['scenes'])}")
            self.stdout.write(f"Journals: {len(export_data['journals'])}")
        self.stdout.write(f"XP Requests: {len(export_data['xp_requests'])}")
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS(f"\n✓ Export complete: {filename}\n"))

    def export_chronicle(self, chronicle):
        """Export chronicle data."""
        data = json.loads(serialize("json", [chronicle]))[0]

        # Add storyteller usernames
        data["storytellers"] = [st.username for st in chronicle.storytellers.all()]

        return data

    def export_characters(self, chronicle):
        """Export all characters in the chronicle."""
        from characters.models.core.character import CharacterModel

        characters = CharacterModel.objects.filter(chronicle=chronicle)
        self.stdout.write(f"Exporting {characters.count()} characters...")

        return json.loads(serialize("json", characters))

    def export_items(self, chronicle):
        """Export all items in the chronicle."""
        from items.models.core.item import ItemModel

        items = ItemModel.objects.filter(chronicle=chronicle)
        self.stdout.write(f"Exporting {items.count()} items...")

        return json.loads(serialize("json", items))

    def export_locations(self, chronicle):
        """Export all locations in the chronicle."""
        from locations.models.core.location import LocationModel

        locations = LocationModel.objects.filter(chronicle=chronicle)
        self.stdout.write(f"Exporting {locations.count()} locations...")

        return json.loads(serialize("json", locations))

    def export_scenes(self, chronicle):
        """Export all scenes in the chronicle."""
        scenes = Scene.objects.filter(chronicle=chronicle)
        self.stdout.write(f"Exporting {scenes.count()} scenes...")

        return json.loads(serialize("json", scenes))

    def export_journals(self, chronicle):
        """Export all journals in the chronicle."""
        journals = Journal.objects.filter(chronicle=chronicle)
        self.stdout.write(f"Exporting {journals.count()} journals...")

        return json.loads(serialize("json", journals))

    def export_setting_elements(self, chronicle):
        """Export setting elements."""
        elements = chronicle.common_knowledge_elements.all()
        self.stdout.write(f"Exporting {elements.count()} setting elements...")

        return json.loads(serialize("json", elements))

    def export_xp_requests(self, chronicle):
        """Export XP requests for characters in the chronicle."""
        from characters.models.core.character import CharacterModel

        character_ids = CharacterModel.objects.filter(chronicle=chronicle).values_list(
            "id", flat=True
        )

        weekly_requests = WeeklyXPRequest.objects.filter(character_id__in=character_ids)
        story_requests = StoryXPRequest.objects.filter(character_id__in=character_ids)

        self.stdout.write(
            f"Exporting {weekly_requests.count()} weekly + "
            f"{story_requests.count()} story XP requests..."
        )

        return {
            "weekly": json.loads(serialize("json", weekly_requests)),
            "story": json.loads(serialize("json", story_requests)),
        }

    def export_users(self, chronicle):
        """Export user data for chronicle STs and character owners."""
        from django.contrib.auth.models import User

        # Get all STs and character owners
        user_ids = set()
        user_ids.update(chronicle.storytellers.values_list("id", flat=True))

        from characters.models.core.character import CharacterModel

        character_owners = (
            CharacterModel.objects.filter(chronicle=chronicle)
            .exclude(owner__isnull=True)
            .values_list("owner_id", flat=True)
        )
        user_ids.update(character_owners)

        users = User.objects.filter(id__in=user_ids)
        self.stdout.write(f"Exporting {users.count()} users...")

        return json.loads(serialize("json", users))
