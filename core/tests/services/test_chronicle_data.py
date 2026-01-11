"""Tests for ChronicleDataService."""

from collections import OrderedDict
from datetime import date
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core import Human
from characters.models.vampire import Vampire
from core.services import ChronicleDataService
from game.models import Chronicle, Scene
from items.models.core import ItemModel
from items.models.mage import Wonder
from locations.models.core.location import LocationModel
from locations.models.mage import Node


class TestChronicleDataServiceConstants(TestCase):
    """Test ChronicleDataService class constants."""

    def test_gameline_order(self):
        """Test that GAMELINE_ORDER is derived from settings and excludes 'orp'."""
        # Should contain all gamelines from settings except 'orp'
        self.assertIn("wod", ChronicleDataService.GAMELINE_ORDER)
        self.assertIn("vtm", ChronicleDataService.GAMELINE_ORDER)
        self.assertIn("mta", ChronicleDataService.GAMELINE_ORDER)
        self.assertNotIn("orp", ChronicleDataService.GAMELINE_ORDER)

    def test_get_display_name(self):
        """Test that get_display_name returns proper tab labels."""
        self.assertEqual(ChronicleDataService.get_display_name("wod"), "All")
        self.assertEqual(ChronicleDataService.get_display_name("vtm"), "Vampire")
        self.assertEqual(ChronicleDataService.get_display_name("mta"), "Mage")
        self.assertEqual(ChronicleDataService.get_display_name("wta"), "Werewolf")


class TestChronicleDataServiceGroupByGameline(TestCase):
    """Tests for ChronicleDataService.group_by_gameline()."""

    def test_empty_queryset_returns_empty_dict(self):
        """Test that empty queryset returns empty OrderedDict."""
        # Use an actual empty queryset from the database
        from game.models import SettingElement

        empty_qs = SettingElement.objects.none()
        result = ChronicleDataService.group_by_gameline(empty_qs)

        self.assertIsInstance(result, OrderedDict)
        self.assertEqual(len(result), 0)

    def test_wod_shows_all_content(self):
        """Test that 'wod' entry contains all items."""
        mock_qs = MagicMock()
        mock_qs.exists.return_value = True
        mock_qs.filter.return_value.exists.return_value = False

        result = ChronicleDataService.group_by_gameline(mock_qs)

        self.assertIn("wod", result)
        self.assertEqual(result["wod"]["name"], "All")
        self.assertEqual(result["wod"]["items"], mock_qs)


class TestChronicleDataServiceGroupCharacters(TestCase):
    """Tests for ChronicleDataService.group_characters_by_gameline()."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_empty_queryset_returns_empty_dict(self):
        """Test that empty character queryset returns empty OrderedDict."""
        from characters.models.core.character import Character

        empty_qs = Character.objects.none()
        result = ChronicleDataService.group_characters_by_gameline(empty_qs)

        self.assertIsInstance(result, OrderedDict)
        self.assertEqual(len(result), 0)

    def test_characters_grouped_by_gameline(self):
        """Test that characters are grouped by their gameline model type."""
        from characters.models.core.character import Character

        # Create a Human (WoD base)
        human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            chronicle=self.chronicle,
        )

        # Create a Vampire (VtM)
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            chronicle=self.chronicle,
        )

        all_chars = Character.objects.filter(pk__in=[human.pk, vampire.pk])
        result = ChronicleDataService.group_characters_by_gameline(all_chars)

        # Should have "wod" (All) and "vtm" gamelines
        self.assertIn("wod", result)
        self.assertEqual(result["wod"]["name"], "All")
        # Vampire is in vtm gameline
        self.assertIn("vtm", result)
        self.assertEqual(result["vtm"]["name"], "Vampire")


class TestChronicleDataServiceGroupLocations(TestCase):
    """Tests for ChronicleDataService.group_locations_by_gameline()."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_empty_queryset_returns_empty_dict(self):
        """Test that empty location queryset returns empty OrderedDict."""
        empty_qs = LocationModel.objects.none()
        result = ChronicleDataService.group_locations_by_gameline(empty_qs)

        self.assertIsInstance(result, OrderedDict)
        self.assertEqual(len(result), 0)

    def test_generic_locations_in_all_tabs(self):
        """Test that generic locations (gameline='wod') appear in all tabs."""
        loc = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )

        all_locs = LocationModel.objects.filter(pk=loc.pk)
        result = ChronicleDataService.group_locations_by_gameline(all_locs)

        # Generic location should appear in "wod" (All) tab
        self.assertIn("wod", result)
        self.assertEqual(len(result["wod"]["locations"]), 1)
        # Generic locations also appear in gameline-specific tabs
        self.assertIn("vtm", result)
        self.assertIn(loc, result["vtm"]["locations"])

    def test_gameline_specific_locations(self):
        """Test that gameline-specific locations are grouped correctly."""
        # Create a Node (Mage location)
        node = Node.objects.create(
            name="Test Node",
            chronicle=self.chronicle,
            rank=1,
        )

        all_locs = LocationModel.objects.filter(pk=node.pk)
        result = ChronicleDataService.group_locations_by_gameline(all_locs)

        self.assertIn("wod", result)
        self.assertIn("mta", result)
        self.assertEqual(result["mta"]["name"], "Mage")


class TestChronicleDataServiceGroupItems(TestCase):
    """Tests for ChronicleDataService.group_items_by_gameline()."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_empty_queryset_returns_empty_dict(self):
        """Test that empty item queryset returns empty OrderedDict."""
        empty_qs = ItemModel.objects.none()
        result = ChronicleDataService.group_items_by_gameline(empty_qs)

        self.assertIsInstance(result, OrderedDict)
        self.assertEqual(len(result), 0)

    def test_items_grouped_by_gameline(self):
        """Test that items are grouped by their gameline model type."""
        # Create a Wonder (Mage item)
        wonder = Wonder.objects.create(
            name="Test Wonder",
            chronicle=self.chronicle,
            rank=1,
        )

        all_items = ItemModel.objects.filter(pk=wonder.pk)
        result = ChronicleDataService.group_items_by_gameline(all_items)

        self.assertIn("wod", result)
        self.assertIn("mta", result)
        self.assertEqual(result["mta"]["name"], "Mage")


class TestChronicleDataServiceGroupScenesByMonth(TestCase):
    """Tests for ChronicleDataService.group_scenes_by_month()."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )

    def test_empty_queryset_returns_empty_list(self):
        """Test that empty scene queryset returns empty list."""
        empty_qs = Scene.objects.none()
        result = ChronicleDataService.group_scenes_by_month(empty_qs)

        self.assertEqual(result, [])

    def test_scenes_grouped_by_month(self):
        """Test that scenes are grouped by year/month."""
        scene1 = Scene.objects.create(
            name="Scene 1",
            chronicle=self.chronicle,
            location=self.location,
            date_of_scene=date(2024, 1, 15),
        )
        scene2 = Scene.objects.create(
            name="Scene 2",
            chronicle=self.chronicle,
            location=self.location,
            date_of_scene=date(2024, 1, 20),
        )
        scene3 = Scene.objects.create(
            name="Scene 3",
            chronicle=self.chronicle,
            location=self.location,
            date_of_scene=date(2024, 2, 10),
        )

        all_scenes = Scene.objects.filter(pk__in=[scene1.pk, scene2.pk, scene3.pk]).order_by(
            "date_of_scene"
        )
        result = ChronicleDataService.group_scenes_by_month(all_scenes)

        # Should have 2 groups: January and February
        self.assertEqual(len(result), 2)
        # First group is January
        self.assertEqual(result[0][0].month, 1)
        self.assertEqual(len(result[0][1]), 2)
        # Second group is February
        self.assertEqual(result[1][0].month, 2)
        self.assertEqual(len(result[1][1]), 1)


class TestChronicleDataServiceGroupScenesByGameline(TestCase):
    """Tests for ChronicleDataService.group_scenes_by_gameline()."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )

    def test_empty_queryset_returns_empty_dict(self):
        """Test that empty scene queryset returns empty OrderedDict."""
        empty_qs = Scene.objects.none()
        result = ChronicleDataService.group_scenes_by_gameline(empty_qs)

        self.assertIsInstance(result, OrderedDict)
        self.assertEqual(len(result), 0)

    def test_scenes_grouped_by_gameline(self):
        """Test that scenes are grouped by gameline field."""
        scene_wod = Scene.objects.create(
            name="WoD Scene",
            chronicle=self.chronicle,
            location=self.location,
            gameline="wod",
            date_of_scene=date(2024, 1, 15),
        )
        scene_vtm = Scene.objects.create(
            name="VtM Scene",
            chronicle=self.chronicle,
            location=self.location,
            gameline="vtm",
            date_of_scene=date(2024, 1, 20),
        )

        all_scenes = Scene.objects.filter(pk__in=[scene_wod.pk, scene_vtm.pk])
        result = ChronicleDataService.group_scenes_by_gameline(all_scenes)

        self.assertIn("wod", result)
        self.assertEqual(result["wod"]["name"], "All")
        self.assertIn("vtm", result)
        self.assertEqual(result["vtm"]["name"], "Vampire")

    def test_scenes_include_month_grouping(self):
        """Test that scene gameline groups include scenes_by_month."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            gameline="mta",
            date_of_scene=date(2024, 1, 15),
        )

        all_scenes = Scene.objects.filter(pk=scene.pk)
        result = ChronicleDataService.group_scenes_by_gameline(all_scenes)

        self.assertIn("mta", result)
        self.assertIn("scenes_by_month", result["mta"])
        self.assertEqual(len(result["mta"]["scenes_by_month"]), 1)
