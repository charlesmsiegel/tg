"""Tests for the XP checks of the validate_character_data management command."""

from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from characters.models.core.human import Human
from core.management.commands.validate_character_data import Command
from game.models import XPSpendingRequest


class ValidateCharacterDataXPTests(TestCase):
    def setUp(self):
        owner = User.objects.create_user("owner", password="x")
        self.character = Human.objects.create(name="Spender", owner=owner, xp=5)

    def run_command(self):
        out = StringIO()
        call_command("validate_character_data", stdout=out)
        return out.getvalue()

    def test_negative_xp_balance_is_reported(self):
        # Fresh databases forbid negative XP with a check constraint; databases created
        # before it can still hold such rows, so check the method on an unsaved value.
        command = Command()
        command.issues = {"xp_inconsistencies": []}
        self.character.xp = -3
        command.check_xp_consistency(self.character)
        [issue] = command.issues["xp_inconsistencies"]
        self.assertIn("negative XP balance: -3", issue["issue"])

    def test_many_pending_spends_are_reported(self):
        XPSpendingRequest.objects.bulk_create(
            XPSpendingRequest(
                character=self.character,
                trait_name="Alertness",
                trait_type="ability",
                trait_value=1,
                cost=1,
            )
            for _ in range(21)
        )
        output = self.run_command()
        self.assertIn("Pending Xp Spends: 1", output)
        self.assertIn("21 pending XP spends", output)

    def test_clean_character_passes(self):
        self.assertIn("passed validation", self.run_command())
