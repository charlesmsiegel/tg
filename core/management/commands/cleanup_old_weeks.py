"""
Management command to clean up old Week objects.

Archives or deletes Week objects older than a threshold while preserving
XP data in character records.
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from game.models import Week


class Command(BaseCommand):
    help = "Clean up old Week objects to prevent unbounded growth"

    def add_arguments(self, parser):
        parser.add_argument(
            "--months",
            type=int,
            default=6,
            help="Delete weeks older than this many months (default: 6)",
        )
        parser.add_argument(
            "--keep-with-pending",
            action="store_true",
            help="Keep weeks that have pending XP requests",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        cutoff_date = now().date() - timedelta(days=options["months"] * 30)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nFinding weeks older than {options['months']} months "
                f"(before {cutoff_date})...\n"
            )
        )

        if self.dry_run:
            self.stdout.write(self.style.WARNING("[DRY RUN MODE]\n"))

        # Find old weeks
        old_weeks = Week.objects.filter(end_date__lt=cutoff_date)

        if options["keep_with_pending"]:
            # Filter out weeks with pending requests
            from game.models import WeeklyXPRequest

            weeks_with_pending = WeeklyXPRequest.objects.filter(
                approved=False
            ).values_list("week_id", flat=True)

            old_weeks = old_weeks.exclude(id__in=weeks_with_pending)

        count = old_weeks.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS("No old weeks found to clean up!")
            )
            return

        # Display information
        self.stdout.write(f"Found {count} old week(s) to delete:\n")

        for week in old_weeks[:10]:
            self.stdout.write(f"  - {week} (ID: {week.id})")

        if count > 10:
            self.stdout.write(f"  ... and {count - 10} more")

        # Delete
        if not self.dry_run:
            old_weeks.delete()
            self.stdout.write(
                self.style.SUCCESS(f"\n✓ Deleted {count} old week(s)")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"\n[DRY RUN] Would delete {count} week(s)")
            )
