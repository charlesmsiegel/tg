"""
Management command to generate a dashboard-style report for Storytellers.

Shows:
- Pending approvals count
- Active scenes
- Recent XP requests
- Character status breakdown
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from game.models import Chronicle, Scene, WeeklyXPRequest


class Command(BaseCommand):
    help = "Generate dashboard-style report for Storytellers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--st-username",
            type=str,
            help="Generate report for specific ST (username)",
        )
        parser.add_argument(
            "--chronicle",
            type=int,
            help="Generate report for specific chronicle (by ID)",
        )
        parser.add_argument(
            "--output",
            type=str,
            help="Output filename for report",
        )

    def handle(self, *args, **options):
        # Determine scope
        if options["st_username"]:
            try:
                st_user = User.objects.get(username=options["st_username"])
                chronicles = Chronicle.objects.filter(storytellers=st_user)
                report_title = f"ST Report for {st_user.username}"
            except User.DoesNotExist:
                raise CommandError(f"User {options['st_username']} not found")
        elif options["chronicle"]:
            try:
                chronicles = [Chronicle.objects.get(pk=options["chronicle"])]
                report_title = f"ST Report for Chronicle: {chronicles[0].name}"
            except Chronicle.DoesNotExist:
                raise CommandError(f"Chronicle {options['chronicle']} not found")
        else:
            chronicles = Chronicle.objects.all()
            report_title = "ST Report - All Chronicles"

        # Generate report
        report = self.generate_report(report_title, chronicles)

        # Output
        if options["output"]:
            with open(options["output"], "w") as f:
                f.write(report)
            self.stdout.write(
                self.style.SUCCESS(f"\nReport saved to {options['output']}")
            )
        else:
            self.stdout.write(report)

    def generate_report(self, title, chronicles):
        """Generate the ST report."""
        from characters.models.core.character import CharacterModel

        output = []
        output.append("=" * 70)
        output.append(title.upper())
        output.append("=" * 70)
        output.append("")

        for chronicle in chronicles:
            output.append(f"\nCHRONICLE: {chronicle.name} (ID: {chronicle.id})")
            output.append("-" * 70)

            # Storytellers
            sts = chronicle.storytellers.all()
            st_names = ", ".join(st.username for st in sts) if sts.exists() else "None"
            output.append(f"Storytellers: {st_names}")
            output.append("")

            # Pending Approvals
            output.append("PENDING APPROVALS:")

            # Characters
            pending_chars = CharacterModel.objects.filter(
                chronicle=chronicle, status="Sub"
            ).count()
            output.append(f"  Submitted Characters: {pending_chars}")

            # Images
            pending_images = (
                CharacterModel.objects.filter(chronicle=chronicle, image_status="sub")
                .exclude(image="")
                .count()
            )
            output.append(f"  Pending Images: {pending_images}")

            # Freebies
            pending_freebies = CharacterModel.objects.filter(
                chronicle=chronicle, freebies_approved=False, status="Sub"
            ).count()
            output.append(f"  Pending Freebies: {pending_freebies}")

            # XP Requests
            char_ids = CharacterModel.objects.filter(chronicle=chronicle).values_list(
                "id", flat=True
            )
            pending_xp = WeeklyXPRequest.objects.filter(
                character_id__in=char_ids, approved=False
            ).count()
            output.append(f"  Pending XP Requests: {pending_xp}")
            output.append("")

            # Active Scenes
            output.append("ACTIVE SCENES:")
            active_scenes = Scene.objects.filter(chronicle=chronicle, finished=False)
            active_count = active_scenes.count()
            output.append(f"  Total: {active_count}")

            if active_count > 0:
                for scene in active_scenes[:5]:
                    char_count = scene.characters.count()
                    output.append(
                        f"    - {scene.name or '(unnamed)'}: {char_count} character(s)"
                    )
                if active_count > 5:
                    output.append(f"    ... and {active_count - 5} more")
            output.append("")

            # Character Status Breakdown
            output.append("CHARACTER STATUS:")
            all_chars = CharacterModel.objects.filter(chronicle=chronicle)

            status_counts = {
                "Approved": all_chars.filter(status="App").count(),
                "Submitted": all_chars.filter(status="Sub").count(),
                "Unfinished": all_chars.filter(status="Un").count(),
                "Retired": all_chars.filter(status="Ret").count(),
                "Deceased": all_chars.filter(status="Dec").count(),
            }

            for status, count in status_counts.items():
                output.append(f"  {status}: {count}")

            npc_count = all_chars.filter(npc=True).count()
            pc_count = all_chars.filter(npc=False).count()
            output.append(f"  PCs: {pc_count} | NPCs: {npc_count}")
            output.append("")

        output.append("=" * 70)
        output.append("")

        return "\n".join(output)
