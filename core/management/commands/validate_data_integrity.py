"""
Management command to validate data integrity before and after deploying validation constraints.

This command checks for data that would violate the validation constraints and provides
a report of issues that need to be fixed before deployment.

Usage:
    python manage.py validate_data_integrity --fix  # Fix issues automatically
    python manage.py validate_data_integrity        # Report only
"""

from accounts.models import Profile
from characters.models.core.character import Character
from characters.models.core.human import Human
from django.core.management.base import BaseCommand
from django.db.models import F, Q
from game.models import Scene, STRelationship


class Command(BaseCommand):
    help = "Validate data integrity for validation system deployment"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Automatically fix issues (where safe to do so)",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed information about each issue",
        )

    def handle(self, *args, **options):
        fix = options["fix"]
        verbose = options["verbose"]

        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Data Integrity Validation Report"))
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write("")

        total_issues = 0

        # Check 1: Characters with negative XP
        total_issues += self.check_negative_xp(fix, verbose)

        # Check 2: Characters with invalid status
        total_issues += self.check_invalid_status(fix, verbose)

        # Check 3: Attributes out of range (1-10)
        total_issues += self.check_attribute_ranges(fix, verbose)

        # Check 4: Abilities out of range (0-10)
        total_issues += self.check_ability_ranges(fix, verbose)

        # Check 5: Willpower constraints
        total_issues += self.check_willpower_constraints(fix, verbose)

        # Check 6: Age constraints
        total_issues += self.check_age_constraints(fix, verbose)

        # Check 7: Duplicate STRelationships
        total_issues += self.check_duplicate_st_relationships(fix, verbose)

        # Check 8: XP already awarded scenes
        total_issues += self.check_scene_xp_integrity(fix, verbose)

        # Summary
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 70))
        if total_issues == 0:
            self.stdout.write(self.style.SUCCESS("✓ No data integrity issues found!"))
            self.stdout.write(
                self.style.SUCCESS("Database is ready for validation constraints.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⚠ Found {total_issues} data integrity issues")
            )
            if fix:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Issues have been automatically fixed where possible."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Run with --fix flag to automatically fix issues."
                    )
                )
        self.stdout.write(self.style.SUCCESS("=" * 70))

    def check_negative_xp(self, fix, verbose):
        """Check for characters with negative XP."""
        self.stdout.write(self.style.HTTP_INFO("\n1. Checking for negative XP..."))

        negative_xp_chars = Character.objects.filter(xp__lt=0)
        count = negative_xp_chars.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("   ✓ No characters with negative XP"))
            return 0

        self.stdout.write(
            self.style.WARNING(f"   ✗ Found {count} characters with negative XP")
        )

        if verbose:
            for char in negative_xp_chars:
                self.stdout.write(f"     - {char.name} (ID: {char.pk}): XP = {char.xp}")

        if fix:
            updated = negative_xp_chars.update(xp=0)
            self.stdout.write(
                self.style.SUCCESS(f"   → Fixed {updated} characters (set XP to 0)")
            )

        return count

    def check_invalid_status(self, fix, verbose):
        """Check for characters with invalid status values."""
        self.stdout.write(
            self.style.HTTP_INFO("\n2. Checking for invalid status values...")
        )

        valid_statuses = ["Un", "Sub", "App", "Ret", "Dec"]
        invalid_status_chars = Character.objects.exclude(status__in=valid_statuses)
        count = invalid_status_chars.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS("   ✓ All characters have valid status")
            )
            return 0

        self.stdout.write(
            self.style.WARNING(f"   ✗ Found {count} characters with invalid status")
        )

        if verbose:
            for char in invalid_status_chars:
                self.stdout.write(
                    f"     - {char.name} (ID: {char.pk}): status = '{char.status}'"
                )

        if fix:
            # Set invalid statuses to 'Un' (Unfinished) as safe default
            updated = invalid_status_chars.update(status="Un")
            self.stdout.write(
                self.style.SUCCESS(
                    f"   → Fixed {updated} characters (set status to 'Un')"
                )
            )

        return count

    def check_attribute_ranges(self, fix, verbose):
        """Check for attributes outside valid range (1-10)."""
        self.stdout.write(
            self.style.HTTP_INFO("\n3. Checking attribute ranges (1-10)...")
        )

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

        total_issues = 0

        for attr in attributes:
            # Check for values < 1 or > 10
            filter_kwargs = {f"{attr}__lt": 1}
            low_chars = Human.objects.filter(**filter_kwargs)

            filter_kwargs = {f"{attr}__gt": 10}
            high_chars = Human.objects.filter(**filter_kwargs)

            low_count = low_chars.count()
            high_count = high_chars.count()

            if low_count > 0:
                total_issues += low_count
                self.stdout.write(
                    self.style.WARNING(f"   ✗ {low_count} characters with {attr} < 1")
                )
                if fix:
                    update_kwargs = {attr: 1}
                    low_chars.update(**update_kwargs)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"     → Fixed {low_count} characters (set to 1)"
                        )
                    )

            if high_count > 0:
                total_issues += high_count
                self.stdout.write(
                    self.style.WARNING(f"   ✗ {high_count} characters with {attr} > 10")
                )
                if fix:
                    update_kwargs = {attr: 10}
                    high_chars.update(**update_kwargs)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"     → Fixed {high_count} characters (set to 10)"
                        )
                    )

        if total_issues == 0:
            self.stdout.write(
                self.style.SUCCESS("   ✓ All attributes in valid range (1-10)")
            )

        return total_issues

    def check_ability_ranges(self, fix, verbose):
        """Check for abilities outside valid range (0-10)."""
        self.stdout.write(
            self.style.HTTP_INFO("\n4. Checking ability ranges (0-10)...")
        )

        # Get all ability field names from Human model
        abilities = [
            "alertness",
            "athletics",
            "brawl",
            "empathy",
            "expression",
            "intimidation",
            "streetwise",
            "subterfuge",
            "crafts",
            "drive",
            "etiquette",
            "firearms",
            "melee",
            "stealth",
            "academics",
            "computer",
            "investigation",
            "medicine",
            "science",
        ]

        total_issues = 0

        for ability in abilities:
            # Check for values < 0 or > 10
            filter_kwargs = {f"{ability}__lt": 0}
            low_chars = Human.objects.filter(**filter_kwargs)

            filter_kwargs = {f"{ability}__gt": 10}
            high_chars = Human.objects.filter(**filter_kwargs)

            low_count = low_chars.count()
            high_count = high_chars.count()

            if low_count > 0:
                total_issues += low_count
                self.stdout.write(
                    self.style.WARNING(
                        f"   ✗ {low_count} characters with {ability} < 0"
                    )
                )
                if fix:
                    update_kwargs = {ability: 0}
                    low_chars.update(**update_kwargs)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"     → Fixed {low_count} characters (set to 0)"
                        )
                    )

            if high_count > 0:
                total_issues += high_count
                self.stdout.write(
                    self.style.WARNING(
                        f"   ✗ {high_count} characters with {ability} > 10"
                    )
                )
                if fix:
                    update_kwargs = {ability: 10}
                    high_chars.update(**update_kwargs)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"     → Fixed {high_count} characters (set to 10)"
                        )
                    )

        if total_issues == 0:
            self.stdout.write(
                self.style.SUCCESS("   ✓ All abilities in valid range (0-10)")
            )

        return total_issues

    def check_willpower_constraints(self, fix, verbose):
        """Check willpower constraints."""
        self.stdout.write(
            self.style.HTTP_INFO("\n5. Checking willpower constraints...")
        )

        total_issues = 0

        # Willpower range (1-10)
        low_wp = Human.objects.filter(willpower__lt=1)
        high_wp = Human.objects.filter(willpower__gt=10)

        if low_wp.exists():
            count = low_wp.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(f"   ✗ {count} characters with willpower < 1")
            )
            if fix:
                low_wp.update(willpower=1)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to 1)"))

        if high_wp.exists():
            count = high_wp.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(f"   ✗ {count} characters with willpower > 10")
            )
            if fix:
                high_wp.update(willpower=10)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to 10)"))

        # Temporary willpower range (0-10)
        low_temp = Human.objects.filter(temporary_willpower__lt=0)
        high_temp = Human.objects.filter(temporary_willpower__gt=10)

        if low_temp.exists():
            count = low_temp.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(f"   ✗ {count} characters with temp willpower < 0")
            )
            if fix:
                low_temp.update(temporary_willpower=0)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to 0)"))

        if high_temp.exists():
            count = high_temp.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(f"   ✗ {count} characters with temp willpower > 10")
            )
            if fix:
                high_temp.update(temporary_willpower=10)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to 10)"))

        # Temp <= permanent
        temp_exceeds = Human.objects.filter(temporary_willpower__gt=F("willpower"))
        if temp_exceeds.exists():
            count = temp_exceeds.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(
                    f"   ✗ {count} characters with temp willpower > permanent"
                )
            )
            if fix:
                # Set temp to equal permanent
                for human in temp_exceeds:
                    human.temporary_willpower = human.willpower
                    human.save()
                self.stdout.write(
                    self.style.SUCCESS(f"     → Fixed (set temp = permanent)")
                )

        if total_issues == 0:
            self.stdout.write(self.style.SUCCESS("   ✓ All willpower values valid"))

        return total_issues

    def check_age_constraints(self, fix, verbose):
        """Check age constraints."""
        self.stdout.write(self.style.HTTP_INFO("\n6. Checking age constraints..."))

        total_issues = 0

        # Age range (0-500)
        negative_age = Human.objects.filter(age__lt=0)
        excessive_age = Human.objects.filter(age__gt=500)

        if negative_age.exists():
            count = negative_age.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(f"   ✗ {count} characters with negative age")
            )
            if fix:
                negative_age.update(age=None)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to NULL)"))

        if excessive_age.exists():
            count = excessive_age.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(f"   ✗ {count} characters with age > 500")
            )
            if fix:
                excessive_age.update(age=500)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to 500)"))

        # Apparent age (0-200)
        negative_apparent = Human.objects.filter(apparent_age__lt=0)
        excessive_apparent = Human.objects.filter(apparent_age__gt=200)

        if negative_apparent.exists():
            count = negative_apparent.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(
                    f"   ✗ {count} characters with negative apparent age"
                )
            )
            if fix:
                negative_apparent.update(apparent_age=None)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to NULL)"))

        if excessive_apparent.exists():
            count = excessive_apparent.count()
            total_issues += count
            self.stdout.write(
                self.style.WARNING(f"   ✗ {count} characters with apparent age > 200")
            )
            if fix:
                excessive_apparent.update(apparent_age=200)
                self.stdout.write(self.style.SUCCESS(f"     → Fixed (set to 200)"))

        if total_issues == 0:
            self.stdout.write(self.style.SUCCESS("   ✓ All age values valid"))

        return total_issues

    def check_duplicate_st_relationships(self, fix, verbose):
        """Check for duplicate STRelationships."""
        self.stdout.write(
            self.style.HTTP_INFO("\n7. Checking for duplicate ST relationships...")
        )

        # Find duplicates by grouping
        from django.db.models import Count

        duplicates = (
            STRelationship.objects.values("user", "chronicle", "gameline")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
        )

        count = duplicates.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("   ✓ No duplicate ST relationships"))
            return 0

        self.stdout.write(
            self.style.WARNING(f"   ✗ Found {count} duplicate ST relationships")
        )

        if verbose or fix:
            for dup in duplicates:
                # Get all instances of this duplicate
                instances = STRelationship.objects.filter(
                    user=dup["user"],
                    chronicle=dup["chronicle"],
                    gameline=dup["gameline"],
                )

                if verbose:
                    self.stdout.write(
                        f"     - User {dup['user']}, Chronicle {dup['chronicle']}, "
                        f"Gameline {dup['gameline']}: {dup['count']} instances"
                    )

                if fix:
                    # Keep the first one, delete the rest
                    first = instances.first()
                    deleted = instances.exclude(pk=first.pk).delete()[0]
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"     → Kept 1, deleted {deleted} duplicates"
                        )
                    )

        return count

    def check_scene_xp_integrity(self, fix, verbose):
        """Check for scenes with inconsistent XP state."""
        self.stdout.write(self.style.HTTP_INFO("\n8. Checking scene XP integrity..."))

        # This is more of an informational check - we can't automatically fix this
        scenes_with_xp_given = Scene.objects.filter(xp_given=True).count()
        scenes_without_xp = Scene.objects.filter(finished=True, xp_given=False).count()

        self.stdout.write(
            self.style.SUCCESS(f"   ℹ {scenes_with_xp_given} scenes have XP awarded")
        )
        self.stdout.write(
            self.style.SUCCESS(f"   ℹ {scenes_without_xp} finished scenes awaiting XP")
        )

        # No issues to report - this is informational only
        return 0
