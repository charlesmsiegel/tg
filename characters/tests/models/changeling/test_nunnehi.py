"""Tests for Nunnehi model."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.changeling.nunnehi import Nunnehi


class TestNunnehi(TestCase):
    """Tests for Nunnehi model methods."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        # Provide required fields for Nunnehi
        self.character = Nunnehi.objects.create(
            owner=self.player,
            name="Test Nunnehi",
            tribe="kachina",
            nunnehi_seeming="kohedan",
            path="warrior",
        )

    def test_nunnehi_creation(self):
        """Test basic creation of a Nunnehi."""
        self.assertEqual(self.character.name, "Test Nunnehi")
        self.assertEqual(self.character.type, "nunnehi")

    def test_has_tribe(self):
        """Test has_tribe method."""
        self.assertTrue(self.character.has_tribe())
        self.character.tribe = ""
        self.assertFalse(self.character.has_tribe())

    def test_set_tribe(self):
        """Test setting tribe."""
        result = self.character.set_tribe("yunwi_tsundi")
        self.assertTrue(result)
        self.assertEqual(self.character.tribe, "yunwi_tsundi")
        self.assertTrue(self.character.has_tribe())

    def test_set_tribe_all_types(self):
        """Test setting all tribe types."""
        tribes = [
            "may_may_gway_shi",  # Water dwellers
            "yunwi_tsundi",  # Little People of Cherokee
            "canotina",  # Tree spirits
            "kachina",  # Spirit dancers
            "nanehi",  # Pathfinders
            "nunnehi_proper",  # Cherokee immortals
            "other",  # Other tribal spirits
        ]
        for tribe in tribes:
            result = self.character.set_tribe(tribe)
            self.assertTrue(result)
            self.assertEqual(self.character.tribe, tribe)

    def test_has_path(self):
        """Test has_path method."""
        self.assertTrue(self.character.has_path())
        self.character.path = ""
        self.assertFalse(self.character.has_path())

    def test_set_path(self):
        """Test setting path."""
        result = self.character.set_path("healer")
        self.assertTrue(result)
        self.assertEqual(self.character.path, "healer")
        self.assertTrue(self.character.has_path())

    def test_set_path_all_types(self):
        """Test setting all path types."""
        paths = ["warrior", "healer", "sage", "trickster"]
        for path in paths:
            result = self.character.set_path(path)
            self.assertTrue(result)
            self.assertEqual(self.character.path, path)

    def test_has_nunnehi_seeming(self):
        """Test has_nunnehi_seeming method."""
        self.assertTrue(self.character.has_nunnehi_seeming())
        self.character.nunnehi_seeming = ""
        self.assertFalse(self.character.has_nunnehi_seeming())

    def test_set_nunnehi_seeming_katchina(self):
        """Test setting katchina seeming increases spirit medicine."""
        result = self.character.set_nunnehi_seeming("katchina")
        self.assertTrue(result)
        self.assertEqual(self.character.nunnehi_seeming, "katchina")
        self.assertEqual(self.character.spirit_medicine, 5)  # Young and energetic
        self.assertTrue(self.character.has_nunnehi_seeming())

    def test_set_nunnehi_seeming_kohedan(self):
        """Test setting kohedan seeming gives default spirit medicine."""
        result = self.character.set_nunnehi_seeming("kohedan")
        self.assertTrue(result)
        self.assertEqual(self.character.nunnehi_seeming, "kohedan")
        self.assertEqual(self.character.spirit_medicine, 4)  # Mature, balanced
        self.assertTrue(self.character.has_nunnehi_seeming())

    def test_set_nunnehi_seeming_kurganegh(self):
        """Test setting kurganegh seeming decreases spirit medicine."""
        result = self.character.set_nunnehi_seeming("kurganegh")
        self.assertTrue(result)
        self.assertEqual(self.character.nunnehi_seeming, "kurganegh")
        self.assertEqual(self.character.spirit_medicine, 3)  # Elder, less raw power
        self.assertTrue(self.character.has_nunnehi_seeming())

    def test_add_spirit_medicine(self):
        """Test adding spirit medicine."""
        initial_medicine = self.character.spirit_medicine
        result = self.character.add_spirit_medicine()
        self.assertTrue(result)
        self.assertEqual(self.character.spirit_medicine, initial_medicine + 1)

    def test_add_spirit_medicine_at_max(self):
        """Test that add_spirit_medicine fails at maximum (10)."""
        self.character.spirit_medicine = 10
        result = self.character.add_spirit_medicine()
        self.assertFalse(result)
        self.assertEqual(self.character.spirit_medicine, 10)

    def test_has_sacred_place(self):
        """Test has_sacred_place method."""
        self.assertFalse(self.character.has_sacred_place())
        self.character.sacred_place = "An ancient burial mound"
        self.assertTrue(self.character.has_sacred_place())

    def test_set_sacred_place(self):
        """Test setting sacred place."""
        self.assertFalse(self.character.has_sacred_place())
        result = self.character.set_sacred_place("The Great Smoky Mountains")
        self.assertTrue(result)
        self.assertEqual(self.character.sacred_place, "The Great Smoky Mountains")
        self.assertTrue(self.character.has_sacred_place())

    def test_has_spirit_guide(self):
        """Test has_spirit_guide method."""
        self.assertFalse(self.character.has_spirit_guide())
        self.character.spirit_guide = "Raven"
        self.assertTrue(self.character.has_spirit_guide())

    def test_set_spirit_guide(self):
        """Test setting spirit guide."""
        self.assertFalse(self.character.has_spirit_guide())
        result = self.character.set_spirit_guide("Bear Spirit")
        self.assertTrue(result)
        self.assertEqual(self.character.spirit_guide, "Bear Spirit")
        self.assertTrue(self.character.has_spirit_guide())

    def test_has_tribal_duty(self):
        """Test has_tribal_duty method."""
        self.assertFalse(self.character.has_tribal_duty())
        self.character.tribal_duty = "Protect the sacred lands"
        self.assertTrue(self.character.has_tribal_duty())

    def test_set_tribal_duty(self):
        """Test setting tribal duty."""
        self.assertFalse(self.character.has_tribal_duty())
        result = self.character.set_tribal_duty("Guide lost travelers to safety")
        self.assertTrue(result)
        self.assertEqual(self.character.tribal_duty, "Guide lost travelers to safety")
        self.assertTrue(self.character.has_tribal_duty())

    def test_multiple_spirit_medicine_additions(self):
        """Test adding spirit medicine multiple times."""
        self.character.spirit_medicine = 4
        for expected in range(5, 11):
            result = self.character.add_spirit_medicine()
            self.assertTrue(result)
            self.assertEqual(self.character.spirit_medicine, expected)

        # At max, should fail
        result = self.character.add_spirit_medicine()
        self.assertFalse(result)
        self.assertEqual(self.character.spirit_medicine, 10)

    def test_tribes_choices(self):
        """Test that TRIBES constant exists and has expected values."""
        tribes_dict = dict(Nunnehi.TRIBES)
        self.assertIn("may_may_gway_shi", tribes_dict)
        self.assertIn("yunwi_tsundi", tribes_dict)
        self.assertIn("canotina", tribes_dict)
        self.assertIn("kachina", tribes_dict)
        self.assertIn("nanehi", tribes_dict)
        self.assertIn("nunnehi_proper", tribes_dict)
        self.assertIn("other", tribes_dict)

    def test_nunnehi_seemings_choices(self):
        """Test that NUNNEHI_SEEMINGS constant exists and has expected values."""
        seemings_dict = dict(Nunnehi.NUNNEHI_SEEMINGS)
        self.assertIn("katchina", seemings_dict)
        self.assertIn("kohedan", seemings_dict)
        self.assertIn("kurganegh", seemings_dict)

    def test_path_choices(self):
        """Test that PATH_CHOICES constant exists and has expected values."""
        paths_dict = dict(Nunnehi.PATH_CHOICES)
        self.assertIn("warrior", paths_dict)
        self.assertIn("healer", paths_dict)
        self.assertIn("sage", paths_dict)
        self.assertIn("trickster", paths_dict)

    def test_gameline(self):
        """Test that gameline is set to ctd."""
        self.assertEqual(self.character.gameline, "ctd")

    def test_verbose_name(self):
        """Test model verbose names."""
        self.assertEqual(Nunnehi._meta.verbose_name, "Nunnehi")
        self.assertEqual(Nunnehi._meta.verbose_name_plural, "Nunnehi")
