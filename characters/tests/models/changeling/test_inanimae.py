"""Tests for Inanimae model."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.changeling.inanimae import Inanimae


class TestInanimae(TestCase):
    """Tests for Inanimae model methods."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        # Provide required fields for Inanimae
        self.character = Inanimae.objects.create(
            owner=self.player,
            name="Test Inanimae",
            kingdom="kubera",
            inanimae_seeming="naturae",
            season="summer",
        )

    def test_inanimae_creation(self):
        """Test basic creation of an Inanimae."""
        self.assertEqual(self.character.name, "Test Inanimae")
        self.assertEqual(self.character.type, "inanimae")
        self.assertEqual(self.character.mana, 4)  # Default mana

    def test_has_kingdom(self):
        """Test has_kingdom method."""
        self.assertTrue(self.character.has_kingdom())
        self.character.kingdom = ""
        self.assertFalse(self.character.has_kingdom())

    def test_set_kingdom(self):
        """Test setting kingdom."""
        result = self.character.set_kingdom("ondine")
        self.assertTrue(result)
        self.assertEqual(self.character.kingdom, "ondine")
        self.assertTrue(self.character.has_kingdom())

    def test_set_kingdom_all_types(self):
        """Test setting all kingdom types."""
        kingdoms = [
            "kubera",  # Earth
            "ondine",  # Water
            "paroseme",  # Wood/plant
            "sylph",  # Air
            "salamander",  # Fire
            "solimond",  # Crystal/mineral
            "mannikin",  # Artificial
        ]
        for kingdom in kingdoms:
            result = self.character.set_kingdom(kingdom)
            self.assertTrue(result)
            self.assertEqual(self.character.kingdom, kingdom)

    def test_has_season(self):
        """Test has_season method."""
        self.assertTrue(self.character.has_season())
        self.character.season = ""
        self.assertFalse(self.character.has_season())

    def test_set_season(self):
        """Test setting season."""
        result = self.character.set_season("winter")
        self.assertTrue(result)
        self.assertEqual(self.character.season, "winter")
        self.assertTrue(self.character.has_season())

    def test_set_season_all_types(self):
        """Test setting all season types."""
        seasons = ["spring", "summer", "autumn", "winter"]
        for season in seasons:
            result = self.character.set_season(season)
            self.assertTrue(result)
            self.assertEqual(self.character.season, season)

    def test_has_inanimae_seeming(self):
        """Test has_inanimae_seeming method."""
        self.assertTrue(self.character.has_inanimae_seeming())
        self.character.inanimae_seeming = ""
        self.assertFalse(self.character.has_inanimae_seeming())

    def test_set_inanimae_seeming_glimmer(self):
        """Test setting glimmer seeming increases mana."""
        result = self.character.set_inanimae_seeming("glimmer")
        self.assertTrue(result)
        self.assertEqual(self.character.inanimae_seeming, "glimmer")
        self.assertEqual(self.character.mana, 5)  # Young and full of energy
        self.assertTrue(self.character.has_inanimae_seeming())

    def test_set_inanimae_seeming_naturae(self):
        """Test setting naturae seeming gives default mana."""
        result = self.character.set_inanimae_seeming("naturae")
        self.assertTrue(result)
        self.assertEqual(self.character.inanimae_seeming, "naturae")
        self.assertEqual(self.character.mana, 4)  # Mature, balanced
        self.assertTrue(self.character.has_inanimae_seeming())

    def test_set_inanimae_seeming_ancient(self):
        """Test setting ancient seeming decreases mana."""
        result = self.character.set_inanimae_seeming("ancient")
        self.assertTrue(result)
        self.assertEqual(self.character.inanimae_seeming, "ancient")
        self.assertEqual(self.character.mana, 3)  # Less energy but more wisdom
        self.assertTrue(self.character.has_inanimae_seeming())

    def test_add_mana(self):
        """Test adding mana."""
        initial_mana = self.character.mana
        result = self.character.add_mana()
        self.assertTrue(result)
        self.assertEqual(self.character.mana, initial_mana + 1)

    def test_add_mana_at_max(self):
        """Test that add_mana fails at maximum (10)."""
        self.character.mana = 10
        result = self.character.add_mana()
        self.assertFalse(result)
        self.assertEqual(self.character.mana, 10)

    def test_has_anchor(self):
        """Test has_anchor method."""
        self.assertFalse(self.character.has_anchor())
        self.character.anchor_description = "An ancient oak tree"
        self.assertTrue(self.character.has_anchor())

    def test_set_anchor(self):
        """Test setting anchor."""
        self.assertFalse(self.character.has_anchor())
        result = self.character.set_anchor("A sacred spring in the forest")
        self.assertTrue(result)
        self.assertEqual(self.character.anchor_description, "A sacred spring in the forest")
        self.assertTrue(self.character.has_anchor())

    def test_elemental_strength_and_weakness(self):
        """Test elemental strength and weakness fields."""
        self.assertEqual(self.character.elemental_strength, "")
        self.assertEqual(self.character.elemental_weakness, "")

        self.character.elemental_strength = "Resistant to fire"
        self.character.elemental_weakness = "Vulnerable to water"
        self.character.save()

        self.character.refresh_from_db()
        self.assertEqual(self.character.elemental_strength, "Resistant to fire")
        self.assertEqual(self.character.elemental_weakness, "Vulnerable to water")

    def test_multiple_mana_additions(self):
        """Test adding mana multiple times."""
        self.character.mana = 4
        for expected in range(5, 11):
            result = self.character.add_mana()
            self.assertTrue(result)
            self.assertEqual(self.character.mana, expected)

        # At max, should fail
        result = self.character.add_mana()
        self.assertFalse(result)
        self.assertEqual(self.character.mana, 10)

    def test_kingdoms_choices(self):
        """Test that KINGDOMS constant exists and has expected values."""
        kingdoms_dict = dict(Inanimae.KINGDOMS)
        self.assertIn("kubera", kingdoms_dict)
        self.assertIn("ondine", kingdoms_dict)
        self.assertIn("paroseme", kingdoms_dict)
        self.assertIn("sylph", kingdoms_dict)
        self.assertIn("salamander", kingdoms_dict)
        self.assertIn("solimond", kingdoms_dict)
        self.assertIn("mannikin", kingdoms_dict)

    def test_inanimae_seemings_choices(self):
        """Test that INANIMAE_SEEMINGS constant exists and has expected values."""
        seemings_dict = dict(Inanimae.INANIMAE_SEEMINGS)
        self.assertIn("glimmer", seemings_dict)
        self.assertIn("naturae", seemings_dict)
        self.assertIn("ancient", seemings_dict)

    def test_seasons_choices(self):
        """Test that SEASONS constant exists and has expected values."""
        seasons_dict = dict(Inanimae.SEASONS)
        self.assertIn("spring", seasons_dict)
        self.assertIn("summer", seasons_dict)
        self.assertIn("autumn", seasons_dict)
        self.assertIn("winter", seasons_dict)

    def test_gameline(self):
        """Test that gameline is set to ctd."""
        self.assertEqual(self.character.gameline, "ctd")

    def test_verbose_name(self):
        """Test model verbose names."""
        self.assertEqual(Inanimae._meta.verbose_name, "Inanimae")
        self.assertEqual(Inanimae._meta.verbose_name_plural, "Inanimae")
