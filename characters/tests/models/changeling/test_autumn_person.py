"""Tests for Autumn Person model."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.changeling.autumn_person import AutumnPerson


class TestAutumnPerson(TestCase):
    """Tests for Autumn Person model methods."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        # Provide required fields for AutumnPerson
        self.character = AutumnPerson.objects.create(
            owner=self.player,
            name="Test Autumn Person",
            archetype="authority",
        )

    def test_autumn_person_creation(self):
        """Test basic creation of an Autumn Person."""
        self.assertEqual(self.character.name, "Test Autumn Person")
        self.assertEqual(self.character.type, "autumn_person")
        self.assertEqual(self.character.banality_rating, 8)  # Default high banality
        self.assertEqual(self.character.awareness, "unaware")  # Default awareness

    def test_has_archetype(self):
        """Test has_archetype method."""
        self.assertTrue(self.character.has_archetype())
        self.character.archetype = ""
        self.assertFalse(self.character.has_archetype())

    def test_set_archetype(self):
        """Test setting archetype."""
        result = self.character.set_archetype("bureaucrat")
        self.assertTrue(result)
        self.assertEqual(self.character.archetype, "bureaucrat")
        self.assertTrue(self.character.has_archetype())

    def test_set_archetype_all_types(self):
        """Test setting various archetype types."""
        archetypes = [
            "authority",
            "bureaucrat",
            "cynic",
            "fundamentalist",
            "corporate",
            "scientist",
            "debunker",
            "other",
        ]
        for archetype in archetypes:
            self.character.set_archetype(archetype)
            self.assertEqual(self.character.archetype, archetype)

    def test_set_awareness(self):
        """Test setting awareness level."""
        result = self.character.set_awareness("suspicious")
        self.assertTrue(result)
        self.assertEqual(self.character.awareness, "suspicious")

    def test_set_awareness_all_levels(self):
        """Test all awareness levels."""
        levels = ["unaware", "suspicious", "aware", "hunter"]
        for level in levels:
            result = self.character.set_awareness(level)
            self.assertTrue(result)
            self.assertEqual(self.character.awareness, level)

    def test_has_organization(self):
        """Test has_organization method."""
        self.assertFalse(self.character.has_organization())
        self.character.organization = "FBI"
        self.assertTrue(self.character.has_organization())

    def test_set_organization(self):
        """Test setting organization."""
        self.assertFalse(self.character.has_organization())
        result = self.character.set_organization("Local Police Department")
        self.assertTrue(result)
        self.assertEqual(self.character.organization, "Local Police Department")
        self.assertTrue(self.character.has_organization())

    def test_has_motivation(self):
        """Test has_motivation method."""
        self.assertFalse(self.character.has_motivation())
        self.character.motivation = "Fear of the unknown"
        self.assertTrue(self.character.has_motivation())

    def test_set_motivation(self):
        """Test setting motivation."""
        self.assertFalse(self.character.has_motivation())
        result = self.character.set_motivation("Bitter after childhood dreams were crushed")
        self.assertTrue(result)
        self.assertEqual(self.character.motivation, "Bitter after childhood dreams were crushed")
        self.assertTrue(self.character.has_motivation())

    def test_has_sphere_of_influence(self):
        """Test has_sphere_of_influence method."""
        self.assertFalse(self.character.has_sphere_of_influence())
        self.character.sphere_of_influence = "Downtown business district"
        self.assertTrue(self.character.has_sphere_of_influence())

    def test_set_sphere_of_influence(self):
        """Test setting sphere of influence."""
        self.assertFalse(self.character.has_sphere_of_influence())
        result = self.character.set_sphere_of_influence("University campus")
        self.assertTrue(result)
        self.assertEqual(self.character.sphere_of_influence, "University campus")
        self.assertTrue(self.character.has_sphere_of_influence())

    def test_make_dauntain(self):
        """Test make_dauntain method."""
        self.assertFalse(self.character.is_dauntain)
        self.assertEqual(self.character.banality_rating, 8)

        result = self.character.make_dauntain("Pooka")
        self.assertTrue(result)
        self.assertTrue(self.character.is_dauntain)
        self.assertEqual(self.character.former_kith, "Pooka")
        self.assertEqual(self.character.banality_rating, 10)  # Max banality for Dauntain

    def test_make_dauntain_without_kith(self):
        """Test make_dauntain method without specifying former kith."""
        result = self.character.make_dauntain()
        self.assertTrue(result)
        self.assertTrue(self.character.is_dauntain)
        self.assertEqual(self.character.former_kith, "")
        self.assertEqual(self.character.banality_rating, 10)

    def test_add_anti_fae_ability(self):
        """Test adding anti-fae abilities."""
        self.assertEqual(self.character.anti_fae_abilities, [])

        result = self.character.add_anti_fae_ability("Cold Iron Affinity")
        self.assertTrue(result)
        self.assertIn("Cold Iron Affinity", self.character.anti_fae_abilities)

        # Add another ability
        result = self.character.add_anti_fae_ability("Banality Aura")
        self.assertTrue(result)
        self.assertIn("Banality Aura", self.character.anti_fae_abilities)
        self.assertEqual(len(self.character.anti_fae_abilities), 2)

    def test_add_anti_fae_ability_no_duplicates(self):
        """Test that duplicate abilities are not added."""
        self.character.add_anti_fae_ability("Cold Iron Affinity")
        self.character.add_anti_fae_ability("Cold Iron Affinity")

        self.assertEqual(len(self.character.anti_fae_abilities), 1)
        self.assertEqual(self.character.anti_fae_abilities.count("Cold Iron Affinity"), 1)

    def test_archetypes_choices(self):
        """Test that ARCHETYPES constant exists and has expected values."""
        archetypes_dict = dict(AutumnPerson.ARCHETYPES)
        self.assertIn("authority", archetypes_dict)
        self.assertIn("bureaucrat", archetypes_dict)
        self.assertIn("cynic", archetypes_dict)
        self.assertIn("fundamentalist", archetypes_dict)
        self.assertIn("corporate", archetypes_dict)
        self.assertIn("scientist", archetypes_dict)
        self.assertIn("debunker", archetypes_dict)
        self.assertIn("other", archetypes_dict)

    def test_awareness_levels_choices(self):
        """Test that AWARENESS_LEVELS constant exists and has expected values."""
        awareness_dict = dict(AutumnPerson.AWARENESS_LEVELS)
        self.assertIn("unaware", awareness_dict)
        self.assertIn("suspicious", awareness_dict)
        self.assertIn("aware", awareness_dict)
        self.assertIn("hunter", awareness_dict)

    def test_default_anti_fae_abilities_is_list(self):
        """Test that anti_fae_abilities defaults to empty list."""
        self.assertIsInstance(self.character.anti_fae_abilities, list)
        self.assertEqual(len(self.character.anti_fae_abilities), 0)

    def test_gameline(self):
        """Test that gameline is set to ctd."""
        self.assertEqual(self.character.gameline, "ctd")

    def test_verbose_name(self):
        """Test model verbose names."""
        self.assertEqual(AutumnPerson._meta.verbose_name, "Autumn Person")
        self.assertEqual(AutumnPerson._meta.verbose_name_plural, "Autumn People")
