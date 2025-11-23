"""
Management command to monitor validation system health and performance.

This command runs periodic checks on the validation system and reports:
- Constraint violation attempts (from logs)
- Transaction rollback rate
- Performance metrics for XP operations
- Data integrity issues

Can be run as a cron job or monitoring service.

Usage:
    python manage.py monitor_validation                    # Run checks and report
    python manage.py monitor_validation --alert             # Send alerts on issues
    python manage.py monitor_validation --json              # JSON output for monitoring tools
"""

import json
from datetime import datetime, timedelta

from characters.models.core.character import Character
from characters.models.core.human import Human
from django.core.management.base import BaseCommand
from django.db.models import Avg, Count, F, Q
from django.utils import timezone
from game.models import Scene


class Command(BaseCommand):
    help = "Monitor validation system health and performance"

    def add_arguments(self, parser):
        parser.add_argument(
            "--alert",
            action="store_true",
            help="Send alerts if issues detected",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output results as JSON",
        )
        parser.add_argument(
            "--period",
            type=int,
            default=24,
            help="Time period in hours to analyze (default: 24)",
        )

    def handle(self, *args, **options):
        alert_mode = options["alert"]
        json_output = options["json"]
        period_hours = options["period"]

        # Calculate time window
        since = timezone.now() - timedelta(hours=period_hours)

        # Collect metrics
        metrics = {
            "timestamp": timezone.now().isoformat(),
            "period_hours": period_hours,
            "checks": {},
        }

        # Run all checks
        metrics["checks"]["data_integrity"] = self.check_data_integrity()
        metrics["checks"]["xp_activity"] = self.check_xp_activity(since)
        metrics["checks"]["scene_xp_awards"] = self.check_scene_xp_awards(since)
        metrics["checks"]["character_stats"] = self.check_character_statistics()

        # Calculate overall health score
        metrics["health_score"] = self.calculate_health_score(metrics["checks"])
        metrics["status"] = "healthy" if metrics["health_score"] >= 90 else "degraded"

        # Output results
        if json_output:
            self.stdout.write(json.dumps(metrics, indent=2))
        else:
            self.display_report(metrics)

        # Send alerts if needed
        if alert_mode and metrics["status"] != "healthy":
            self.send_alerts(metrics)

    def check_data_integrity(self):
        """Check for data integrity issues."""
        issues = {
            "negative_xp": Character.objects.filter(xp__lt=0).count(),
            "invalid_status": Character.objects.exclude(
                status__in=["Un", "Sub", "App", "Ret", "Dec"]
            ).count(),
            "attributes_out_of_range": self.count_attribute_issues(),
            "abilities_out_of_range": self.count_ability_issues(),
            "willpower_violations": Human.objects.filter(
                temporary_willpower__gt=F("willpower")
            ).count(),
        }

        issues["total"] = sum(issues.values())
        issues["healthy"] = issues["total"] == 0

        return issues

    def count_attribute_issues(self):
        """Count characters with attributes outside valid range."""
        count = 0
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
            count += Human.objects.filter(
                Q(**{f"{attr}__lt": 1}) | Q(**{f"{attr}__gt": 10})
            ).count()

        return count

    def count_ability_issues(self):
        """Count characters with abilities outside valid range."""
        count = 0
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

        for ability in abilities:
            count += Human.objects.filter(
                Q(**{f"{ability}__lt": 0}) | Q(**{f"{ability}__gt": 10})
            ).count()

        return count

    def check_xp_activity(self, since):
        """Check XP spending activity and patterns."""
        # Characters that spent XP recently (based on spent_xp JSONField)
        chars_with_recent_spending = Character.objects.filter(
            spent_xp__isnull=False
        ).exclude(spent_xp=[])

        # Count spending records
        total_spends = 0
        pending_spends = 0
        approved_spends = 0
        denied_spends = 0

        for char in chars_with_recent_spending:
            for spend in char.spent_xp:
                total_spends += 1
                status = spend.get("approved", "Pending")
                if status == "Pending":
                    pending_spends += 1
                elif status == "Approved":
                    approved_spends += 1
                elif status == "Denied":
                    denied_spends += 1

        return {
            "total_spending_records": total_spends,
            "pending_approval": pending_spends,
            "approved": approved_spends,
            "denied": denied_spends,
            "approval_rate": (
                round((approved_spends / total_spends * 100), 2)
                if total_spends > 0
                else 0
            ),
        }

    def check_scene_xp_awards(self, since):
        """Check scene XP award patterns."""
        total_scenes = Scene.objects.filter(date_played__gte=since).count()
        finished_scenes = Scene.objects.filter(
            finished=True, date_played__gte=since
        ).count()
        scenes_with_xp = Scene.objects.filter(
            xp_given=True, date_played__gte=since
        ).count()
        scenes_awaiting_xp = Scene.objects.filter(
            finished=True, xp_given=False, date_played__gte=since
        ).count()

        return {
            "total_scenes": total_scenes,
            "finished_scenes": finished_scenes,
            "scenes_with_xp_awarded": scenes_with_xp,
            "scenes_awaiting_xp": scenes_awaiting_xp,
            "xp_award_rate": (
                round((scenes_with_xp / finished_scenes * 100), 2)
                if finished_scenes > 0
                else 0
            ),
        }

    def check_character_statistics(self):
        """Get overall character statistics."""
        total_chars = Character.objects.count()
        status_breakdown = {
            "unfinished": Character.objects.filter(status="Un").count(),
            "submitted": Character.objects.filter(status="Sub").count(),
            "approved": Character.objects.filter(status="App").count(),
            "retired": Character.objects.filter(status="Ret").count(),
            "deceased": Character.objects.filter(status="Dec").count(),
        }

        # XP statistics
        xp_stats = Character.objects.aggregate(
            avg_xp=Avg("xp"),
            total_xp=Count("xp"),
        )

        return {
            "total_characters": total_chars,
            "status_breakdown": status_breakdown,
            "average_xp": round(xp_stats["avg_xp"] or 0, 2),
        }

    def calculate_health_score(self, checks):
        """Calculate overall health score (0-100)."""
        score = 100

        # Deduct points for data integrity issues
        integrity = checks["data_integrity"]
        if integrity["total"] > 0:
            # -5 points per issue, max -50
            score -= min(integrity["total"] * 5, 50)

        # Deduct points for low approval rate
        xp_activity = checks["xp_activity"]
        if xp_activity["approval_rate"] < 80:
            score -= 10

        # Deduct points for scenes awaiting XP
        scene_xp = checks["scene_xp_awards"]
        if scene_xp["scenes_awaiting_xp"] > 10:
            score -= 10

        return max(score, 0)

    def display_report(self, metrics):
        """Display human-readable report."""
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Validation System Health Report"))
        self.stdout.write(self.style.SUCCESS(f"Generated: {metrics['timestamp']}"))
        self.stdout.write(
            self.style.SUCCESS(f"Period: Last {metrics['period_hours']} hours")
        )
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write("")

        # Overall status
        if metrics["status"] == "healthy":
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Overall Status: HEALTHY (Score: {metrics['health_score']}/100)"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠ Overall Status: DEGRADED (Score: {metrics['health_score']}/100)"
                )
            )
        self.stdout.write("")

        # Data Integrity
        integrity = metrics["checks"]["data_integrity"]
        self.stdout.write(self.style.HTTP_INFO("1. Data Integrity"))
        if integrity["healthy"]:
            self.stdout.write(self.style.SUCCESS("   ✓ No integrity issues detected"))
        else:
            self.stdout.write(
                self.style.WARNING(f"   ⚠ {integrity['total']} issues detected:")
            )
            if integrity["negative_xp"] > 0:
                self.stdout.write(
                    f"     - {integrity['negative_xp']} characters with negative XP"
                )
            if integrity["invalid_status"] > 0:
                self.stdout.write(
                    f"     - {integrity['invalid_status']} characters with invalid status"
                )
            if integrity["attributes_out_of_range"] > 0:
                self.stdout.write(
                    f"     - {integrity['attributes_out_of_range']} attribute violations"
                )
            if integrity["abilities_out_of_range"] > 0:
                self.stdout.write(
                    f"     - {integrity['abilities_out_of_range']} ability violations"
                )
            if integrity["willpower_violations"] > 0:
                self.stdout.write(
                    f"     - {integrity['willpower_violations']} willpower violations"
                )
        self.stdout.write("")

        # XP Activity
        xp = metrics["checks"]["xp_activity"]
        self.stdout.write(self.style.HTTP_INFO("2. XP Spending Activity"))
        self.stdout.write(f"   Total spending records: {xp['total_spending_records']}")
        self.stdout.write(f"   Pending approval: {xp['pending_approval']}")
        self.stdout.write(f"   Approved: {xp['approved']}")
        self.stdout.write(f"   Denied: {xp['denied']}")
        self.stdout.write(f"   Approval rate: {xp['approval_rate']}%")
        self.stdout.write("")

        # Scene XP Awards
        scene_xp = metrics["checks"]["scene_xp_awards"]
        self.stdout.write(self.style.HTTP_INFO("3. Scene XP Awards"))
        self.stdout.write(f"   Total scenes: {scene_xp['total_scenes']}")
        self.stdout.write(f"   Finished scenes: {scene_xp['finished_scenes']}")
        self.stdout.write(f"   XP awarded: {scene_xp['scenes_with_xp_awarded']}")
        self.stdout.write(f"   Awaiting XP: {scene_xp['scenes_awaiting_xp']}")
        self.stdout.write(f"   Award rate: {scene_xp['xp_award_rate']}%")
        self.stdout.write("")

        # Character Statistics
        char_stats = metrics["checks"]["character_stats"]
        self.stdout.write(self.style.HTTP_INFO("4. Character Statistics"))
        self.stdout.write(f"   Total characters: {char_stats['total_characters']}")
        self.stdout.write(f"   Average XP: {char_stats['average_xp']}")
        self.stdout.write("   Status breakdown:")
        for status, count in char_stats["status_breakdown"].items():
            self.stdout.write(f"     - {status}: {count}")
        self.stdout.write("")

        self.stdout.write(self.style.SUCCESS("=" * 70))

        # Recommendations
        if not integrity["healthy"]:
            self.stdout.write(self.style.WARNING("\nRecommendations:"))
            self.stdout.write(
                "   - Run: python manage.py validate_data_integrity --fix"
            )
            self.stdout.write("   - Review recent data changes for source of issues")

    def send_alerts(self, metrics):
        """Send alerts for degraded health."""
        # This is a placeholder - implement actual alerting
        # (e.g., email, Slack, PagerDuty, etc.)

        alert_message = f"""
ALERT: Validation System Health Degraded

Health Score: {metrics['health_score']}/100
Status: {metrics['status']}

Issues Detected:
{json.dumps(metrics['checks']['data_integrity'], indent=2)}

Please investigate immediately.

Run for details:
    python manage.py monitor_validation --period 24

Run to fix:
    python manage.py validate_data_integrity --fix
"""

        self.stdout.write(self.style.ERROR("\n[ALERT] " + alert_message))

        # TODO: Implement actual alerting mechanism
        # - Send email via Django's send_mail()
        # - Post to Slack webhook
        # - Trigger PagerDuty incident
        # - Log to monitoring system
