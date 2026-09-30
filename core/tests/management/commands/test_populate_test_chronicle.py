"""Tests for the --gameline option of populate_test_chronicle."""

from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from characters.models.core.human import Human
from characters.models.mage.mtahuman import MtAHuman
from characters.models.vampire.vtmhuman import VtMHuman
from game.models import Chronicle


class PopulateTestChronicleGamelineTests(TestCase):
    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Sandbox")

    def populate(self, *args):
        call_command(
            "populate_test_chronicle",
            "--chronicle",
            str(self.chronicle.pk),
            "--characters",
            "3",
            "--scenes",
            "2",
            *args,
            stdout=StringIO(),
        )

    def test_default_creates_vampire_mortals(self):
        self.populate()
        self.assertEqual(VtMHuman.objects.filter(chronicle=self.chronicle).count(), 3)

    def test_gameline_selects_model(self):
        self.populate("--gameline", "mta")
        self.assertEqual(MtAHuman.objects.filter(chronicle=self.chronicle).count(), 3)
        self.assertFalse(VtMHuman.objects.filter(chronicle=self.chronicle).exists())

    def test_wod_creates_core_humans(self):
        self.populate("--gameline", "wod")
        humans = Human.objects.filter(chronicle=self.chronicle)
        self.assertEqual(humans.count(), 3)
        self.assertTrue(all(type(human) is Human for human in humans))

    def test_unknown_gameline_is_rejected(self):
        with self.assertRaises(CommandError):
            self.populate("--gameline", "xyz")
