from characters.models.core.human import Human
from characters.models.mage.cabal import Cabal
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase
from items.models.mage.grimoire import Grimoire
from locations.models.mage.chantry import Chantry
from locations.models.mage.library import Library
from locations.models.mage.node import Node


class TestChantry(TestCase):
    def setUp(self) -> None:
        self.chantry = Chantry.objects.create(name="")
        self.library = Library.objects.create(rank=3)
        self.grimoire1 = Grimoire.objects.create()
        self.grimoire2 = Grimoire.objects.create()
        self.grimoire3 = Grimoire.objects.create()
        self.library.add_book(self.grimoire1)
        self.library.add_book(self.grimoire2)
        self.library.add_book(self.grimoire3)
        self.node1 = Node.objects.create(name="node1", rank=1)
        self.node2 = Node.objects.create(name="node2", rank=1)
        self.human = Human.objects.create(name="human")
        self.cabal = Cabal.objects.create(name="cabal")
        self.faction = MageFaction.objects.create(name="faction")
        self.player = User.objects.create_user(username="Test")
        self.character = Mage.objects.create(name="", owner=self.player)
        self.grimoire = Grimoire.objects.create(name="Grimoire")
        mage_setup()

    def test_trait_cost(self):
        self.assertEqual(self.chantry.trait_cost("allies"), 2)
        self.assertEqual(self.chantry.trait_cost("arcane"), 2)
        self.assertEqual(self.chantry.trait_cost("backup"), 2)
        self.assertEqual(self.chantry.trait_cost("cult"), 2)
        self.assertEqual(self.chantry.trait_cost("elders"), 2)
        self.assertEqual(self.chantry.trait_cost("integrated_effects"), 2)
        self.assertEqual(self.chantry.trait_cost("library_rating"), 2)
        self.assertEqual(self.chantry.trait_cost("retainers"), 2)
        self.assertEqual(self.chantry.trait_cost("spies"), 2)
        self.assertEqual(self.chantry.trait_cost("node_rating"), 3)
        self.assertEqual(self.chantry.trait_cost("resources"), 3)
        self.assertEqual(self.chantry.trait_cost("enhancement"), 4)
        self.assertEqual(self.chantry.trait_cost("requisitions"), 4)
        self.assertEqual(self.chantry.trait_cost("reality_zone_rating"), 5)

    def test_has_node(self):
        self.chantry.node_rating = 1
        self.assertFalse(self.chantry.has_node())
        self.chantry.nodes.add(self.node1)
        self.assertTrue(self.chantry.has_node())

    def test_total_node(self):
        self.assertEqual(self.chantry.total_node(), 0)
        self.chantry.nodes.add(self.node1)
        self.assertEqual(self.chantry.total_node(), 1)
        self.chantry.nodes.add(self.node2)
        self.assertEqual(self.chantry.total_node(), 2)

    def test_has_library(self):
        self.chantry.library_rating = 3
        self.assertFalse(self.chantry.has_library())
        self.chantry.chantry_library = self.library
        self.chantry.save()
        self.assertTrue(self.chantry.has_library())

    def test_set_library(self):
        library = Library.objects.create(name="Test Library", rank=0)
        self.assertFalse(self.chantry.has_library())
        self.chantry.set_library(library)
        self.assertTrue(self.chantry.has_library())

    def test_add_node(self):
        node = Node.objects.create(name="Test Node", rank=3)
        self.chantry.node_rating = 3
        self.assertFalse(self.chantry.has_node())
        self.chantry.add_node(node)
        self.assertTrue(self.chantry.has_node())

    def test_points_spent(self):
        self.assertEqual(self.chantry.points_spent(), 0)
        self.chantry.requisitions = 3
        self.assertEqual(self.chantry.points_spent(), 12)
        self.chantry.node_rating = 8
        self.assertEqual(self.chantry.points_spent(), 36)
        self.chantry.arcane = 1
        self.assertEqual(self.chantry.points_spent(), 38)

    def test_set_rank(self):
        self.chantry.set_rank(5)
        self.assertEqual(self.chantry.rank, 5)

    def test_has_faction(self):
        faction = MageFaction.objects.get(name="Test Faction 0")
        self.assertFalse(self.chantry.has_faction())
        self.chantry.faction = faction
        self.chantry.save()
        self.assertTrue(self.chantry.has_faction())

    def test_set_faction(self):
        faction = MageFaction.objects.get(name="Test Faction 0")
        self.assertFalse(self.chantry.has_faction())
        self.assertTrue(self.chantry.set_faction(faction))
        self.assertEqual(self.chantry.faction, faction)
        self.assertTrue(self.chantry.has_faction())

    def test_has_name(self):
        self.assertFalse(self.chantry.has_name())
        self.chantry.name = "Test"
        self.assertTrue(self.chantry.has_name())

    def test_set_name(self):
        self.assertFalse(self.chantry.has_name())
        self.assertTrue(self.chantry.set_name("Test Chantry"))
        self.assertTrue(self.chantry.has_name())

    def test_has_chantry_type(self):
        self.assertFalse(self.chantry.has_chantry_type())
        self.chantry.chantry_type = "war"
        self.assertTrue(self.chantry.has_chantry_type())

    def test_set_chantry_type(self):
        self.assertFalse(self.chantry.has_chantry_type())
        self.chantry.set_chantry_type("war")
        self.assertTrue(self.chantry.has_chantry_type())

    def test_has_season(self):
        self.assertFalse(self.chantry.has_season())
        self.chantry.season = "spring"
        self.assertTrue(self.chantry.has_season())

    def test_set_season(self):
        self.assertFalse(self.chantry.has_season())
        self.chantry.set_season("spring")
        self.assertTrue(self.chantry.has_season())

    def test_get_traits(self):
        self.chantry.allies = 2
        self.chantry.arcane = 3
        self.chantry.backup = 4
        self.chantry.cult = 5
        self.chantry.elders = 6
        self.chantry.integrated_effects = 7
        self.chantry.retainers = 8
        self.chantry.spies = 9
        self.chantry.resources = 10
        self.chantry.enhancement = 11
        self.chantry.requisitions = 12
        self.chantry.reality_zone_rating = 13
        self.chantry.node_rating = 14
        self.chantry.library_rating = 15
        self.chantry.save()

        result = self.chantry.get_traits()
        expected = {
            "allies": 2,
            "arcane": 3,
            "backup": 4,
            "cult": 5,
            "elders": 6,
            "integrated_effects": 7,
            "retainers": 8,
            "spies": 9,
            "resources": 10,
            "enhancement": 11,
            "requisitions": 12,
            "reality_zone": 13,
            "node_rating": 14,
            "library_rating": 15,
        }

        self.assertEqual(result, expected)


class TestChantryDetailView(TestCase):
    def setUp(self) -> None:
        self.chantry = Chantry.objects.create(name="Test Chantry")
        self.url = self.chantry.get_absolute_url()

    def test_chantry_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_chantry_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/chantry/detail.html")


class TestChantryCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Chantry",
            "description": "Test",
            "leadership_type": "panel",
            "season": "spring",
            "chantry_type": "exploration",
            "rank": 3,
            "points": 0,
            "allies": 0,
            "arcane": 0,
            "backup": 0,
            "cult": 0,
            "elders": 0,
            "integrated_effects": 3,
            "retainers": 2,
            "spies": 1,
            "resources": 0,
            "enhancement": 1,
            "requisitions": 2,
            "reality_zone_rating": 2,
            "node_rating": 3,
            "library_rating": 4,
        }
        self.url = Chantry.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/chantry/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Chantry.objects.count(), 1)
        self.assertEqual(Chantry.objects.first().name, "Chantry")


class TestChantryUpdateView(TestCase):
    def setUp(self):
        self.chantry = Chantry.objects.create(
            name="Test Chantry",
            description="Test description",
        )
        self.valid_data = {
            "name": "Chantry Updated",
            "description": "Test Chantry",
            "leadership_type": "panel",
            "season": "spring",
            "chantry_type": "exploration",
            "rank": 3,
            "points": 0,
            "allies": 0,
            "arcane": 0,
            "backup": 0,
            "cult": 0,
            "elders": 0,
            "integrated_effects": 3,
            "retainers": 2,
            "spies": 1,
            "resources": 0,
            "enhancement": 1,
            "requisitions": 2,
            "reality_zone_rating": 2,
            "node_rating": 3,
            "library_rating": 4,
        }
        self.url = self.chantry.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/chantry/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.name, "Chantry Updated")
        self.assertEqual(self.chantry.description, "Test Chantry")


class TestCharacterRetirementChantryRemoval(TestCase):
    """Test that retiring or marking a character as deceased removes them from chantries."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.player,
            status="App",  # Approved status
        )
        self.chantry = Chantry.objects.create(name="Test Chantry")

    def test_character_removed_from_chantry_members_on_retirement(self):
        """Test that retiring a character removes them from chantry membership."""
        self.chantry.members.add(self.character)
        self.assertIn(self.character, self.chantry.members.all())

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from chantry
        self.assertNotIn(self.character, self.chantry.members.all())

    def test_character_removed_from_chantry_leaders_on_retirement(self):
        """Test that retiring a character removes them from chantry leadership."""
        self.chantry.leaders.add(self.character)
        self.assertIn(self.character, self.chantry.leaders.all())

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from leadership
        self.assertNotIn(self.character, self.chantry.leaders.all())

    def test_character_removed_from_ambassador_on_retirement(self):
        """Test that retiring a character removes them from ambassador position."""
        self.chantry.ambassador = self.character
        self.chantry.save()
        self.assertEqual(self.chantry.ambassador, self.character)

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from ambassador position
        self.assertIsNone(self.chantry.ambassador)

    def test_character_removed_from_node_tender_on_retirement(self):
        """Test that retiring a character removes them from node tender position."""
        self.chantry.node_tender = self.character
        self.chantry.save()
        self.assertEqual(self.chantry.node_tender, self.character)

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from node tender position
        self.assertIsNone(self.chantry.node_tender)

    def test_character_removed_from_investigator_on_retirement(self):
        """Test that retiring a character removes them from investigator role."""
        self.chantry.investigator.add(self.character)
        self.assertIn(self.character, self.chantry.investigator.all())

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from investigator role
        self.assertNotIn(self.character, self.chantry.investigator.all())

    def test_character_removed_from_guardian_on_retirement(self):
        """Test that retiring a character removes them from guardian role."""
        self.chantry.guardian.add(self.character)
        self.assertIn(self.character, self.chantry.guardian.all())

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from guardian role
        self.assertNotIn(self.character, self.chantry.guardian.all())

    def test_character_removed_from_teacher_on_retirement(self):
        """Test that retiring a character removes them from teacher role."""
        self.chantry.teacher.add(self.character)
        self.assertIn(self.character, self.chantry.teacher.all())

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from teacher role
        self.assertNotIn(self.character, self.chantry.teacher.all())

    def test_character_removed_from_all_chantry_roles_on_death(self):
        """Test that marking a character as deceased removes them from all chantry roles."""
        # Add character to all possible roles
        self.chantry.members.add(self.character)
        self.chantry.leaders.add(self.character)
        self.chantry.ambassador = self.character
        self.chantry.node_tender = self.character
        self.chantry.investigator.add(self.character)
        self.chantry.guardian.add(self.character)
        self.chantry.teacher.add(self.character)
        self.chantry.save()

        # Mark character as deceased
        self.character.status = "Dec"
        self.character.save()

        # Refresh from database
        self.chantry.refresh_from_db()

        # Character should be removed from all roles
        self.assertNotIn(self.character, self.chantry.members.all())
        self.assertNotIn(self.character, self.chantry.leaders.all())
        self.assertIsNone(self.chantry.ambassador)
        self.assertIsNone(self.chantry.node_tender)
        self.assertNotIn(self.character, self.chantry.investigator.all())
        self.assertNotIn(self.character, self.chantry.guardian.all())
        self.assertNotIn(self.character, self.chantry.teacher.all())
