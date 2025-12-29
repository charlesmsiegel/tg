"""Tests for MageFaction model."""

from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Paradigm, Practice
from characters.models.mage.sphere import Sphere
from django.test import TestCase


class TestMageFaction(TestCase):
    """Tests for MageFaction model methods and properties."""

    def setUp(self):
        self.faction1 = MageFaction.objects.create(name="Faction 1")
        self.faction2 = MageFaction.objects.create(name="Faction 2", parent=self.faction1)
        self.faction3 = MageFaction.objects.create(name="Faction 3", parent=self.faction2)

        self.paradigm1 = Paradigm.objects.create(name="Paradigm 1")
        self.paradigm2 = Paradigm.objects.create(name="Paradigm 2")
        self.paradigm3 = Paradigm.objects.create(name="Paradigm 3")

        self.practice1 = Practice.objects.create(name="Practice 1")
        self.practice2 = Practice.objects.create(name="Practice 2")
        self.practice3 = Practice.objects.create(name="Practice 3")

        self.faction1.paradigms.add(self.paradigm1, self.paradigm2)
        self.faction2.paradigms.add(self.paradigm2, self.paradigm3)
        self.faction3.paradigms.add(self.paradigm1, self.paradigm3)

        self.faction1.practices.add(self.practice1, self.practice2)
        self.faction2.practices.add(self.practice2, self.practice3)
        self.faction3.practices.add(self.practice1, self.practice3)

    def test_affinities(self):
        faction = MageFaction.objects.create(name="Faction 1", parent=None)
        forces = Sphere.objects.create(name="Forces", property_name="forces")
        correspondence = Sphere.objects.create(
            name="Correspondence", property_name="correspondence"
        )
        faction.affinities.add(forces)
        faction.affinities.add(correspondence)
        self.assertEqual(faction.affinities.count(), 2)
        life = Sphere.objects.create(name="Life", property_name="life")
        faction.affinities.add(life)
        self.assertEqual(faction.affinities.count(), 3)

    def test_get_all_paradigms(self):
        expected_paradigms = Paradigm.objects.filter(id__in=[1, 2, 3])
        self.assertQuerySetEqual(
            self.faction3.get_all_paradigms(), expected_paradigms, ordered=False
        )

    def test_get_all_practices(self):
        expected_practices = Practice.objects.filter(id__in=[1, 2, 3])
        self.assertQuerySetEqual(
            self.faction3.get_all_practices(), expected_practices, ordered=False
        )

    def test_str(self):
        faction = MageFaction.objects.create(name="Faction 1", parent=None)
        self.assertEqual(str(faction), "Faction 1")
