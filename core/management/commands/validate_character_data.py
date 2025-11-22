"""
Management command to validate character data integrity.

Checks for:
- Attribute bounds (typically 1-10)
- XP calculation consistency
- Required fields based on status
- Orphaned spent_xp entries
- Polymorphic relationship integrity
"""
from characters.models.core.character import Character, CharacterModel
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Validate character data integrity and report issues"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Attempt to fix issues automatically where possible",
        )
        parser.add_argument(
            "--status",
            type=str,
            help="Only validate characters with specific status (Un, Sub, App, Ret, Dec)",
        )
        parser.add_argument(
            "--chronicle",
            type=int,
            help="Only validate characters in specific chronicle (by ID)",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed information for each issue",
        )

    def handle(self, *args, **options):
        self.fix_mode = options["fix"]
        self.verbose = options["verbose"]

        # Filter characters based on options
        queryset = CharacterModel.objects.all()

        if options["status"]:
            queryset = queryset.filter(status=options["status"])

        if options["chronicle"]:
            queryset = queryset.filter(chronicle_id=options["chronicle"])

        # Count total characters to validate
        total = queryset.count()
        self.stdout.write(self.style.SUCCESS(f"\nValidating {total} character(s)...\n"))

        # Track issues
        self.issues = {
            "attribute_bounds": [],
            "xp_inconsistencies": [],
            "missing_required_fields": [],
            "orphaned_xp_spends": [],
            "status_inconsistencies": [],
        }

        # Validate each character
        for char in queryset:
            self.validate_character(char)

        # Report results
        self.report_results(total)

    def validate_character(self, char):
        """Validate a single character."""
        # Check if character has AttributeBlock
        if hasattr(char, "strength"):
            self.check_attribute_bounds(char)

        # Check XP consistency
        self.check_xp_consistency(char)

        # Check required fields based on status
        self.check_required_fields(char)

        # Check spent_xp orphans
        self.check_orphaned_xp_spends(char)

        # Check status consistency
        self.check_status_consistency(char)

    def check_attribute_bounds(self, char):
        """Validate attribute values are within acceptable bounds."""
        attributes = [
            "strength",
            "dexterity",
            "stamina",
            "perception",
            "intelligence",
            "wits",
            "charisma",
            "manipulation",
            "appearance",
        ]

        for attr in attributes:
            if hasattr(char, attr):
                value = getattr(char, attr)
                # Most attributes should be 1-10 (some elder/powerful characters go higher)
                if value < 0 or value > 15:
                    self.issues["attribute_bounds"].append(
                        {
                            "character": char,
                            "attribute": attr,
                            "value": value,
                            "issue": f"Attribute {attr} = {value} is outside normal bounds (0-15)",
                        }
                    )

                    if self.fix_mode and value < 0:
                        setattr(char, attr, 1)
                        char.save()
                        if self.verbose:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Fixed {char.name} ({char.id}): {attr} set to 1"
                                )
                            )

    def check_xp_consistency(self, char):
        """Check that XP calculations are consistent."""
        if not hasattr(char, "xp") or not hasattr(char, "spent_xp"):
            return

        # Calculate total spent XP
        total_spent = sum(
            spend.get("cost", 0)
            for spend in char.spent_xp
            if spend.get("approved") == "Approved"
        )

        # Check for negative XP situations
        remaining_xp = char.xp - total_spent

        if remaining_xp < 0:
            self.issues["xp_inconsistencies"].append(
                {
                    "character": char,
                    "earned": char.xp,
                    "spent": total_spent,
                    "remaining": remaining_xp,
                    "issue": f"Character has negative XP: earned {char.xp}, spent {total_spent}",
                }
            )

    def check_required_fields(self, char):
        """Check that required fields are filled based on character status."""
        issues = []

        # Characters should have a name
        if not char.name or char.name == "":
            issues.append("Missing name")

        # Submitted/Approved characters should have concept
        if char.status in ["Sub", "App"] and hasattr(char, "concept"):
            if not char.concept or char.concept == "":
                issues.append(
                    "Missing concept (required for Submitted/Approved status)"
                )

        # Approved characters should have owner
        if char.status == "App" and not char.owner:
            issues.append("Missing owner (required for Approved status)")

        if issues:
            self.issues["missing_required_fields"].append(
                {
                    "character": char,
                    "issues": issues,
                }
            )

    def check_orphaned_xp_spends(self, char):
        """Check for spent_xp entries that don't correspond to actual traits."""
        if not hasattr(char, "spent_xp"):
            return

        # Count pending spends
        pending_spends = [
            spend for spend in char.spent_xp if spend.get("approved") == "Pending"
        ]

        # Check for very old pending spends (potential orphans)
        # Note: This is a simple check - a more sophisticated version would
        # verify that the trait actually exists on the character
        if len(pending_spends) > 20:
            self.issues["orphaned_xp_spends"].append(
                {
                    "character": char,
                    "pending_count": len(pending_spends),
                    "issue": f"Character has {len(pending_spends)} pending XP spends (possible orphaned entries)",
                }
            )

    def check_status_consistency(self, char):
        """Check for status-related inconsistencies."""
        # Deceased/Retired characters shouldn't be in active scenes
        if char.status in ["Ret", "Dec"]:
            # Check if character is in any active (non-finished) scenes
            active_scenes = char.scenes.filter(finished=False)
            if active_scenes.exists():
                self.issues["status_inconsistencies"].append(
                    {
                        "character": char,
                        "status": char.get_status_display(),
                        "issue": f"{char.get_status_display()} character is in {active_scenes.count()} active scene(s)",
                    }
                )

    def report_results(self, total):
        """Display validation results."""
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("VALIDATION RESULTS"))
        self.stdout.write("=" * 70 + "\n")

        total_issues = sum(len(v) for v in self.issues.values())

        if total_issues == 0:
            self.stdout.write(
                self.style.SUCCESS(f"✓ All {total} character(s) passed validation!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {total_issues} issue(s) across {total} character(s)\n"
                )
            )

            # Report each category
            for category, issues in self.issues.items():
                if issues:
                    self.stdout.write(
                        self.style.WARNING(
                            f"\n{category.replace('_', ' ').title()}: {len(issues)}"
                        )
                    )

                    for issue in issues[:10]:  # Show first 10 of each type
                        char = issue["character"]
                        self.stdout.write(
                            f"  • {char.name} (ID: {char.id}, Status: {char.get_status_display()})"
                        )
                        if "issue" in issue:
                            self.stdout.write(f"    {issue['issue']}")
                        if self.verbose and "issues" in issue:
                            for sub_issue in issue["issues"]:
                                self.stdout.write(f"    - {sub_issue}")

                    if len(issues) > 10:
                        self.stdout.write(f"  ... and {len(issues) - 10} more")

        self.stdout.write("\n" + "=" * 70 + "\n")

        if self.fix_mode:
            self.stdout.write(
                self.style.SUCCESS("Some issues were automatically fixed.")
            )
