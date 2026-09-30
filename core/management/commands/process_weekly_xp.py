"""
Management command to process weekly XP for characters.

Creates the Week, records the characters who took part in its finished scenes on
Week.characters (which the storyteller and player XP queues read), and generates a
WeeklyXPRequest for each of them.
"""

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from game.models import Week, WeeklyXPRequest


def most_recent_sunday(day):
    """``day`` itself when it is a Sunday, else the Sunday before it."""
    # weekday(): Monday=0, Sunday=6
    return day - timedelta(days=(day.weekday() + 1) % 7)


class Command(BaseCommand):
    help = "Process weekly XP for characters who participated in scenes"

    def add_arguments(self, parser):
        """Define command-line arguments for the process_weekly_xp command."""
        parser.add_argument(
            "--week-ending",
            type=str,
            help="Week ending date (YYYY-MM-DD). Defaults to the most recent Sunday.",
        )
        parser.add_argument(
            "--auto-approve",
            action="store_true",
            help="Approve each new request and award its XP",
        )
        parser.add_argument(
            "--notify",
            action="store_true",
            help=(
                "Print a reminder with the number of new requests; nothing is sent "
                "(storytellers see pending requests in their queue)"
            ),
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without actually creating it",
        )

    def handle(self, *args, **options):
        """Execute the process_weekly_xp command."""
        self.dry_run = options["dry_run"]
        self.auto_approve = options["auto_approve"]

        # Determine week ending date
        if options["week_ending"]:
            try:
                week_ending = datetime.strptime(options["week_ending"], "%Y-%m-%d").date()
            except ValueError:
                self.stdout.write(self.style.ERROR("Invalid date format. Use YYYY-MM-DD"))
                return
        else:
            week_ending = most_recent_sunday(now().date())

        week = Week.objects.filter(end_date=week_ending).first()
        if week:
            self.stdout.write(
                self.style.WARNING(f"\nWeek ending {week_ending} already exists (ID: {week.id})")
            )
        elif self.dry_run:
            self.stdout.write(
                self.style.WARNING(f"\n[DRY RUN] Would create week ending {week_ending}")
            )
        else:
            week = Week.objects.create(end_date=week_ending)
            self.stdout.write(
                self.style.SUCCESS(f"\n✓ Created week ending {week_ending} (ID: {week.id})")
            )

        # Characters in scenes finished during the week; an unsaved Week computes the
        # same set for a dry run.
        characters = list((week or Week(end_date=week_ending)).weekly_characters())

        # Display summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("WEEKLY XP PROCESSING"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Week: {week_ending - timedelta(days=7)} to {week_ending}")
        self.stdout.write(f"Characters participating: {len(characters)}")
        self.stdout.write("=" * 70 + "\n")

        if not characters:
            self.stdout.write(self.style.WARNING("No characters participated in scenes this week."))
            return

        if not self.dry_run:
            # The XP queues list (character, week) pairs from Week.characters.
            week.characters.add(*characters)

        # Create XP requests for each character
        created_count = 0
        existing_count = 0
        approved_count = 0

        for character in characters:
            if self.dry_run:
                self.stdout.write(
                    self.style.WARNING(f"  [DRY RUN] Would create XP request for {character.name}")
                )
                created_count += 1
                continue

            existing = WeeklyXPRequest.objects.filter(week=week, character=character).first()
            if existing:
                existing_count += 1
                self.stdout.write(
                    f"  ≈ {character.name}: Request already exists (ID: {existing.id})"
                )
                continue

            with transaction.atomic():
                request = WeeklyXPRequest.objects.create(
                    week=week,
                    character=character,
                    finishing=True,  # Default to just finishing XP
                )
                created_count += 1

                if self.auto_approve:
                    awarded = request.approve()
                    approved_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ {character.name}: Created and approved (+{awarded} XP)"
                        )
                    )
                else:
                    self.stdout.write(f"  ✓ {character.name}: Created request (ID: {request.id})")

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

        if options["notify"] and not self.dry_run and created_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"\n{created_count} request(s) created for week {week.end_date}; "
                    "no notification is sent, storytellers see them in their queue."
                )
            )
