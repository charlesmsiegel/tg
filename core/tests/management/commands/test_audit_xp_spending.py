"""Tests for the --pending-days check of audit_xp_spending."""

from datetime import timedelta
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from characters.models.core.human import Human
from game.models import XPSpendingRequest


class AuditXPSpendingPendingDaysTests(TestCase):
    def setUp(self):
        owner = User.objects.create_user("owner", password="x")
        self.character = Human.objects.create(name="Waiting", owner=owner, status="App", xp=10)
        self.spend = XPSpendingRequest.objects.create(
            character=self.character,
            trait_name="Alertness",
            trait_type="ability",
            trait_value=1,
            cost=1,
        )

    def run_command(self, *args):
        out = StringIO()
        call_command("audit_xp_spending", *args, stdout=out)
        return out.getvalue()

    def age_spend(self, days):
        XPSpendingRequest.objects.filter(pk=self.spend.pk).update(
            created_at=timezone.now() - timedelta(days=days)
        )

    def test_old_pending_spend_is_flagged(self):
        self.age_spend(40)
        self.assertIn("1 pending spend(s) older than 30 days", self.run_command())

    def test_recent_pending_spend_is_not_flagged(self):
        self.age_spend(5)
        self.assertNotIn("older than", self.run_command())

    def test_threshold_follows_option(self):
        self.age_spend(5)
        self.assertIn("older than 3 days", self.run_command("--pending-days", "3"))
