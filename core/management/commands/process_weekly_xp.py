"""
Management command to process weekly XP for characters.

Creates Week objects and generates WeeklyXPRequest objects for characters
who participated in finished scenes during the week.
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from game.models import Week, WeeklyXPRequest, get_next_sunday


class Command(BaseCommand):
    help = "Process weekly XP for characters who participated in scenes"

    def add_arguments(self, parser):
        """Define command-line arguments for the process_weekly_xp command."""
        parser.add_argument(
            "--week-ending",
            type=str,
            help="Week ending date (YYYY-MM-DD). Defaults to last Sunday.",
        )
        parser.add_argument(
            "--auto-approve",
            action="store_true",
            help="Automatically approve all XP requests",
        )
        parser.add_argument(
            "--notify",
            action="store_true",
            help="Send notifications to STs about pending requests (requires email setup)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without actually creating it",
        )

    def handle(self, *args, **options):
        """Execute the process_weekly_xp command.

        Creates a Week object and generates WeeklyXPRequest objects for
        characters who participated in finished scenes during the week.
        """
        self.dry_run = options["dry_run"]
        self.auto_approve = options["auto_approve"]

        # Determine week ending date
        if options["week_ending"]:
            from datetime import datetime

            try:
                week_ending = datetime.strptime(options["week_ending"], "%Y-%m-%d").date()
            except ValueError:
                self.stdout.write(self.style.ERROR("Invalid date format. Use YYYY-MM-DD"))
                return
        else:
            # Default to last Sunday
            week_ending = get_next_sunday(now().date())
            if week_ending == now().date() and now().weekday() != 6:
                # If today is not Sunday, use last Sunday
                week_ending = week_ending - timedelta(days=7)

        # Check if week already exists
        existing_week = Week.objects.filter(end_date=week_ending).first()

        if existing_week:
            self.stdout.write(
                self.style.WARNING(
                    f"\nWeek ending {week_ending} already exists (ID: {existing_week.id})"
                )
            )
            week = existing_week
        else:
            if self.dry_run:
                self.stdout.write(
                    self.style.WARNING(f"\n[DRY RUN] Would create week ending {week_ending}")
                )
                week = type("Week", (), {"end_date": week_ending, "id": "NEW"})()
            else:
                week = Week.objects.create(end_date=week_ending)
                self.stdout.write(
                    self.style.SUCCESS(f"\n✓ Created week ending {week_ending} (ID: {week.id})")
                )

        # Get characters who participated in finished scenes this week
        if not self.dry_run and existing_week:
            characters = week.weekly_characters()
        else:
            # For dry run or new week, calculate from scratch
            from django.db.models import Max, OuterRef, Subquery

            from characters.models.core.human import Human
            from game.models import Post, Scene

            week_start = week_ending - timedelta(days=7)

            # Find scenes finished during this week
            recent_post_subquery = (
                Post.objects.filter(scene=OuterRef("pk"))
                .values("scene")
                .annotate(latest_dt=Max("datetime_created"))
                .values("latest_dt")
            )

            finished_scenes = Scene.objects.annotate(
                latest_post_date=Subquery(recent_post_subquery)
            ).filter(
                finished=True,
                latest_post_date__date__gte=week_start,
                latest_post_date__date__lte=week_ending,
            )

            # Get characters from those scenes
            scene_ids = finished_scenes.values_list("id", flat=True)
            characters = (
                Human.objects.filter(scenes__id__in=scene_ids, npc=False)
                .distinct()
                .order_by("name")
            )

        # Display summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("WEEKLY XP PROCESSING"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Week: {week_ending - timedelta(days=7)} to {week_ending}")
        self.stdout.write(f"Characters participating: {characters.count()}")
        self.stdout.write("=" * 70 + "\n")

        if not characters.exists():
            self.stdout.write(self.style.WARNING("No characters participated in scenes this week."))
            return

        # Create XP requests for each character
        created_count = 0
        existing_count = 0
        approved_count = 0

        for character in characters:
            # Check if request already exists
            if not self.dry_run:
                existing = WeeklyXPRequest.objects.filter(week=week, character=character).first()

                if existing:
                    existing_count += 1
                    self.stdout.write(
                        f"  ≈ {character.name}: Request already exists (ID: {existing.id})"
                    )
                    continue

            # Create request
            if self.dry_run:
                self.stdout.write(
                    self.style.WARNING(f"  [DRY RUN] Would create XP request for {character.name}")
                )
                created_count += 1
            else:
                # Use atomic transaction for request creation and auto-approval
                with transaction.atomic():
                    request = WeeklyXPRequest.objects.create(
                        week=week,
                        character=character,
                        finishing=True,  # Default to just finishing XP
                        approved=self.auto_approve,
                    )
                    created_count += 1

                    if self.auto_approve:
                        approved_count += 1
                        # Award XP to character
                        character.add_xp(request.total_xp())
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  ✓ {character.name}: Created and approved "
                                f"(+{request.total_xp()} XP)"
                            )
                        )
                    else:
                        self.stdout.write(
                            f"  ✓ {character.name}: Created request (ID: {request.id})"
                        )

        # Summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("PROCESSING COMPLETE"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Created: {created_count} request(s)")
        if existing_count > 0:
            self.stdout.write(f"Already existed: {existing_count} request(s)")
        if approved_count > 0:
            self.stdout.write(f"Auto-approved: {approved_count} request(s)")
        self.stdout.write("=" * 70 + "\n")

        if self.dry_run:
            self.stdout.write(self.style.WARNING("[DRY RUN] No data was actually created"))

        # Send notifications if requested
        if options["notify"] and not self.dry_run and created_count > 0:
            self.send_notifications(week, created_count)

    def send_notifications(self, week, count):
        """Send notifications to STs about pending requests."""
        self.stdout.write(
            self.style.WARNING(
                f"\nNotification feature not yet implemented. "
                f"{count} request(s) created for week {week.end_date}"
            )
        )
        # Future implementation:
        # - Get all STs for chronicles with pending requests
        # - Send email or create in-app notification
        # - Include link to approval page
