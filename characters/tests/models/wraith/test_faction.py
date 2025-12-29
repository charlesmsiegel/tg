"""Tests for WraithFaction model."""

from characters.models.wraith.faction import WraithFaction
from django.test import TestCase


class TestWraithFactionModel(TestCase):
    """Tests for WraithFaction model creation and attributes."""

    def test_faction_creation(self):
        """WraithFaction can be created with basic attributes."""
        faction = WraithFaction.objects.create(
            name="Iron Legion",
            faction_type="legion",
            description="Legion of soldiers and warriors.",
        )
        self.assertEqual(faction.name, "Iron Legion")
        self.assertEqual(faction.faction_type, "legion")

    def test_faction_default_values(self):
        """WraithFaction has correct default values."""
        faction = WraithFaction.objects.create(
            name="Test Faction",
            description="Test description",
        )
        self.assertEqual(faction.faction_type, "legion")
        self.assertIsNone(faction.parent)

    def test_faction_type_choices(self):
        """WraithFaction can have various faction types."""
        legion = WraithFaction.objects.create(
            name="Legion",
            faction_type="legion",
            description="Legion faction",
        )
        guild = WraithFaction.objects.create(
            name="Guild",
            faction_type="guild",
            description="Guild faction",
        )
        heretic = WraithFaction.objects.create(
            name="Heretic",
            faction_type="heretic",
            description="Heretic faction",
        )
        spectre = WraithFaction.objects.create(
            name="Spectre",
            faction_type="spectre",
            description="Spectre faction",
        )
        other = WraithFaction.objects.create(
            name="Other",
            faction_type="other",
            description="Other faction",
        )
        self.assertEqual(legion.faction_type, "legion")
        self.assertEqual(guild.faction_type, "guild")
        self.assertEqual(heretic.faction_type, "heretic")
        self.assertEqual(spectre.faction_type, "spectre")
        self.assertEqual(other.faction_type, "other")

    def test_faction_gameline(self):
        """WraithFaction has correct gameline."""
        faction = WraithFaction.objects.create(name="Test", description="Test")
        self.assertEqual(faction.gameline, "wto")

    def test_faction_type_attribute(self):
        """WraithFaction has correct type attribute."""
        faction = WraithFaction.objects.create(name="Test", description="Test")
        self.assertEqual(faction.type, "wraith_faction")


class TestWraithFactionHierarchy(TestCase):
    """Tests for WraithFaction parent-child relationships."""

    def test_faction_can_have_parent(self):
        """WraithFaction can have a parent faction."""
        parent = WraithFaction.objects.create(
            name="Parent Faction",
            description="Parent",
        )
        child = WraithFaction.objects.create(
            name="Child Faction",
            parent=parent,
            description="Child",
        )
        self.assertEqual(child.parent, parent)

    def test_faction_subfactions_related_name(self):
        """Parent faction can access subfactions via related name."""
        parent = WraithFaction.objects.create(
            name="Parent Faction",
            description="Parent",
        )
        child1 = WraithFaction.objects.create(
            name="Child 1",
            parent=parent,
            description="Child 1",
        )
        child2 = WraithFaction.objects.create(
            name="Child 2",
            parent=parent,
            description="Child 2",
        )
        self.assertIn(child1, parent.subfactions.all())
        self.assertIn(child2, parent.subfactions.all())
        self.assertEqual(parent.subfactions.count(), 2)

    def test_deleting_parent_nullifies_children(self):
        """Deleting parent faction sets children's parent to null."""
        parent = WraithFaction.objects.create(
            name="Parent",
            description="Parent",
        )
        child = WraithFaction.objects.create(
            name="Child",
            parent=parent,
            description="Child",
        )
        child_id = child.id

        parent.delete()
        child.refresh_from_db()
        self.assertIsNone(child.parent)


class TestWraithFactionUrls(TestCase):
    """Tests for WraithFaction URL methods."""

    def setUp(self):
        self.faction = WraithFaction.objects.create(
            name="Test Faction",
            description="Test description",
        )

    def test_get_absolute_url_method_exists(self):
        """WraithFaction has get_absolute_url method."""
        self.assertTrue(hasattr(self.faction, "get_absolute_url"))
        self.assertTrue(callable(getattr(self.faction, "get_absolute_url")))

    def test_get_update_url_method_exists(self):
        """WraithFaction has get_update_url method."""
        self.assertTrue(hasattr(self.faction, "get_update_url"))
        self.assertTrue(callable(getattr(self.faction, "get_update_url")))

    def test_get_creation_url_method_exists(self):
        """WraithFaction has get_creation_url class method."""
        self.assertTrue(hasattr(WraithFaction, "get_creation_url"))
        self.assertTrue(callable(getattr(WraithFaction, "get_creation_url")))

    def test_get_heading(self):
        """WraithFaction returns correct heading class."""
        self.assertEqual(self.faction.get_heading(), "wto_heading")


class TestWraithFactionMetaOptions(TestCase):
    """Tests for WraithFaction Meta options."""

    def test_verbose_name(self):
        """WraithFaction has correct verbose_name."""
        self.assertEqual(WraithFaction._meta.verbose_name, "Wraith Faction")

    def test_verbose_name_plural(self):
        """WraithFaction has correct verbose_name_plural."""
        self.assertEqual(WraithFaction._meta.verbose_name_plural, "Wraith Factions")


class TestWraithFactionStr(TestCase):
    """Tests for WraithFaction string representation."""

    def test_faction_str(self):
        """WraithFaction uses name for string representation."""
        faction = WraithFaction.objects.create(
            name="Renegades",
            description="Free wraiths",
        )
        self.assertEqual(str(faction), "Renegades")
