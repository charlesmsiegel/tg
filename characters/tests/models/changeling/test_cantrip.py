"""Tests for Cantrip model."""

from characters.models.changeling.cantrip import Cantrip
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle


class TestCantripModel(TestCase):
    """Tests for the Cantrip model."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.cantrip = Cantrip.objects.create(
            name="Test Cantrip",
            art="wayfare",
            primary_realm="actor",
            level=1,
            difficulty=7,
            effect="Test effect",
        )

    def test_cantrip_type(self):
        """Test that Cantrip has correct type attribute."""
        self.assertEqual(self.cantrip.type, "cantrip")

    def test_cantrip_gameline(self):
        """Test that Cantrip has correct gameline."""
        self.assertEqual(self.cantrip.gameline, "ctd")

    def test_cantrip_str_with_art(self):
        """Test string representation with art and name."""
        self.assertEqual(str(self.cantrip), "Test Cantrip (Wayfare 1)")

    def test_cantrip_str_without_art(self):
        """Test string representation without art."""
        cantrip = Cantrip.objects.create(name="Nameless Cantrip")
        self.assertEqual(str(cantrip), "Nameless Cantrip")

    def test_cantrip_get_heading(self):
        """Test that get_heading returns correct heading class."""
        self.assertEqual(self.cantrip.get_heading(), "ctd_heading")

    def test_cantrip_art_choices(self):
        """Test that art field has correct choices."""
        arts = [
            "autumn",
            "chicanery",
            "chronos",
            "contract",
            "dragons_ire",
            "legerdemain",
            "metamorphosis",
            "naming",
            "oneiromancy",
            "primal",
            "pyretics",
            "skycraft",
            "soothsay",
            "sovereign",
            "spring",
            "summer",
            "wayfare",
            "winter",
        ]
        valid_choices = [choice[0] for choice in Cantrip._meta.get_field("art").choices]
        for art in arts:
            self.assertIn(art, valid_choices)

    def test_cantrip_realm_choices(self):
        """Test that primary_realm field has correct choices."""
        realms = ["actor", "fae", "nature", "prop", "time", "scene"]
        valid_choices = [choice[0] for choice in Cantrip._meta.get_field("primary_realm").choices]
        for realm in realms:
            self.assertIn(realm, valid_choices)

    def test_cantrip_level_choices(self):
        """Test that level field has correct choices (1-5)."""
        valid_choices = [choice[0] for choice in Cantrip._meta.get_field("level").choices]
        for level in range(1, 6):
            self.assertIn(level, valid_choices)

    def test_cantrip_modifier_realms_default(self):
        """Test that modifier_realms defaults to empty list."""
        cantrip = Cantrip.objects.create(name="No Modifiers")
        self.assertEqual(cantrip.modifier_realms, [])

    def test_cantrip_modifier_realms_with_values(self):
        """Test modifier_realms with values."""
        cantrip = Cantrip.objects.create(
            name="Modified Cantrip",
            modifier_realms=["scene", "time"],
        )
        self.assertIn("scene", cantrip.modifier_realms)
        self.assertIn("time", cantrip.modifier_realms)

    def test_cantrip_type_of_effect_choices(self):
        """Test type_of_effect field choices."""
        valid_choices = [choice[0] for choice in Cantrip._meta.get_field("type_of_effect").choices]
        self.assertIn("chimerical", valid_choices)
        self.assertIn("wyrd", valid_choices)
        self.assertIn("both", valid_choices)

    def test_cantrip_bunk_examples_default(self):
        """Test that bunk_examples defaults to empty list."""
        cantrip = Cantrip.objects.create(name="No Bunks")
        self.assertEqual(cantrip.bunk_examples, [])

    def test_cantrip_bunk_examples_with_values(self):
        """Test bunk_examples with values."""
        cantrip = Cantrip.objects.create(
            name="Bunked Cantrip",
            bunk_examples=["Dance a jig", "Whistle a tune", "Draw a circle"],
        )
        self.assertEqual(len(cantrip.bunk_examples), 3)
        self.assertIn("Dance a jig", cantrip.bunk_examples)

    def test_cantrip_difficulty_default(self):
        """Test that difficulty defaults to 8."""
        cantrip = Cantrip.objects.create(name="Default Difficulty")
        self.assertEqual(cantrip.difficulty, 8)

    def test_cantrip_duration_field(self):
        """Test duration field."""
        cantrip = Cantrip.objects.create(
            name="Duration Test",
            duration="Until sunrise",
        )
        self.assertEqual(cantrip.duration, "Until sunrise")

    def test_cantrip_range_field(self):
        """Test range field."""
        cantrip = Cantrip.objects.create(
            name="Range Test",
            range="Touch",
        )
        self.assertEqual(cantrip.range, "Touch")

    def test_cantrip_glamour_cost_field(self):
        """Test glamour_cost field."""
        cantrip = Cantrip.objects.create(
            name="Cost Test",
            glamour_cost="1 Wyrd",
        )
        self.assertEqual(cantrip.glamour_cost, "1 Wyrd")


class TestCantripDetailView(TestCase):
    """Tests for Cantrip detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.cantrip = Cantrip.objects.create(
            name="Test Cantrip",
            art="wayfare",
            primary_realm="actor",
            level=1,
        )
        self.url = self.cantrip.get_absolute_url()

    def test_cantrip_detail_view_status_code(self):
        """Test that detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_cantrip_detail_view_context(self):
        """Test that detail view contains cantrip object."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.context["object"], self.cantrip)


class TestCantripCreateView(TestCase):
    """Tests for Cantrip create view."""

    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.url = Cantrip.get_creation_url()

    def test_cantrip_create_view_status_code(self):
        """Test that create view returns 200."""
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_cantrip_create_view_successful_post(self):
        """Test successful cantrip creation."""
        self.client.login(username="ST", password="password")
        data = {
            "name": "New Cantrip",
            "art": "chicanery",
            "primary_realm": "fae",
            "level": 2,
            "difficulty": 7,
            "effect": "A test effect",
            "type_of_effect": "chimerical",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cantrip.objects.filter(name="New Cantrip").count(), 1)


class TestCantripUpdateView(TestCase):
    """Tests for Cantrip update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.cantrip = Cantrip.objects.create(
            name="Test Cantrip",
            art="wayfare",
            primary_realm="actor",
            level=1,
        )
        self.url = self.cantrip.get_update_url()

    def test_cantrip_update_view_status_code(self):
        """Test that update view returns 200."""
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_cantrip_update_view_successful_post(self):
        """Test successful cantrip update."""
        self.client.login(username="ST", password="password")
        data = {
            "name": "Updated Cantrip",
            "art": "wayfare",
            "primary_realm": "actor",
            "level": 3,
            "difficulty": 6,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.cantrip.refresh_from_db()
        self.assertEqual(self.cantrip.name, "Updated Cantrip")
        self.assertEqual(self.cantrip.level, 3)
