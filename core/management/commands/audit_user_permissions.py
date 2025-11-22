"""
Management command to audit user permissions and ST relationships.

Reports on:
- ST relationships and chronicle access
- Users with ST permissions but no active chronicles
- Profile data completeness (lines/veils for safety tools)
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from game.models import Chronicle, STRelationship


class Command(BaseCommand):
    help = "Audit user permissions and ST relationships"

    def add_arguments(self, parser):
        parser.add_argument(
            "--check-profiles",
            action="store_true",
            help="Check profile data completeness",
        )
        parser.add_argument(
            "--export",
            type=str,
            help="Export audit results to CSV file",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\nAuditing user permissions...\n"))

        # Gather data
        all_users = User.objects.all()
        total_users = all_users.count()

        # ST relationships
        st_relationships = STRelationship.objects.all()
        total_st_rels = st_relationships.count()

        # Users who are STs
        st_user_ids = st_relationships.values_list("user_id", flat=True).distinct()
        st_users = User.objects.filter(id__in=st_user_ids)
        st_count = st_users.count()

        # Chronicles
        total_chronicles = Chronicle.objects.all().count()

        # Display summary
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("USER PERMISSION AUDIT"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Total Users: {total_users}")
        self.stdout.write(f"Total Chronicles: {total_chronicles}")
        self.stdout.write(f"Users with ST Relationships: {st_count}")
        self.stdout.write(f"Total ST Relationships: {total_st_rels}")
        self.stdout.write("")

        # Display ST relationships
        self.display_st_relationships()

        # Check for STs with no active chronicles
        self.check_inactive_sts()

        # Check profile data if requested
        if options["check_profiles"]:
            self.check_profile_completeness()

        # Export if requested
        if options["export"]:
            self.export_audit(options["export"], all_users, st_users)

    def display_st_relationships(self):
        """Display ST relationships by chronicle."""
        from game.models import Chronicle

        self.stdout.write("\nST RELATIONSHIPS BY CHRONICLE")
        self.stdout.write("-" * 70)

        chronicles = Chronicle.objects.all()

        for chronicle in chronicles:
            sts = chronicle.storytellers.all()
            st_names = ", ".join(st.username for st in sts) if sts.exists() else "None"
            self.stdout.write(f"{chronicle.name} (ID: {chronicle.id})")
            self.stdout.write(f"  STs: {st_names}")

        if not chronicles.exists():
            self.stdout.write("No chronicles found")

    def check_inactive_sts(self):
        """Find STs who have no active chronicles."""
        from game.models import STRelationship

        self.stdout.write("\n\nSTORYTELLERS WITH NO ACTIVE CHRONICLES")
        self.stdout.write("-" * 70)

        # Get all ST relationships with null chronicle
        inactive_rels = STRelationship.objects.filter(chronicle__isnull=True)

        if inactive_rels.exists():
            inactive_users = set()
            for rel in inactive_rels:
                if rel.user:
                    inactive_users.add(rel.user)

            for user in inactive_users:
                self.stdout.write(f"  - {user.username} (ID: {user.id})")

            self.stdout.write(f"\nTotal: {len(inactive_users)} user(s)")
        else:
            self.stdout.write("All ST relationships are associated with chronicles")

    def check_profile_completeness(self):
        """Check profile data completeness."""
        from accounts.models import Profile

        self.stdout.write("\n\nPROFILE DATA COMPLETENESS")
        self.stdout.write("-" * 70)

        profiles = Profile.objects.all()
        total = profiles.count()

        # Count profiles with lines/veils set
        with_lines = profiles.exclude(Q(lines="") | Q(lines__isnull=True)).count()
        with_veils = profiles.exclude(Q(veils="") | Q(veils__isnull=True)).count()
        with_discord = profiles.exclude(
            Q(discord_id="") | Q(discord_id__isnull=True)
        ).count()

        # Visibility settings
        lines_visible = profiles.filter(lines_toggle=True).count()
        veils_visible = profiles.filter(veils_toggle=True).count()
        discord_visible = profiles.filter(discord_toggle=True).count()

        self.stdout.write(f"Total Profiles: {total}")
        self.stdout.write(f"\nSafety Tools:")
        self.stdout.write(
            f"  Lines set: {with_lines} ({with_lines/total*100 if total > 0 else 0:.1f}%)"
        )
        self.stdout.write(f"  Lines visible: {lines_visible}")
        self.stdout.write(
            f"  Veils set: {with_veils} ({with_veils/total*100 if total > 0 else 0:.1f}%)"
        )
        self.stdout.write(f"  Veils visible: {veils_visible}")
        self.stdout.write(f"\nContact Info:")
        self.stdout.write(
            f"  Discord ID set: {with_discord} ({with_discord/total*100 if total > 0 else 0:.1f}%)"
        )
        self.stdout.write(f"  Discord visible: {discord_visible}")

    def export_audit(self, filename, all_users, st_users):
        """Export audit results to CSV."""
        import csv

        from accounts.models import Profile

        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "username",
                "email",
                "is_st",
                "chronicles",
                "has_profile",
                "has_lines",
                "has_veils",
                "has_discord",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for user in all_users:
                is_st = user in st_users

                # Get chronicles
                chronicles = Chronicle.objects.filter(storytellers=user)
                chronicle_names = ", ".join(c.name for c in chronicles)

                # Profile data
                try:
                    profile = Profile.objects.get(user=user)
                    has_profile = True
                    has_lines = bool(profile.lines and profile.lines.strip())
                    has_veils = bool(profile.veils and profile.veils.strip())
                    has_discord = bool(
                        profile.discord_id and profile.discord_id.strip()
                    )
                except Profile.DoesNotExist:
                    has_profile = False
                    has_lines = False
                    has_veils = False
                    has_discord = False

                writer.writerow(
                    {
                        "username": user.username,
                        "email": user.email,
                        "is_st": is_st,
                        "chronicles": chronicle_names,
                        "has_profile": has_profile,
                        "has_lines": has_lines,
                        "has_veils": has_veils,
                        "has_discord": has_discord,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"\n✓ Audit exported to {filename}"))


from django.db.models import Q  # Import for check_profile_completeness
