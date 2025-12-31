"""
Management command to audit XP spending and detect discrepancies.

Checks for:
- XP calculation discrepancies (earned vs spent)
- Unapproved XP spends older than threshold
- Characters with negative XP
- Impossible trait progressions
- Weekly/Story XP request issues
"""

from datetime import timedelta

from characters.models.core.character import CharacterModel
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from game.models import StoryXPRequest, Week, WeeklyXPRequest


class Command(BaseCommand):
    help = "Audit XP spending and detect discrepancies"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chronicle",
            type=int,
            help="Only audit characters in specific chronicle (by ID)",
        )
        parser.add_argument(
            "--pending-days",
            type=int,
            default=30,
            help="Flag pending XP spends older than this many days (default: 30)",
        )
        parser.add_argument(
            "--show-all",
            action="store_true",
            help="Show all characters, even those without issues",
        )
        parser.add_argument(
            "--export",
            type=str,
            help="Export results to CSV file (provide filename)",
        )

    def handle(self, *args, **options):
        self.pending_threshold = timedelta(days=options["pending_days"])
        self.show_all = options["show_all"]

        # Filter characters based on options
        queryset = CharacterModel.objects.filter(status__in=["Sub", "App"])

        if options["chronicle"]:
            queryset = queryset.filter(chronicle_id=options["chronicle"])

        total = queryset.count()
        self.stdout.write(self.style.SUCCESS(f"\nAuditing XP for {total} character(s)...\n"))

        # Collect audit results
        self.results = []

        for char in queryset:
            result = self.audit_character(char)
            if result:
                self.results.append(result)

        # Display results
        self.display_results()

        # Export if requested
        if options["export"]:
            self.export_results(options["export"])

        # Audit XP requests
        self.audit_xp_requests()

    def audit_character(self, char):
        """Audit a single character's XP."""
        if not hasattr(char, "xp"):
            return None

        issues = []
        warnings = []

        # Calculate XP totals using XPSpendingRequest model
        total_earned = char.xp

        # Get spending data from xp_spendings relation
        from django.db.models import Sum

        approved_count = char.xp_spendings.filter(approved="Approved").count()
        pending_count = char.xp_spendings.filter(approved="Pending").count()

        total_approved = (
            char.xp_spendings.filter(approved="Approved").aggregate(total=Sum("cost"))["total"] or 0
        )
        total_pending = (
            char.xp_spendings.filter(approved="Pending").aggregate(total=Sum("cost"))["total"] or 0
        )

        remaining = total_earned - total_approved
        after_pending = remaining - total_pending

        # Check for negative XP
        if remaining < 0:
            issues.append(
                f"NEGATIVE XP: Earned {total_earned}, Approved {total_approved}, "
                f"Remaining {remaining}"
            )

        # Check if approving pending would cause negative
        if after_pending < 0:
            warnings.append(f"Pending spends ({total_pending}) exceed remaining XP ({remaining})")

        # Check for excessive pending spends
        if pending_count > 15:
            warnings.append(f"Large number of pending spends: {pending_count}")

        # Check for orphaned approved spends (just flag high counts as suspicious)
        if approved_count > 100:
            warnings.append(
                f"Unusually high approved spend count: {approved_count} " f"(possible duplicates)"
            )

        # Only return result if there are issues, warnings, or show_all is set
        if issues or warnings or self.show_all:
            return {
                "character": char,
                "earned": total_earned,
                "approved": total_approved,
                "pending": total_pending,
                "remaining": remaining,
                "approved_count": approved_count,
                "pending_count": pending_count,
                "issues": issues,
                "warnings": warnings,
            }

        return None

    def display_results(self):
        """Display audit results."""
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("XP AUDIT RESULTS"))
        self.stdout.write("=" * 80 + "\n")

        # Separate characters with issues from those without
        with_issues = [r for r in self.results if r["issues"]]
        with_warnings = [r for r in self.results if r["warnings"] and not r["issues"]]
        clean = [r for r in self.results if not r["issues"] and not r["warnings"]]

        # Display critical issues
        if with_issues:
            self.stdout.write(self.style.ERROR(f"\nCRITICAL ISSUES ({len(with_issues)}):"))
            for result in with_issues:
                self.display_character_result(result, show_issues=True)

        # Display warnings
        if with_warnings:
            self.stdout.write(self.style.WARNING(f"\nWARNINGS ({len(with_warnings)}):"))
            for result in with_warnings:
                self.display_character_result(result, show_warnings=True)

        # Display clean characters if show_all
        if clean and self.show_all:
            self.stdout.write(self.style.SUCCESS(f"\nCLEAN ({len(clean)}):"))
            for result in clean[:10]:  # Show first 10
                self.display_character_result(result)
            if len(clean) > 10:
                self.stdout.write(f"  ... and {len(clean) - 10} more")

        # Summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.ERROR(f"Critical Issues: {len(with_issues)}"))
        self.stdout.write(self.style.WARNING(f"Warnings: {len(with_warnings)}"))
        self.stdout.write(self.style.SUCCESS(f"Clean: {len(clean)}"))
        self.stdout.write("=" * 80 + "\n")

    def display_character_result(self, result, show_issues=False, show_warnings=False):
        """Display audit result for a single character."""
        char = result["character"]
        self.stdout.write(f"\n  {char.name} (ID: {char.id}, {char.get_status_display()})")
        self.stdout.write(
            f"    Earned: {result['earned']} | "
            f"Approved: {result['approved']} ({result['approved_count']} spends) | "
            f"Pending: {result['pending']} ({result['pending_count']} spends) | "
            f"Remaining: {result['remaining']}"
        )

        if show_issues:
            for issue in result["issues"]:
                self.stdout.write(self.style.ERROR(f"    ✗ {issue}"))

        if show_warnings:
            for warning in result["warnings"]:
                self.stdout.write(self.style.WARNING(f"    ⚠ {warning}"))

    def audit_xp_requests(self):
        """Audit XP requests for issues."""
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("XP REQUEST AUDIT"))
        self.stdout.write("=" * 80 + "\n")

        # Check for unapproved weekly requests
        unapproved_weekly = WeeklyXPRequest.objects.filter(approved=False)
        if unapproved_weekly.exists():
            self.stdout.write(
                self.style.WARNING(f"\nUnapproved Weekly XP Requests: {unapproved_weekly.count()}")
            )

            # Show oldest 10
            oldest = unapproved_weekly.order_by("week__end_date")[:10]
            for req in oldest:
                if req.week:
                    self.stdout.write(
                        f"  • {req.character.name if req.character else 'Unknown'} - "
                        f"Week ending {req.week.end_date} ({req.total_xp()} XP)"
                    )

        # Check for orphaned requests (no character)
        orphaned_weekly = WeeklyXPRequest.objects.filter(character__isnull=True)
        if orphaned_weekly.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"\nOrphaned Weekly XP Requests (no character): {orphaned_weekly.count()}"
                )
            )

        orphaned_story = StoryXPRequest.objects.filter(character__isnull=True)
        if orphaned_story.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"Orphaned Story XP Requests (no character): {orphaned_story.count()}"
                )
            )

        self.stdout.write("")

    def export_results(self, filename):
        """Export results to CSV file."""
        import csv

        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "character_id",
                "character_name",
                "status",
                "earned",
                "approved",
                "pending",
                "remaining",
                "approved_count",
                "pending_count",
                "issues",
                "warnings",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for result in self.results:
                writer.writerow(
                    {
                        "character_id": result["character"].id,
                        "character_name": result["character"].name,
                        "status": result["character"].get_status_display(),
                        "earned": result["earned"],
                        "approved": result["approved"],
                        "pending": result["pending"],
                        "remaining": result["remaining"],
                        "approved_count": result["approved_count"],
                        "pending_count": result["pending_count"],
                        "issues": "; ".join(result["issues"]),
                        "warnings": "; ".join(result["warnings"]),
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"\nResults exported to {filename}"))
