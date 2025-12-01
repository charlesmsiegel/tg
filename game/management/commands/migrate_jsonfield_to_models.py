"""
Management command to migrate existing JSONField data to proper model instances.

This migrates:
- spent_xp (JSONField) -> XPSpendingRequest instances
- spent_freebies (JSONField) -> FreebieSpendingRecord instances

Usage:
    python manage.py migrate_jsonfield_to_models
    python manage.py migrate_jsonfield_to_models --dry-run  # Preview changes without saving
"""

from characters.models.core.character import Character
from characters.models.core.human import Human
from django.core.management.base import BaseCommand
from django.db import transaction
from game.models import FreebieSpendingRecord, XPSpendingRequest


class Command(BaseCommand):
    help = "Migrate spent_xp and spent_freebies JSONField data to proper model instances"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without saving to database",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be saved"))

        self.stdout.write("Starting migration of JSONField data to models...")

        # Migrate XP spending records
        self.migrate_xp_spending(dry_run)

        # Migrate freebie spending records
        self.migrate_freebie_spending(dry_run)

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN COMPLETE - No changes were saved"))
        else:
            self.stdout.write(self.style.SUCCESS("Migration complete!"))

    @transaction.atomic
    def migrate_xp_spending(self, dry_run):
        """Migrate spent_xp JSONField to XPSpendingRequest model."""
        self.stdout.write("\nMigrating XP spending records...")

        characters_with_xp = Character.objects.exclude(spent_xp=[])
        total_records = 0
        migrated_records = 0

        for character in characters_with_xp:
            for xp_record in character.spent_xp:
                total_records += 1

                # Skip if already migrated (check by index or unique criteria)
                index = xp_record.get("index", "")
                trait_name = xp_record.get("trait", "")
                cost = xp_record.get("cost", 0)
                approved = xp_record.get("approved", "Pending")

                # Check if this record already exists
                existing = XPSpendingRequest.objects.filter(
                    character=character,
                    trait_name=trait_name,
                    cost=cost,
                    approved=approved,
                ).exists()

                if existing:
                    self.stdout.write(f"  Skipping duplicate: {character.name} - {trait_name}")
                    continue

                if not dry_run:
                    XPSpendingRequest.objects.create(
                        character=character,
                        trait_name=trait_name,
                        trait_type=xp_record.get("value", ""),  # May need adjustment
                        trait_value=xp_record.get("value", 0),
                        cost=cost,
                        approved=approved,
                    )

                migrated_records += 1
                self.stdout.write(
                    f"  Migrated: {character.name} - {trait_name} ({cost} XP, {approved})"
                )

        self.stdout.write(
            self.style.SUCCESS(f"XP Migration: {migrated_records}/{total_records} records migrated")
        )

    @transaction.atomic
    def migrate_freebie_spending(self, dry_run):
        """Migrate spent_freebies JSONField to FreebieSpendingRecord model."""
        self.stdout.write("\nMigrating freebie spending records...")

        humans_with_freebies = Human.objects.exclude(spent_freebies=[])
        total_records = 0
        migrated_records = 0

        for human in humans_with_freebies:
            for freebie_record in human.spent_freebies:
                total_records += 1

                trait_name = freebie_record.get("trait", "")
                cost = freebie_record.get("cost", 0)
                value = freebie_record.get("value", 0)

                # Check if this record already exists
                existing = FreebieSpendingRecord.objects.filter(
                    character=human, trait_name=trait_name, cost=cost, trait_value=value
                ).exists()

                if existing:
                    self.stdout.write(f"  Skipping duplicate: {human.name} - {trait_name}")
                    continue

                if not dry_run:
                    FreebieSpendingRecord.objects.create(
                        character=human,
                        trait_name=trait_name,
                        trait_type="",  # Not stored in original JSONField
                        trait_value=value,
                        cost=cost,
                    )

                migrated_records += 1
                self.stdout.write(f"  Migrated: {human.name} - {trait_name} ({cost} freebies)")

        self.stdout.write(
            self.style.SUCCESS(
                f"Freebie Migration: {migrated_records}/{total_records} records migrated"
            )
        )
