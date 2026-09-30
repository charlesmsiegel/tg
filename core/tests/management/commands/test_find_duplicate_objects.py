"""Tests for the --delete-empty option of find_duplicate_objects."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from characters.models.core.human import Human
from game.models import Chronicle


class FindDuplicateObjectsDeleteEmptyTests(TestCase):
    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Chronicle")

    def delete_empty(self):
        call_command(
            "find_duplicate_objects", "--type", "character", "--delete-empty", stdout=StringIO()
        )

    def test_group_of_empty_members_keeps_the_oldest(self):
        first = Human.objects.create(name="Twin", chronicle=self.chronicle)
        Human.objects.create(name="Twin", chronicle=self.chronicle)
        self.delete_empty()
        self.assertEqual(list(Human.objects.filter(name="Twin")), [first])

    def test_empty_members_go_when_a_full_one_remains(self):
        full = Human.objects.create(name="Twin", chronicle=self.chronicle, description="Kept")
        Human.objects.create(name="Twin", chronicle=self.chronicle)
        self.delete_empty()
        self.assertEqual(list(Human.objects.filter(name="Twin")), [full])
