"""WeeklyXPRequest: one request per week and character, and a locked XP award."""

from datetime import date
from unittest import mock

from django.db.models.query import QuerySet
from django.test import TestCase

from characters.models.core import Character
from characters.models.core.human import Human
from game.models import Week, WeeklyXPRequest


class WeeklyXPRequestTests(TestCase):
    def setUp(self):
        self.char = Human.objects.create(name="Claimant")
        self.week = Week.objects.create(end_date=date(2024, 1, 14))

    def test_approve_locks_the_character_and_adds_to_its_current_xp(self):
        xp_request = WeeklyXPRequest.objects.create(character=self.char, week=self.week)
        self.assertEqual(xp_request.character.xp, 0)  # cached before the award below
        Character.objects.filter(pk=self.char.pk).update(xp=5)  # e.g. a scene award meanwhile
        original = QuerySet.select_for_update
        with mock.patch.object(
            QuerySet, "select_for_update", autospec=True, side_effect=original
        ) as locks:
            self.assertEqual(xp_request.approve(), 1)
        locked = {call.args[0].model for call in locks.call_args_list}
        self.assertIn(Character, locked)
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, 6)
