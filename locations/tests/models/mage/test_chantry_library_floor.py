"""Library-type chantries hold free Library dots that cost nothing."""

from django.test import TestCase

from characters.models.core.background_block import Background
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating


class TestChantryLibraryFloorCost(TestCase):
    def setUp(self):
        self.library_bg, _ = Background.objects.get_or_create(
            property_name="library", defaults={"name": "Library"}
        )

    def make(self, chantry_type, rating):
        chantry = Chantry.objects.create(name="Stacks", total_points=20, chantry_type=chantry_type)
        ChantryBackgroundRating.objects.create(chantry=chantry, bg=self.library_bg, rating=rating)
        return chantry

    def test_free_dots_only_for_library_type_library(self):
        chantry = Chantry(name="Stacks", chantry_type="library")
        self.assertEqual(chantry.free_dots("library"), Chantry.LIBRARY_TYPE_FREE_DOTS)
        self.assertEqual(chantry.free_dots("node"), 0)
        self.assertEqual(Chantry(name="War", chantry_type="war").free_dots("library"), 0)

    def test_library_type_pays_only_above_the_floor(self):
        self.assertEqual(self.make("library", 3).total_cost(), 0)
        self.assertEqual(self.make("library", 5).total_cost(), 4)

    def test_other_types_pay_every_library_dot(self):
        self.assertEqual(self.make("war", 3).total_cost(), 6)
        self.assertEqual(self.make(None, 3).points, 14)
