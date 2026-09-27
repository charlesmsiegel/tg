"""Specialty lookups for character sheets do not query once per stat."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.human import Human
from characters.models.core.specialty import Specialty

STATS = ["strength", "dexterity", "alertness", "athletics", "brawl", "firearms", "occult"]


class SpecialtyLookupTest(TestCase):
    def setUp(self):
        self.human = Human.objects.create(
            name="Sheet", owner=User.objects.create_user("owner", password="pw")
        )
        self.grip = Specialty.objects.create(name="Iron Grip", stat="strength")
        self.ears = Specialty.objects.create(name="Keen Ears", stat="alertness")
        self.human.specialties.add(self.grip, self.ears)
        self.human = Human.objects.get(pk=self.human.pk)

    def test_get_specialty_values(self):
        self.assertEqual(self.human.get_specialty("strength"), "Iron Grip")
        self.assertEqual(self.human.get_specialty("alertness"), "Keen Ears")
        self.assertIsNone(self.human.get_specialty("brawl"))

    def test_a_whole_sheet_of_lookups_costs_one_query(self):
        with self.assertNumQueries(1):
            for stat in STATS * 2:
                self.human.get_specialty(stat)

    def test_prefetched_specialties_cost_nothing(self):
        human = Human.objects.prefetch_related("specialties").get(pk=self.human.pk)
        with self.assertNumQueries(0):
            for stat in STATS:
                human.get_specialty(stat)

    def test_first_specialty_by_primary_key_wins(self):
        later = Specialty.objects.create(name="Bench Press", stat="strength")
        self.human.specialties.add(later)
        self.assertEqual(self.human.get_specialty("strength"), "Iron Grip")
        self.assertEqual(self.human.specialties_by_stat()["strength"], ["Iron Grip", "Bench Press"])

    def test_adding_or_removing_a_specialty_is_seen_immediately(self):
        self.assertIsNone(self.human.get_specialty("brawl"))
        self.human.specialties.add(Specialty.objects.create(name="Boxing", stat="brawl"))
        self.assertEqual(self.human.get_specialty("brawl"), "Boxing")
        self.human.specialties.remove(self.grip)
        self.assertIsNone(self.human.get_specialty("strength"))
