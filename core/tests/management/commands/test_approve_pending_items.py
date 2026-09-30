"""Tests for the approve_pending_items management command."""

from datetime import date
from io import StringIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from characters.models.core.human import Human
from game.models import Chronicle, Week, WeeklyXPRequest


class ApprovePendingItemsTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("staff", password="x", is_staff=True)
        self.player = User.objects.create_user("player", password="x")
        self.chronicle = Chronicle.objects.create(name="Scoped")
        self.other_chronicle = Chronicle.objects.create(name="Other")
        self.pc = Human.objects.create(
            name="Submitted PC", owner=self.player, chronicle=self.chronicle, status="Sub"
        )
        self.other_pc = Human.objects.create(
            name="Elsewhere", owner=self.player, chronicle=self.other_chronicle, status="Sub"
        )

    def run_command(self, *args):
        out = StringIO()
        call_command("approve_pending_items", *args, stdout=out)
        return out.getvalue()

    def test_write_without_scope_is_refused(self):
        with self.assertRaises(CommandError):
            self.run_command("--approver", "staff", "--noinput")
        self.pc.refresh_from_db()
        self.assertEqual(self.pc.status, "Sub")

    def test_write_without_approver_is_refused(self):
        with self.assertRaises(CommandError):
            self.run_command("--all", "--noinput")
        self.pc.refresh_from_db()
        self.assertEqual(self.pc.status, "Sub")

    def test_unknown_owner_is_an_error(self):
        with self.assertRaises(CommandError):
            self.run_command("--owner", "nobody", "--list-only")

    def test_list_only_needs_no_scope_and_changes_nothing(self):
        output = self.run_command("--list-only")
        self.assertIn("Submitted PC", output)
        self.pc.refresh_from_db()
        self.assertEqual(self.pc.status, "Sub")

    def test_chronicle_scope_approves_only_that_chronicle(self):
        self.run_command(
            "--type",
            "characters",
            "--chronicle",
            str(self.chronicle.pk),
            "--approver",
            "staff",
            "--noinput",
        )
        self.pc.refresh_from_db()
        self.other_pc.refresh_from_db()
        self.assertEqual(self.pc.status, "App")
        self.assertEqual(self.other_pc.status, "Sub")

    def test_approver_without_permission_is_skipped(self):
        output = self.run_command(
            "--type", "characters", "--all", "--approver", "player", "--noinput"
        )
        self.pc.refresh_from_db()
        self.assertEqual(self.pc.status, "Sub")
        self.assertIn("Skipped: 2", output)

    def test_confirmation_declined_changes_nothing(self):
        with patch("builtins.input", return_value="n"):
            output = self.run_command("--type", "characters", "--all", "--approver", "staff")
        self.pc.refresh_from_db()
        self.assertEqual(self.pc.status, "Sub")
        self.assertIn("cancelled", output)

    def test_confirmation_accepted_approves(self):
        with patch("builtins.input", return_value="y"):
            self.run_command("--type", "characters", "--all", "--approver", "staff")
        self.pc.refresh_from_db()
        self.assertEqual(self.pc.status, "App")

    def test_freebies_are_approved_without_award(self):
        self.pc.freebies = 15
        self.pc.save()
        self.run_command(
            "--type",
            "freebies",
            "--chronicle",
            str(self.chronicle.pk),
            "--approver",
            "staff",
            "--noinput",
        )
        self.pc.refresh_from_db()
        self.assertTrue(self.pc.freebies_approved)
        self.assertEqual(self.pc.freebies, 15)

    def test_weekly_xp_request_is_approved_and_xp_awarded(self):
        week = Week.objects.create(end_date=date(2026, 9, 27))
        request = WeeklyXPRequest.objects.create(week=week, character=self.pc, finishing=True)
        xp_before = self.pc.xp
        self.run_command(
            "--type", "xp-requests", "--owner", "player", "--approver", "staff", "--noinput"
        )
        request.refresh_from_db()
        self.pc.refresh_from_db()
        self.assertTrue(request.approved)
        self.assertEqual(self.pc.xp, xp_before + 1)

    def test_xp_spends_type_is_gone(self):
        with self.assertRaises(CommandError):
            self.run_command("--type", "xp-spends", "--list-only")
