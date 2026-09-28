"""Tests for discipline reference data."""

from django.test import TestCase

from characters.models.vampire.discipline import Discipline


class DisciplinePropertyNameTests(TestCase):
    def test_new_discipline_uses_its_name_as_character_field(self):
        discipline = Discipline.objects.create(name="Quietus")

        self.assertEqual(discipline.property_name, "quietus")
