"""
Tests for Ghoul model.

Tests cover:
- Ghoul creation and basic attributes
- Blood pool limitations
- Domitor relationship
- Discipline tracking and costs
- Independent ghoul mechanics
"""

from characters.costs import get_freebie_cost
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class GhoulModelTestCase(TestCase):
    """Base test case with common setup for Ghoul model tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.fortitude = Discipline.objects.create(name="Fortitude", property_name="fortitude")
        cls.dominate = Discipline.objects.create(name="Dominate", property_name="dominate")
        cls.presence = Discipline.objects.create(name="Presence", property_name="presence")

        # Create a clan
        cls.ventrue = VampireClan.objects.create(
            name="Ventrue",
            nickname="Blue Bloods",
        )
        cls.ventrue.disciplines.add(cls.dominate, cls.fortitude, cls.presence)

    def setUp(self):
        """Set up test user and character."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create a domitor vampire
        self.domitor = Vampire.objects.create(
            name="Lord Ventrue",
            owner=self.user,
            clan=self.ventrue,
            generation_rating=9,
        )


class TestGhoulCreation(GhoulModelTestCase):
    """Test Ghoul model creation and basic attributes."""

    def test_ghoul_creation_basic(self):
        """Test basic ghoul creation."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Bodyguard",
        )
        self.assertEqual(ghoul.name, "Test Ghoul")
        self.assertEqual(ghoul.owner, self.user)
        self.assertEqual(ghoul.concept, "Bodyguard")
        self.assertEqual(ghoul.type, "ghoul")

    def test_ghoul_default_blood_pool(self):
        """Test that ghouls default to limited blood pool."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertEqual(ghoul.blood_pool, 0)
        self.assertEqual(ghoul.max_blood_pool, 2)

    def test_ghoul_default_potence(self):
        """Test that ghouls start with 1 dot of Potence."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertEqual(ghoul.potence, 1)

    def test_ghoul_default_other_disciplines(self):
        """Test that ghouls default to 0 in other disciplines."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertEqual(ghoul.celerity, 0)
        self.assertEqual(ghoul.fortitude, 0)
        self.assertEqual(ghoul.auspex, 0)
        self.assertEqual(ghoul.dominate, 0)
        self.assertEqual(ghoul.obfuscate, 0)
        self.assertEqual(ghoul.presence, 0)

    def test_ghoul_get_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        expected_url = f"/characters/vampire/ghoul/{ghoul.id}/"
        self.assertEqual(ghoul.get_absolute_url(), expected_url)

    def test_ghoul_get_update_url(self):
        """Test that get_update_url returns correct path."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        expected_url = f"/characters/vampire/update/ghoul/{ghoul.pk}/"
        self.assertEqual(ghoul.get_update_url(), expected_url)

    def test_ghoul_get_creation_url(self):
        """Test that get_creation_url returns correct path."""
        expected_url = "/characters/vampire/create/ghoul/"
        self.assertEqual(Ghoul.get_creation_url(), expected_url)

    def test_ghoul_get_heading(self):
        """Test that get_heading returns vtm_heading."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertEqual(ghoul.get_heading(), "vtm_heading")


class TestGhoulDomitor(GhoulModelTestCase):
    """Test domitor relationship mechanics."""

    def test_ghoul_can_have_domitor(self):
        """Test that a ghoul can have a domitor."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            domitor=self.domitor,
        )
        self.assertEqual(ghoul.domitor, self.domitor)

    def test_domitor_can_have_ghouls(self):
        """Test that ghouls relationship is accessible from domitor."""
        ghoul1 = Ghoul.objects.create(
            name="Ghoul 1",
            owner=self.user,
            domitor=self.domitor,
        )
        ghoul2 = Ghoul.objects.create(
            name="Ghoul 2",
            owner=self.user,
            domitor=self.domitor,
        )
        ghouls = list(self.domitor.ghouls.all())
        self.assertEqual(len(ghouls), 2)
        self.assertIn(ghoul1, ghouls)
        self.assertIn(ghoul2, ghouls)

    def test_ghoul_can_be_independent(self):
        """Test that a ghoul can be independent."""
        ghoul = Ghoul.objects.create(
            name="Independent Ghoul",
            owner=self.user,
            is_independent=True,
        )
        self.assertTrue(ghoul.is_independent)
        self.assertIsNone(ghoul.domitor)

    def test_ghoul_independent_default_false(self):
        """Test that is_independent defaults to False."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertFalse(ghoul.is_independent)


class TestGhoulDisciplines(GhoulModelTestCase):
    """Test discipline tracking and methods."""

    def test_get_disciplines_includes_potence(self):
        """Test get_disciplines includes default Potence."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        disciplines = ghoul.get_disciplines()
        self.assertEqual(disciplines, {"Potence": 1})

    def test_get_disciplines_with_multiple_ratings(self):
        """Test get_disciplines returns only disciplines with ratings > 0."""
        ghoul = Ghoul.objects.create(
            name="Test",
            owner=self.user,
            potence=2,
            celerity=1,
            fortitude=0,  # Should not appear
        )
        disciplines = ghoul.get_disciplines()
        self.assertEqual(disciplines, {"Potence": 2, "Celerity": 1})
        self.assertNotIn("Fortitude", disciplines)

    def test_get_available_disciplines_with_domitor(self):
        """Test get_available_disciplines returns domitor's clan disciplines."""
        ghoul = Ghoul.objects.create(
            name="Test",
            owner=self.user,
            domitor=self.domitor,
        )
        available = ghoul.get_available_disciplines()
        discipline_names = [d.name for d in available]
        self.assertIn("Dominate", discipline_names)
        self.assertIn("Fortitude", discipline_names)
        self.assertIn("Presence", discipline_names)

    def test_get_available_disciplines_independent(self):
        """Test get_available_disciplines returns physical for independent ghouls."""
        ghoul = Ghoul.objects.create(
            name="Test",
            owner=self.user,
            is_independent=True,
        )
        available = ghoul.get_available_disciplines()
        discipline_names = [d.name for d in available]
        self.assertIn("Potence", discipline_names)
        self.assertIn("Celerity", discipline_names)
        self.assertIn("Fortitude", discipline_names)

    def test_get_available_disciplines_no_domitor(self):
        """Test get_available_disciplines returns physical without domitor."""
        ghoul = Ghoul.objects.create(
            name="Test",
            owner=self.user,
        )
        available = ghoul.get_available_disciplines()
        discipline_names = [d.name for d in available]
        self.assertIn("Potence", discipline_names)
        self.assertIn("Celerity", discipline_names)
        self.assertIn("Fortitude", discipline_names)


class TestGhoulFreebies(GhoulModelTestCase):
    """Test freebie point costs."""

    def test_freebie_cost_discipline(self):
        """Test freebie cost for disciplines."""
        self.assertEqual(get_freebie_cost("discipline"), 7)

    def test_freebie_step(self):
        """Test that ghouls have freebie_step of 6."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertEqual(ghoul.freebie_step, 6)


class TestGhoulAllowedBackgrounds(GhoulModelTestCase):
    """Test allowed backgrounds for ghouls."""

    def test_allowed_backgrounds_includes_contacts(self):
        """Test that allowed_backgrounds includes contacts."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertIn("contacts", ghoul.allowed_backgrounds)

    def test_allowed_backgrounds_includes_mentor(self):
        """Test that allowed_backgrounds includes mentor."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertIn("mentor", ghoul.allowed_backgrounds)

    def test_allowed_backgrounds_includes_resources(self):
        """Test that allowed_backgrounds includes resources."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertIn("resources", ghoul.allowed_backgrounds)

    def test_allowed_backgrounds_excludes_generation(self):
        """Test that allowed_backgrounds excludes generation (vampire only)."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertNotIn("generation", ghoul.allowed_backgrounds)

    def test_allowed_backgrounds_excludes_domain(self):
        """Test that allowed_backgrounds excludes domain (vampire only)."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertNotIn("domain", ghoul.allowed_backgrounds)


class TestGhoulYearsAsGhoul(GhoulModelTestCase):
    """Test years as ghoul tracking."""

    def test_years_as_ghoul_default(self):
        """Test that years_as_ghoul defaults to 0."""
        ghoul = Ghoul.objects.create(name="Test", owner=self.user)
        self.assertEqual(ghoul.years_as_ghoul, 0)

    def test_years_as_ghoul_can_be_set(self):
        """Test that years_as_ghoul can be set."""
        ghoul = Ghoul.objects.create(
            name="Ancient Ghoul",
            owner=self.user,
            years_as_ghoul=150,
        )
        self.assertEqual(ghoul.years_as_ghoul, 150)
