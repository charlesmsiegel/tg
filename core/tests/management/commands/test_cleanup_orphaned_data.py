"""Tests for the cleanup_orphaned_data management command."""

from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from characters.models.core.human import Human
from game.models import Chronicle
from items.models.core.meleeweapon import MeleeWeapon


class CleanupOrphanedDataTests(TestCase):
    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Chronicle")
        # Reference data: loaded by populate_gamedata with no owner, status Un, no chronicle.
        self.reference = MeleeWeapon.objects.create(name="Knife")
        self.draft = Human.objects.create(name="Abandoned", chronicle=self.chronicle)
        self.owned = Human.objects.create(
            name="Owned", owner=User.objects.create_user("p"), chronicle=self.chronicle
        )

    def run_command(self, *args):
        out = StringIO()
        call_command("cleanup_orphaned_data", *args, stdout=out)
        return out.getvalue()

    def test_default_run_keeps_unowned_objects(self):
        self.run_command()
        self.assertTrue(Human.objects.filter(pk=self.draft.pk).exists())
        self.assertTrue(MeleeWeapon.objects.filter(pk=self.reference.pk).exists())

    def test_unowned_drafts_option_never_deletes_reference_data(self):
        self.run_command("--include-unowned-drafts")
        self.assertFalse(Human.objects.filter(pk=self.draft.pk).exists())
        self.assertTrue(Human.objects.filter(pk=self.owned.pk).exists())
        self.assertTrue(MeleeWeapon.objects.filter(pk=self.reference.pk).exists())

    def test_dry_run_deletes_nothing(self):
        output = self.run_command("--include-unowned-drafts", "--dry-run")
        self.assertIn("Abandoned", output)
        self.assertTrue(Human.objects.filter(pk=self.draft.pk).exists())

    def test_days_option_is_gone(self):
        with self.assertRaises(CommandError):
            self.run_command("--days", "30")
