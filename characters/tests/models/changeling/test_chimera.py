"""Tests for Chimera model."""

from characters.models.changeling.chimera import Chimera
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle


class TestChimeraModel(TestCase):
    """Tests for the Chimera model."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.chimera = Chimera.objects.create(
            name="Test Chimera",
            chimera_type="simple_crafted",
            chimera_points=10,
            sentience_level="semi_sentient",
        )

    def test_chimera_type(self):
        """Test that Chimera has correct type attribute."""
        self.assertEqual(self.chimera.type, "chimera")

    def test_chimera_gameline(self):
        """Test that Chimera has correct gameline."""
        self.assertEqual(self.chimera.gameline, "ctd")

    def test_chimera_str_with_type(self):
        """Test string representation with chimera_type."""
        self.assertEqual(str(self.chimera), "Test Chimera (Simple Crafted)")

    def test_chimera_str_without_type(self):
        """Test string representation without chimera_type."""
        chimera = Chimera.objects.create(name="Plain Chimera")
        self.assertEqual(str(chimera), "Plain Chimera")

    def test_chimera_get_heading(self):
        """Test that get_heading returns correct heading class."""
        self.assertEqual(self.chimera.get_heading(), "ctd_heading")

    def test_chimera_type_choices(self):
        """Test that chimera_type field has correct choices."""
        types = ["facsimile", "simple_crafted", "advanced_crafted", "complex_crafted", "master_crafted"]
        valid_choices = [choice[0] for choice in Chimera._meta.get_field("chimera_type").choices]
        for t in types:
            self.assertIn(t, valid_choices)

    def test_chimera_sentience_choices(self):
        """Test that sentience_level field has correct choices."""
        levels = ["non_sentient", "semi_sentient", "sentient", "fully_sentient"]
        valid_choices = [choice[0] for choice in Chimera._meta.get_field("sentience_level").choices]
        for level in levels:
            self.assertIn(level, valid_choices)

    def test_chimera_origin_choices(self):
        """Test that origin field has correct choices."""
        origins = ["manifested_dream", "treasure_bound", "created_art", "other"]
        valid_choices = [choice[0] for choice in Chimera._meta.get_field("origin").choices]
        for origin in origins:
            self.assertIn(origin, valid_choices)

    def test_chimera_points_default(self):
        """Test that chimera_points defaults to 5."""
        chimera = Chimera.objects.create(name="Default Points")
        self.assertEqual(chimera.chimera_points, 5)

    def test_chimera_points_custom(self):
        """Test setting custom chimera points."""
        chimera = Chimera.objects.create(name="High Points", chimera_points=30)
        self.assertEqual(chimera.chimera_points, 30)

    def test_chimera_sentience_default(self):
        """Test that sentience_level defaults to non_sentient."""
        chimera = Chimera.objects.create(name="Default Sentience")
        self.assertEqual(chimera.sentience_level, "non_sentient")

    def test_chimera_durability_default(self):
        """Test that durability defaults to 1."""
        chimera = Chimera.objects.create(name="Default Durability")
        self.assertEqual(chimera.durability, 1)

    def test_chimera_durability_custom(self):
        """Test setting custom durability."""
        chimera = Chimera.objects.create(name="Durable", durability=4)
        self.assertEqual(chimera.durability, 4)

    def test_chimera_loyalty_default(self):
        """Test that loyalty defaults to 0."""
        chimera = Chimera.objects.create(name="Default Loyalty")
        self.assertEqual(chimera.loyalty, 0)

    def test_chimera_loyalty_custom(self):
        """Test setting custom loyalty."""
        chimera = Chimera.objects.create(name="Loyal", loyalty=5)
        self.assertEqual(chimera.loyalty, 5)

    def test_chimera_special_abilities_default(self):
        """Test that special_abilities defaults to empty list."""
        chimera = Chimera.objects.create(name="No Abilities")
        self.assertEqual(chimera.special_abilities, [])

    def test_chimera_special_abilities_with_values(self):
        """Test special_abilities with values."""
        chimera = Chimera.objects.create(
            name="Special Chimera",
            special_abilities=["Flight", "Invisibility", "Telepathy"],
        )
        self.assertEqual(len(chimera.special_abilities), 3)
        self.assertIn("Flight", chimera.special_abilities)

    def test_chimera_can_interact_with_physical_default(self):
        """Test that can_interact_with_physical defaults to False."""
        chimera = Chimera.objects.create(name="Non-Physical")
        self.assertFalse(chimera.can_interact_with_physical)

    def test_chimera_can_interact_with_physical_true(self):
        """Test setting can_interact_with_physical to True."""
        chimera = Chimera.objects.create(name="Physical", can_interact_with_physical=True)
        self.assertTrue(chimera.can_interact_with_physical)

    def test_chimera_is_permanent_default(self):
        """Test that is_permanent defaults to False."""
        chimera = Chimera.objects.create(name="Temporary")
        self.assertFalse(chimera.is_permanent)

    def test_chimera_is_permanent_true(self):
        """Test setting is_permanent to True."""
        chimera = Chimera.objects.create(name="Permanent", is_permanent=True)
        self.assertTrue(chimera.is_permanent)

    def test_chimera_behavior_field(self):
        """Test behavior field."""
        chimera = Chimera.objects.create(
            name="Behavior Test",
            behavior="Follows owner around and protects them",
        )
        self.assertEqual(chimera.behavior, "Follows owner around and protects them")

    def test_chimera_appearance_field(self):
        """Test appearance field."""
        chimera = Chimera.objects.create(
            name="Appearance Test",
            appearance="A small dragon made of smoke",
        )
        self.assertEqual(chimera.appearance, "A small dragon made of smoke")

    def test_chimera_creator_field(self):
        """Test creator field."""
        chimera = Chimera.objects.create(
            name="Created Chimera",
            creator="Lord Faeryn",
        )
        self.assertEqual(chimera.creator, "Lord Faeryn")

    def test_chimera_dream_source_field(self):
        """Test dream_source field."""
        chimera = Chimera.objects.create(
            name="Dream Chimera",
            origin="manifested_dream",
            dream_source="A child's nightmare about monsters under the bed",
        )
        self.assertEqual(chimera.dream_source, "A child's nightmare about monsters under the bed")


class TestChimeraDetailView(TestCase):
    """Tests for Chimera detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.chimera = Chimera.objects.create(
            name="Test Chimera",
            chimera_type="simple_crafted",
        )
        self.url = self.chimera.get_absolute_url()

    def test_chimera_detail_view_status_code(self):
        """Test that detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_chimera_detail_view_context(self):
        """Test that detail view contains chimera object."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.context["object"], self.chimera)


class TestChimeraCreateView(TestCase):
    """Tests for Chimera create view."""

    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.url = Chimera.get_creation_url()

    def test_chimera_create_view_status_code(self):
        """Test that create view returns 200."""
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_chimera_create_view_successful_post(self):
        """Test successful chimera creation."""
        self.client.login(username="ST", password="password")
        data = {
            "name": "New Chimera",
            "chimera_type": "advanced_crafted",
            "chimera_points": 20,
            "sentience_level": "sentient",
            "durability": 3,
            "loyalty": 4,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Chimera.objects.filter(name="New Chimera").count(), 1)


class TestChimeraUpdateView(TestCase):
    """Tests for Chimera update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.chimera = Chimera.objects.create(
            name="Test Chimera",
            chimera_type="simple_crafted",
        )
        self.url = self.chimera.get_update_url()

    def test_chimera_update_view_status_code(self):
        """Test that update view returns 200."""
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_chimera_update_view_successful_post(self):
        """Test successful chimera update."""
        self.client.login(username="ST", password="password")
        data = {
            "name": "Updated Chimera",
            "chimera_type": "complex_crafted",
            "chimera_points": 25,
            "sentience_level": "fully_sentient",
            "durability": 5,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.chimera.refresh_from_db()
        self.assertEqual(self.chimera.name, "Updated Chimera")
        self.assertEqual(self.chimera.chimera_type, "complex_crafted")


class TestChimeraDifferentTypes(TestCase):
    """Tests for different chimera types and their characteristics."""

    def test_facsimile_chimera(self):
        """Test creating a facsimile chimera."""
        chimera = Chimera.objects.create(
            name="Shadow Double",
            chimera_type="facsimile",
            chimera_points=5,
            sentience_level="non_sentient",
        )
        self.assertEqual(chimera.chimera_type, "facsimile")
        self.assertEqual(chimera.get_chimera_type_display(), "Facsimile")

    def test_simple_crafted_chimera(self):
        """Test creating a simple crafted chimera."""
        chimera = Chimera.objects.create(
            name="Paper Bird",
            chimera_type="simple_crafted",
            chimera_points=8,
        )
        self.assertEqual(chimera.chimera_type, "simple_crafted")
        self.assertEqual(chimera.get_chimera_type_display(), "Simple Crafted")

    def test_advanced_crafted_chimera(self):
        """Test creating an advanced crafted chimera."""
        chimera = Chimera.objects.create(
            name="Clockwork Servant",
            chimera_type="advanced_crafted",
            chimera_points=18,
            sentience_level="semi_sentient",
        )
        self.assertEqual(chimera.chimera_type, "advanced_crafted")
        self.assertEqual(chimera.get_chimera_type_display(), "Advanced Crafted")

    def test_complex_crafted_chimera(self):
        """Test creating a complex crafted chimera."""
        chimera = Chimera.objects.create(
            name="Dream Guardian",
            chimera_type="complex_crafted",
            chimera_points=35,
            sentience_level="sentient",
        )
        self.assertEqual(chimera.chimera_type, "complex_crafted")
        self.assertEqual(chimera.get_chimera_type_display(), "Complex Crafted")

    def test_master_crafted_chimera(self):
        """Test creating a master crafted chimera."""
        chimera = Chimera.objects.create(
            name="The Nightmare King",
            chimera_type="master_crafted",
            chimera_points=50,
            sentience_level="fully_sentient",
            is_permanent=True,
        )
        self.assertEqual(chimera.chimera_type, "master_crafted")
        self.assertEqual(chimera.get_chimera_type_display(), "Master Crafted")
        self.assertTrue(chimera.is_permanent)
