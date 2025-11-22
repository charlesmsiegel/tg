"""
Management command to generate comprehensive chronicle statistics and summary.

Generates:
- Scene statistics
- Character participation rates
- XP awarded
- Story arcs
- Player engagement metrics
"""
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q, Sum
from game.models import Chronicle, Scene


class Command(BaseCommand):
    help = "Generate comprehensive chronicle summary and statistics"

    def add_arguments(self, parser):
        parser.add_argument(
            "chronicle_id",
            type=int,
            help="ID of the chronicle to summarize",
        )
        parser.add_argument(
            "--output",
            type=str,
            help="Output filename for HTML report",
        )
        parser.add_argument(
            "--format",
            type=str,
            choices=["text", "html", "markdown"],
            default="text",
            help="Output format (default: text)",
        )

    def handle(self, *args, **options):
        chronicle_id = options["chronicle_id"]

        # Get chronicle
        try:
            self.chronicle = Chronicle.objects.get(pk=chronicle_id)
        except Chronicle.DoesNotExist:
            raise CommandError(f"Chronicle with ID {chronicle_id} does not exist")

        # Gather statistics
        stats = self.gather_statistics()

        # Format output
        output_format = options["format"]

        if output_format == "text":
            output = self.format_text(stats)
        elif output_format == "html":
            output = self.format_html(stats)
        elif output_format == "markdown":
            output = self.format_markdown(stats)

        # Display or save
        if options["output"]:
            with open(options["output"], "w") as f:
                f.write(output)
            self.stdout.write(
                self.style.SUCCESS(f"\nReport saved to {options['output']}")
            )
        else:
            self.stdout.write(output)

    def gather_statistics(self):
        """Gather comprehensive chronicle statistics."""
        from characters.models.core.character import CharacterModel
        from game.models import WeeklyXPRequest

        stats = {
            "chronicle": self.chronicle,
            "storytellers": list(self.chronicle.storytellers.all()),
            "scenes": {},
            "characters": {},
            "xp": {},
            "engagement": {},
        }

        # Scene statistics
        all_scenes = Scene.objects.filter(chronicle=self.chronicle)
        stats["scenes"]["total"] = all_scenes.count()
        stats["scenes"]["finished"] = all_scenes.filter(finished=True).count()
        stats["scenes"]["active"] = all_scenes.filter(finished=False).count()
        stats["scenes"]["with_xp"] = all_scenes.filter(xp_given=True).count()

        # Character statistics
        all_chars = CharacterModel.objects.filter(chronicle=self.chronicle)
        stats["characters"]["total"] = all_chars.count()
        stats["characters"]["approved"] = all_chars.filter(status="App").count()
        stats["characters"]["submitted"] = all_chars.filter(status="Sub").count()
        stats["characters"]["unfinished"] = all_chars.filter(status="Un").count()
        stats["characters"]["retired"] = all_chars.filter(status="Ret").count()
        stats["characters"]["deceased"] = all_chars.filter(status="Dec").count()
        stats["characters"]["npc"] = all_chars.filter(npc=True).count()
        stats["characters"]["pc"] = all_chars.filter(npc=False).count()

        # XP statistics
        approved_chars = all_chars.filter(status="App")
        if approved_chars.exists():
            total_xp = sum(char.xp for char in approved_chars if hasattr(char, "xp"))
            stats["xp"]["total_awarded"] = total_xp
            stats["xp"]["average_per_character"] = (
                total_xp / approved_chars.count() if approved_chars.count() > 0 else 0
            )

            # Count pending XP requests
            char_ids = approved_chars.values_list("id", flat=True)
            pending_requests = WeeklyXPRequest.objects.filter(
                character_id__in=char_ids, approved=False
            ).count()
            stats["xp"]["pending_requests"] = pending_requests
        else:
            stats["xp"]["total_awarded"] = 0
            stats["xp"]["average_per_character"] = 0
            stats["xp"]["pending_requests"] = 0

        # Player engagement
        # Count unique players (character owners)
        unique_players = (
            all_chars.filter(npc=False)
            .exclude(owner__isnull=True)
            .values("owner")
            .distinct()
            .count()
        )
        stats["engagement"]["unique_players"] = unique_players

        # Character participation in scenes
        chars_in_scenes = all_chars.filter(npc=False, scenes__isnull=False).distinct()
        stats["engagement"]["characters_with_scenes"] = chars_in_scenes.count()

        # Most active characters
        active_chars = (
            all_chars.filter(npc=False)
            .annotate(scene_count=Count("scenes"))
            .filter(scene_count__gt=0)
            .order_by("-scene_count")[:5]
        )

        stats["engagement"]["top_characters"] = [
            {
                "name": char.name,
                "owner": char.owner.username if char.owner else "Unknown",
                "scene_count": char.scene_count,
            }
            for char in active_chars
        ]

        return stats

    def format_text(self, stats):
        """Format statistics as plain text."""
        output = []
        output.append("=" * 70)
        output.append(f"CHRONICLE SUMMARY: {stats['chronicle'].name}")
        output.append("=" * 70)
        output.append("")

        # Basic info
        output.append("CHRONICLE INFORMATION")
        output.append("-" * 70)
        output.append(
            f"Storytellers: {', '.join(st.username for st in stats['storytellers']) or 'None'}"
        )
        output.append(f"Theme: {stats['chronicle'].theme or 'Not set'}")
        output.append(f"Mood: {stats['chronicle'].mood or 'Not set'}")
        output.append(f"Year: {stats['chronicle'].year}")
        output.append("")

        # Scene statistics
        output.append("SCENE STATISTICS")
        output.append("-" * 70)
        output.append(f"Total Scenes: {stats['scenes']['total']}")
        output.append(f"  Finished: {stats['scenes']['finished']}")
        output.append(f"  Active: {stats['scenes']['active']}")
        output.append(f"  XP Given: {stats['scenes']['with_xp']}")
        output.append("")

        # Character statistics
        output.append("CHARACTER STATISTICS")
        output.append("-" * 70)
        output.append(f"Total Characters: {stats['characters']['total']}")
        output.append(f"  Player Characters: {stats['characters']['pc']}")
        output.append(f"  NPCs: {stats['characters']['npc']}")
        output.append(f"  Approved: {stats['characters']['approved']}")
        output.append(f"  Submitted: {stats['characters']['submitted']}")
        output.append(f"  Unfinished: {stats['characters']['unfinished']}")
        output.append(f"  Retired: {stats['characters']['retired']}")
        output.append(f"  Deceased: {stats['characters']['deceased']}")
        output.append("")

        # XP statistics
        output.append("XP STATISTICS")
        output.append("-" * 70)
        output.append(f"Total XP Awarded: {stats['xp']['total_awarded']}")
        output.append(
            f"Average XP per Character: {stats['xp']['average_per_character']:.1f}"
        )
        output.append(f"Pending XP Requests: {stats['xp']['pending_requests']}")
        output.append("")

        # Engagement statistics
        output.append("PLAYER ENGAGEMENT")
        output.append("-" * 70)
        output.append(f"Unique Players: {stats['engagement']['unique_players']}")
        output.append(
            f"Characters with Scenes: {stats['engagement']['characters_with_scenes']}"
        )
        output.append("")

        if stats["engagement"]["top_characters"]:
            output.append("Top 5 Most Active Characters:")
            for char in stats["engagement"]["top_characters"]:
                output.append(
                    f"  - {char['name']} ({char['owner']}): {char['scene_count']} scenes"
                )
        else:
            output.append("No character activity recorded")

        output.append("")
        output.append("=" * 70)

        return "\n".join(output)

    def format_markdown(self, stats):
        """Format statistics as Markdown."""
        output = []
        output.append(f"# Chronicle Summary: {stats['chronicle'].name}")
        output.append("")

        # Basic info
        output.append("## Chronicle Information")
        output.append("")
        output.append(
            f"**Storytellers:** {', '.join(st.username for st in stats['storytellers']) or 'None'}"
        )
        output.append(f"**Theme:** {stats['chronicle'].theme or 'Not set'}")
        output.append(f"**Mood:** {stats['chronicle'].mood or 'Not set'}")
        output.append(f"**Year:** {stats['chronicle'].year}")
        output.append("")

        # Scene statistics
        output.append("## Scene Statistics")
        output.append("")
        output.append(f"- **Total Scenes:** {stats['scenes']['total']}")
        output.append(f"  - Finished: {stats['scenes']['finished']}")
        output.append(f"  - Active: {stats['scenes']['active']}")
        output.append(f"  - XP Given: {stats['scenes']['with_xp']}")
        output.append("")

        # Character statistics
        output.append("## Character Statistics")
        output.append("")
        output.append(f"- **Total Characters:** {stats['characters']['total']}")
        output.append(f"  - Player Characters: {stats['characters']['pc']}")
        output.append(f"  - NPCs: {stats['characters']['npc']}")
        output.append(f"  - Approved: {stats['characters']['approved']}")
        output.append(f"  - Submitted: {stats['characters']['submitted']}")
        output.append(f"  - Unfinished: {stats['characters']['unfinished']}")
        output.append(f"  - Retired: {stats['characters']['retired']}")
        output.append(f"  - Deceased: {stats['characters']['deceased']}")
        output.append("")

        # XP statistics
        output.append("## XP Statistics")
        output.append("")
        output.append(f"- **Total XP Awarded:** {stats['xp']['total_awarded']}")
        output.append(
            f"- **Average XP per Character:** {stats['xp']['average_per_character']:.1f}"
        )
        output.append(f"- **Pending XP Requests:** {stats['xp']['pending_requests']}")
        output.append("")

        # Engagement statistics
        output.append("## Player Engagement")
        output.append("")
        output.append(f"- **Unique Players:** {stats['engagement']['unique_players']}")
        output.append(
            f"- **Characters with Scenes:** {stats['engagement']['characters_with_scenes']}"
        )
        output.append("")

        if stats["engagement"]["top_characters"]:
            output.append("### Top 5 Most Active Characters")
            output.append("")
            for char in stats["engagement"]["top_characters"]:
                output.append(
                    f"- **{char['name']}** ({char['owner']}): {char['scene_count']} scenes"
                )
        else:
            output.append("No character activity recorded")

        output.append("")

        return "\n".join(output)

    def format_html(self, stats):
        """Format statistics as HTML."""
        # Simple HTML template
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Chronicle Summary: {stats['chronicle'].name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; border-bottom: 2px solid #ccc; padding-bottom: 5px; }}
        .stat {{ margin: 10px 0; }}
        .stat-label {{ font-weight: bold; }}
        .subsection {{ margin-left: 20px; }}
    </style>
</head>
<body>
    <h1>Chronicle Summary: {stats['chronicle'].name}</h1>

    <h2>Chronicle Information</h2>
    <div class="stat"><span class="stat-label">Storytellers:</span> {', '.join(st.username for st in stats['storytellers']) or 'None'}</div>
    <div class="stat"><span class="stat-label">Theme:</span> {stats['chronicle'].theme or 'Not set'}</div>
    <div class="stat"><span class="stat-label">Mood:</span> {stats['chronicle'].mood or 'Not set'}</div>
    <div class="stat"><span class="stat-label">Year:</span> {stats['chronicle'].year}</div>

    <h2>Scene Statistics</h2>
    <div class="stat"><span class="stat-label">Total Scenes:</span> {stats['scenes']['total']}</div>
    <div class="subsection">
        <div>Finished: {stats['scenes']['finished']}</div>
        <div>Active: {stats['scenes']['active']}</div>
        <div>XP Given: {stats['scenes']['with_xp']}</div>
    </div>

    <h2>Character Statistics</h2>
    <div class="stat"><span class="stat-label">Total Characters:</span> {stats['characters']['total']}</div>
    <div class="subsection">
        <div>Player Characters: {stats['characters']['pc']}</div>
        <div>NPCs: {stats['characters']['npc']}</div>
        <div>Approved: {stats['characters']['approved']}</div>
        <div>Submitted: {stats['characters']['submitted']}</div>
        <div>Unfinished: {stats['characters']['unfinished']}</div>
        <div>Retired: {stats['characters']['retired']}</div>
        <div>Deceased: {stats['characters']['deceased']}</div>
    </div>

    <h2>XP Statistics</h2>
    <div class="stat"><span class="stat-label">Total XP Awarded:</span> {stats['xp']['total_awarded']}</div>
    <div class="stat"><span class="stat-label">Average XP per Character:</span> {stats['xp']['average_per_character']:.1f}</div>
    <div class="stat"><span class="stat-label">Pending XP Requests:</span> {stats['xp']['pending_requests']}</div>

    <h2>Player Engagement</h2>
    <div class="stat"><span class="stat-label">Unique Players:</span> {stats['engagement']['unique_players']}</div>
    <div class="stat"><span class="stat-label">Characters with Scenes:</span> {stats['engagement']['characters_with_scenes']}</div>
"""

        if stats["engagement"]["top_characters"]:
            html += """
    <h3>Top 5 Most Active Characters</h3>
    <ul>
"""
            for char in stats["engagement"]["top_characters"]:
                html += f"""        <li><strong>{char['name']}</strong> ({char['owner']}): {char['scene_count']} scenes</li>
"""
            html += """    </ul>
"""

        html += """</body>
</html>"""

        return html
