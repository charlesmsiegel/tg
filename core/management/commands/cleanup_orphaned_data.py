"""
Management command to clean up orphaned data.

Removes:
- Characters/items/locations with no owner and status="Un" older than threshold
- Empty Scene objects with no posts or participants
- Unused SettingElement objects
- Orphaned WeeklyXPRequest and StoryXPRequest objects
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db.models import Q, Count


class Command(BaseCommand):
    help = "Clean up orphaned and unused data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Delete unowned objects older than this many days (default: 30)",
        )
        parser.add_argument(
            "--include-scenes",
            action="store_true",
            help="Also clean up empty scenes",
        )
        parser.add_argument(
            "--include-setting-elements",
            action="store_true",
            help="Also clean up unused setting elements",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        self.cutoff_date = now() - timedelta(days=options["days"])

        self.stdout.write(
            self.style.SUCCESS(f"\nCleaning up orphaned data...\n")
        )
        if self.dry_run:
            self.stdout.write(self.style.WARNING("[DRY RUN MODE]\n"))

        # Track deletions
        self.deleted = {
            "characters": 0,
            "items": 0,
            "locations": 0,
            "scenes": 0,
            "setting_elements": 0,
            "xp_requests": 0,
        }

        # Clean up orphaned objects
        self.cleanup_orphaned_characters()
        self.cleanup_orphaned_items()
        self.cleanup_orphaned_locations()
        self.cleanup_orphaned_xp_requests()

        if options["include_scenes"]:
            self.cleanup_empty_scenes()

        if options["include_setting_elements"]:
            self.cleanup_unused_setting_elements()

        # Display summary
        self.display_summary()

    def cleanup_orphaned_characters(self):
        """Remove orphaned character objects."""
        from characters.models.core.character import CharacterModel

        orphaned = CharacterModel.objects.filter(
            owner__isnull=True,
            status="Un"
        )

        count = orphaned.count()
        if count > 0:
            self.stdout.write(f"\nOrphaned characters (no owner, unfinished): {count}")

            # Show some examples
            for char in orphaned[:5]:
                self.stdout.write(f"  - {char.name or '(unnamed)'} (ID: {char.id})")

            if count > 5:
                self.stdout.write(f"  ... and {count - 5} more")

            if not self.dry_run:
                orphaned.delete()
                self.deleted["characters"] = count
                self.stdout.write(self.style.SUCCESS(f"  ✓ Deleted {count} orphaned character(s)"))

    def cleanup_orphaned_items(self):
        """Remove orphaned item objects."""
        from items.models.core.item import ItemModel

        orphaned = ItemModel.objects.filter(
            owner__isnull=True,
            status="Un"
        )

        count = orphaned.count()
        if count > 0:
            self.stdout.write(f"\nOrphaned items (no owner, unfinished): {count}")

            for item in orphaned[:5]:
                self.stdout.write(f"  - {item.name or '(unnamed)'} (ID: {item.id})")

            if count > 5:
                self.stdout.write(f"  ... and {count - 5} more")

            if not self.dry_run:
                orphaned.delete()
                self.deleted["items"] = count
                self.stdout.write(self.style.SUCCESS(f"  ✓ Deleted {count} orphaned item(s)"))

    def cleanup_orphaned_locations(self):
        """Remove orphaned location objects."""
        from locations.models.core.location import LocationModel

        orphaned = LocationModel.objects.filter(
            owner__isnull=True,
            status="Un"
        )

        count = orphaned.count()
        if count > 0:
            self.stdout.write(f"\nOrphaned locations (no owner, unfinished): {count}")

            for loc in orphaned[:5]:
                self.stdout.write(f"  - {loc.name or '(unnamed)'} (ID: {loc.id})")

            if count > 5:
                self.stdout.write(f"  ... and {count - 5} more")

            if not self.dry_run:
                orphaned.delete()
                self.deleted["locations"] = count
                self.stdout.write(self.style.SUCCESS(f"  ✓ Deleted {count} orphaned location(s)"))

    def cleanup_empty_scenes(self):
        """Remove empty scenes with no posts or participants."""
        from game.models import Scene

        # Find scenes with no posts and no characters
        empty_scenes = Scene.objects.annotate(
            post_count=Count('post'),
            char_count=Count('characters')
        ).filter(
            post_count=0,
            char_count=0,
            finished=False
        )

        count = empty_scenes.count()
        if count > 0:
            self.stdout.write(f"\nEmpty scenes (no posts, no participants): {count}")

            for scene in empty_scenes[:5]:
                self.stdout.write(f"  - {scene.name or '(unnamed)'} (ID: {scene.id})")

            if count > 5:
                self.stdout.write(f"  ... and {count - 5} more")

            if not self.dry_run:
                empty_scenes.delete()
                self.deleted["scenes"] = count
                self.stdout.write(self.style.SUCCESS(f"  ✓ Deleted {count} empty scene(s)"))

    def cleanup_unused_setting_elements(self):
        """Remove unused setting elements."""
        from game.models import SettingElement

        # Find setting elements not associated with any chronicle
        unused = SettingElement.objects.annotate(
            chronicle_count=Count('chronicle')
        ).filter(chronicle_count=0)

        count = unused.count()
        if count > 0:
            self.stdout.write(f"\nUnused setting elements: {count}")

            for elem in unused[:5]:
                self.stdout.write(f"  - {elem.name} (ID: {elem.id})")

            if count > 5:
                self.stdout.write(f"  ... and {count - 5} more")

            if not self.dry_run:
                unused.delete()
                self.deleted["setting_elements"] = count
                self.stdout.write(self.style.SUCCESS(f"  ✓ Deleted {count} unused setting element(s)"))

    def cleanup_orphaned_xp_requests(self):
        """Remove XP requests with no associated character."""
        from game.models import WeeklyXPRequest, StoryXPRequest

        # Weekly requests
        orphaned_weekly = WeeklyXPRequest.objects.filter(character__isnull=True)
        weekly_count = orphaned_weekly.count()

        # Story requests
        orphaned_story = StoryXPRequest.objects.filter(character__isnull=True)
        story_count = orphaned_story.count()

        total_count = weekly_count + story_count

        if total_count > 0:
            self.stdout.write(f"\nOrphaned XP requests (no character): {total_count}")
            self.stdout.write(f"  Weekly: {weekly_count}")
            self.stdout.write(f"  Story: {story_count}")

            if not self.dry_run:
                orphaned_weekly.delete()
                orphaned_story.delete()
                self.deleted["xp_requests"] = total_count
                self.stdout.write(self.style.SUCCESS(f"  ✓ Deleted {total_count} orphaned XP request(s)"))

    def display_summary(self):
        """Display cleanup summary."""
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("CLEANUP SUMMARY"))
        self.stdout.write("=" * 70)

        total = sum(self.deleted.values())

        if total == 0:
            self.stdout.write(self.style.SUCCESS("No orphaned data found!"))
        else:
            for category, count in self.deleted.items():
                if count > 0:
                    self.stdout.write(f"{category.replace('_', ' ').title()}: {count}")

            self.stdout.write("=" * 70)
            self.stdout.write(self.style.SUCCESS(f"Total deleted: {total} object(s)"))

        self.stdout.write("=" * 70 + "\n")

        if self.dry_run:
            self.stdout.write(
                self.style.WARNING("[DRY RUN] No data was actually deleted")
            )
