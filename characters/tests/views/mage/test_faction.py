"""Tests for MageFaction views."""

from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Paradigm, Practice
from characters.models.mage.sphere import Sphere
from core.models import Language
from items.models.core.material import Material
from items.models.core.medium import Medium


class TestMageFactionDetailView(TestCase):
    """Tests for MageFactionDetailView."""

    def setUp(self):
        self.faction = MageFaction.objects.create(name="Test MageFaction", description="Test")
        self.url = self.faction.get_absolute_url()

    def test_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/faction/detail.html")

    def test_detail_view_context_data(self):
        """Test that context data includes expected keys."""
        # Add related data to test context
        language = Language.objects.create(name="Enochian")
        sphere = Sphere.objects.create(name="Forces", property_name="forces")
        paradigm = Paradigm.objects.create(name="Divine Order")
        practice = Practice.objects.create(name="High Ritual Magick")
        medium = Medium.objects.create(name="Spoken Word")
        material = Material.objects.create(name="Gold")

        self.faction.languages.add(language)
        self.faction.affinities.add(sphere)
        self.faction.paradigms.add(paradigm)
        self.faction.practices.add(practice)
        self.faction.media.add(medium)
        self.faction.materials.add(material)
        self.faction.founded = 1325
        self.faction.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("languages", response.context)
        self.assertIn("affinities", response.context)
        self.assertIn("paradigms", response.context)
        self.assertIn("practices", response.context)
        self.assertIn("media", response.context)
        self.assertIn("materials", response.context)
        self.assertIn("year", response.context)
        self.assertEqual(response.context["year"], 1325)


class TestMageFactionCreateView(TestCase):
    """Tests for MageFactionCreateView."""

    def setUp(self):
        self.valid_data = {
            "name": "Test MageFaction",
            "description": "Test description",
            "founded": 2000,
            "ended": 2001,
        }
        self.url = MageFaction.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/faction/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MageFaction.objects.count(), 1)
        self.assertEqual(MageFaction.objects.first().name, "Test MageFaction")


class TestMageFactionUpdateView(TestCase):
    """Tests for MageFactionUpdateView."""

    def setUp(self):
        self.faction = MageFaction.objects.create(name="Test MageFaction", description="Test")
        self.valid_data = {
            "name": "Test MageFaction Updated",
            "description": "Test",
            "founded": 2000,
            "ended": 2001,
        }
        self.url = self.faction.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/faction/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.faction.refresh_from_db()
        self.assertEqual(self.faction.name, "Test MageFaction Updated")
        self.assertEqual(self.faction.description, "Test")


class TestMageFactionListView(TestCase):
    """Tests for MageFactionListView."""

    def setUp(self):
        self.client = Client()
        # Create multiple factions with various related data
        for i in range(5):
            faction = MageFaction.objects.create(
                name=f"Faction {i}",
                description=f"Description {i}",
                founded=1900 + i,
            )
            # Add some related objects to test prefetching
            paradigm = Paradigm.objects.create(name=f"Paradigm {i}")
            practice = Practice.objects.create(name=f"Practice {i}")
            faction.paradigms.add(paradigm)
            faction.practices.add(practice)

    def test_list_view_status_code(self):
        response = self.client.get("/characters/mage/list/mage_factions/")
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        response = self.client.get("/characters/mage/list/mage_factions/")
        self.assertTemplateUsed(response, "characters/mage/faction/list.html")

    def test_list_view_context_contains_factions(self):
        response = self.client.get("/characters/mage/list/mage_factions/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("object_list", response.context)
        self.assertEqual(len(response.context["object_list"]), 5)

    def test_list_view_ordered_by_name(self):
        """Test that factions are ordered alphabetically by name."""
        response = self.client.get("/characters/mage/list/mage_factions/")
        object_list = list(response.context["object_list"])
        names = [f.name for f in object_list]
        self.assertEqual(names, sorted(names))

    def test_list_view_query_count_is_bounded(self):
        """Test that list view query count doesn't scale with number of factions."""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get("/characters/mage/list/mage_factions/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # Base queries: session, content type, faction list
        # Should not have N+1 queries for related objects
        self.assertLessEqual(
            query_count,
            10,
            f"Too many queries ({query_count}). List view may have N+1 issue.",
        )


class TestMageFactionHierarchy(TestCase):
    """Tests for MageFaction parent-child relationships in views."""

    def setUp(self):
        self.parent_faction = MageFaction.objects.create(
            name="Parent Faction",
            description="Parent description",
        )
        self.child_faction = MageFaction.objects.create(
            name="Child Faction",
            description="Child description",
            parent=self.parent_faction,
        )

    def test_detail_view_shows_subfactions(self):
        """Test that detail view shows subfactions in context."""
        response = self.client.get(self.parent_faction.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("subfactions", response.context)
        self.assertIn("Child Faction", response.context["subfactions"])

    def test_create_faction_with_parent(self):
        """Test creating a faction with a parent."""
        data = {
            "name": "New Child Faction",
            "description": "New child description",
            "founded": 2000,
            "ended": 5000,
            "parent": self.parent_faction.pk,
        }
        response = self.client.post(MageFaction.get_creation_url(), data=data)
        self.assertEqual(response.status_code, 302)
        new_faction = MageFaction.objects.get(name="New Child Faction")
        self.assertEqual(new_faction.parent, self.parent_faction)
