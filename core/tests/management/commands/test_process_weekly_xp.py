"""Tests for the process_weekly_xp management command."""

from datetime import date, datetime
from io import StringIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.utils.timezone import make_aware

from accounts.dashboard import ProfileDashboard
from characters.models.core.human import Human
from core.management.commands.process_weekly_xp import most_recent_sunday
from game.models import Post, Scene, Week, WeeklyXPRequest

WEEK_ENDING = date(2026, 9, 27)  # a Sunday


class ProcessWeeklyXPTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("staff", password="x", is_staff=True)
        player = User.objects.create_user("player", password="x")
        self.character = Human.objects.create(name="Player Character", owner=player)
        scene = Scene.objects.create(name="Played", finished=True)
        scene.characters.add(self.character)
        Post.objects.create(
            scene=scene,
            character=self.character,
            display_name="Player Character",
            message="Done.",
            datetime_created=make_aware(datetime(2026, 9, 25, 20, 0)),
        )

    def run_command(self, *args):
        out = StringIO()
        call_command(
            "process_weekly_xp", "--week-ending", WEEK_ENDING.isoformat(), *args, stdout=out
        )
        return out.getvalue()

    def test_new_week_records_its_characters(self):
        self.run_command()
        week = Week.objects.get(end_date=WEEK_ENDING)
        self.assertEqual(list(week.characters.all()), [self.character])

    def test_created_request_reaches_the_storyteller_queue(self):
        self.run_command()
        week = Week.objects.get(end_date=WEEK_ENDING)
        queue = ProfileDashboard(self.staff.profile).get_unfulfilled_weekly_xp_requests_to_approve()
        self.assertEqual(queue, [(self.character, week)])

    def test_existing_week_gains_missing_characters(self):
        week = Week.objects.create(end_date=WEEK_ENDING)
        self.run_command()
        self.assertEqual(list(week.characters.all()), [self.character])
        self.assertTrue(WeeklyXPRequest.objects.filter(week=week, character=self.character))

    def test_auto_approve_awards_xp_through_the_request(self):
        xp_before = self.character.xp
        self.run_command("--auto-approve")
        request = WeeklyXPRequest.objects.get(character=self.character)
        self.character.refresh_from_db()
        self.assertTrue(request.approved)
        self.assertEqual(self.character.xp, xp_before + 1)

    def test_dry_run_writes_nothing(self):
        output = self.run_command("--dry-run")
        self.assertIn("Would create XP request for Player Character", output)
        self.assertFalse(Week.objects.exists())
        self.assertFalse(WeeklyXPRequest.objects.exists())

    def test_rerun_skips_existing_requests(self):
        self.run_command()
        output = self.run_command()
        self.assertEqual(WeeklyXPRequest.objects.count(), 1)
        self.assertIn("Request already exists", output)

    def test_notify_says_nothing_is_sent(self):
        self.assertIn("no notification is sent", self.run_command("--notify"))


class DefaultWeekEndingTests(TestCase):
    def test_most_recent_sunday(self):
        self.assertEqual(most_recent_sunday(date(2026, 9, 27)), date(2026, 9, 27))
        self.assertEqual(most_recent_sunday(date(2026, 9, 30)), date(2026, 9, 27))
        self.assertEqual(most_recent_sunday(date(2026, 10, 3)), date(2026, 9, 27))

    def test_default_is_the_most_recent_sunday(self):
        today = make_aware(datetime(2026, 9, 30, 12, 0))
        with patch("core.management.commands.process_weekly_xp.now", return_value=today):
            call_command("process_weekly_xp", stdout=StringIO())
        self.assertTrue(Week.objects.filter(end_date=date(2026, 9, 27)).exists())
