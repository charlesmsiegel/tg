"""
Tests for Revenant and RevenantFamily models.

Tests cover:
- RevenantFamily creation and attributes
- Revenant creation and basic attributes
- Blood pool mechanics (natural vitae production)
- Pseudo-generation
- Family discipline access
- Family flaw tracking
"""

from characters.costs import get_freebie_cost
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.revenant import Revenant, RevenantFamily
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class RevenantModelTestCase(TestCase):
    """Base test case with common setup for Revenant model tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.fortitude = Discipline.objects.create(name="Fortitude", property_name="fortitude")
        cls.dominate = Discipline.objects.create(name="Dominate", property_name="dominate")
        cls.animalism = Discipline.objects.create(name="Animalism", property_name="animalism")
        cls.vicissitude = Discipline.objects.create(name="Vicissitude", property_name="vicissitude")

        # Create revenant families
        cls.bratovich = RevenantFamily.objects.create(
            name="Bratovich",
            description="Brutal overseers and enforcers",
            weakness="Sadistic tendencies",
        )
        cls.bratovich.disciplines.add(cls.potence, cls.fortitude, cls.vicissitude)

        cls.grimaldi = RevenantFamily.objects.create(
            name="Grimaldi",
            description="Diplomats and spies",
            weakness="Scheming nature",
        )
        cls.grimaldi.disciplines.add(cls.dominate, cls.fortitude, cls.celerity)

    def setUp(self):
        """Set up test user and character."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")


class TestRevenantFamilyCreation(RevenantModelTestCase):
    """Test RevenantFamily model creation and attributes."""

    def test_family_creation_basic(self):
        """Test basic revenant family creation."""
        family = RevenantFamily.objects.create(
            name="Test Family",
            description="A test family of revenants",
            weakness="Test weakness",
        )
        self.assertEqual(family.name, "Test Family")
        self.assertEqual(family.description, "A test family of revenants")
        self.assertEqual(family.weakness, "Test weakness")

    def test_family_str(self):
        """Test family string representation."""
        self.assertEqual(str(self.bratovich), "Bratovich")

    def test_family_has_disciplines(self):
        """Test that families can have disciplines."""
        disciplines = list(self.bratovich.disciplines.all())
        discipline_names = [d.name for d in disciplines]
        self.assertIn("Potence", discipline_names)
        self.assertIn("Fortitude", discipline_names)
        self.assertIn("Vicissitude", discipline_names)

    def test_family_get_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        expected_url = f"/characters/vampire/revenant_family/{self.bratovich.id}/"
        self.assertEqual(self.bratovich.get_absolute_url(), expected_url)

    def test_family_get_update_url(self):
        """Test that get_update_url returns correct path."""
        expected_url = f"/characters/vampire/update/revenant_family/{self.bratovich.pk}/"
        self.assertEqual(self.bratovich.get_update_url(), expected_url)

    def test_family_get_creation_url(self):
        """Test that get_creation_url returns correct path."""
        expected_url = "/characters/vampire/create/revenant_family/"
        self.assertEqual(RevenantFamily.get_creation_url(), expected_url)


class TestRevenantCreation(RevenantModelTestCase):
    """Test Revenant model creation and basic attributes."""

    def test_revenant_creation_basic(self):
        """Test basic revenant creation."""
        revenant = Revenant.objects.create(
            name="Test Revenant",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Family enforcer",
        )
        self.assertEqual(revenant.name, "Test Revenant")
        self.assertEqual(revenant.owner, self.user)
        self.assertEqual(revenant.concept, "Family enforcer")
        self.assertEqual(revenant.type, "revenant")

    def test_revenant_default_blood_pool(self):
        """Test that revenants default to 10 blood pool (natural vitae)."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertEqual(revenant.blood_pool, 10)
        self.assertEqual(revenant.max_blood_pool, 10)

    def test_revenant_default_pseudo_generation(self):
        """Test that pseudo_generation defaults to 10."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertEqual(revenant.pseudo_generation, 10)

    def test_revenant_can_have_family(self):
        """Test that a revenant can have a family."""
        revenant = Revenant.objects.create(
            name="Test",
            owner=self.user,
            family=self.bratovich,
        )
        self.assertEqual(revenant.family, self.bratovich)

    def test_revenant_get_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        expected_url = f"/characters/vampire/revenant/{revenant.id}/"
        self.assertEqual(revenant.get_absolute_url(), expected_url)

    def test_revenant_get_update_url(self):
        """Test that get_update_url returns correct path."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        expected_url = f"/characters/vampire/update/revenant/{revenant.pk}/"
        self.assertEqual(revenant.get_update_url(), expected_url)

    def test_revenant_get_creation_url(self):
        """Test that get_creation_url returns correct path."""
        expected_url = "/characters/vampire/create/revenant/"
        self.assertEqual(Revenant.get_creation_url(), expected_url)

    def test_revenant_get_heading(self):
        """Test that get_heading returns vtm_heading."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertEqual(revenant.get_heading(), "vtm_heading")


class TestRevenantDisciplines(RevenantModelTestCase):
    """Test discipline tracking and methods."""

    def test_get_disciplines_empty(self):
        """Test get_disciplines with no disciplines."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        disciplines = revenant.get_disciplines()
        self.assertEqual(disciplines, {})

    def test_get_disciplines_with_ratings(self):
        """Test get_disciplines returns only disciplines with ratings > 0."""
        revenant = Revenant.objects.create(
            name="Test",
            owner=self.user,
            potence=2,
            fortitude=1,
            celerity=0,  # Should not appear
        )
        disciplines = revenant.get_disciplines()
        self.assertEqual(disciplines, {"Potence": 2, "Fortitude": 1})
        self.assertNotIn("Celerity", disciplines)

    def test_get_family_disciplines_with_family(self):
        """Test get_family_disciplines returns family disciplines."""
        revenant = Revenant.objects.create(
            name="Test",
            owner=self.user,
            family=self.bratovich,
        )
        family_disciplines = revenant.get_family_disciplines()
        discipline_names = [d.name for d in family_disciplines]
        self.assertIn("Potence", discipline_names)
        self.assertIn("Fortitude", discipline_names)
        self.assertIn("Vicissitude", discipline_names)

    def test_get_family_disciplines_without_family(self):
        """Test get_family_disciplines returns empty list without family."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        family_disciplines = revenant.get_family_disciplines()
        self.assertEqual(family_disciplines, [])

    def test_get_available_disciplines_with_family(self):
        """Test get_available_disciplines returns family disciplines."""
        revenant = Revenant.objects.create(
            name="Test",
            owner=self.user,
            family=self.grimaldi,
        )
        available = revenant.get_available_disciplines()
        discipline_names = [d.name for d in available]
        self.assertIn("Dominate", discipline_names)
        self.assertIn("Fortitude", discipline_names)
        self.assertIn("Celerity", discipline_names)

    def test_get_available_disciplines_without_family(self):
        """Test get_available_disciplines returns physical without family."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        available = revenant.get_available_disciplines()
        discipline_names = [d.name for d in available]
        self.assertIn("Potence", discipline_names)
        self.assertIn("Celerity", discipline_names)
        self.assertIn("Fortitude", discipline_names)


class TestRevenantFreebies(RevenantModelTestCase):
    """Test freebie point costs."""

    def test_freebie_cost_discipline(self):
        """Test freebie cost for in-family disciplines."""
        self.assertEqual(get_freebie_cost("discipline"), 7)

    def test_freebie_step(self):
        """Test that revenants have freebie_step of 6."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertEqual(revenant.freebie_step, 6)


class TestRevenantAllowedBackgrounds(RevenantModelTestCase):
    """Test allowed backgrounds for revenants."""

    def test_allowed_backgrounds_includes_contacts(self):
        """Test that allowed_backgrounds includes contacts."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertIn("contacts", revenant.allowed_backgrounds)

    def test_allowed_backgrounds_includes_resources(self):
        """Test that allowed_backgrounds includes resources."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertIn("resources", revenant.allowed_backgrounds)

    def test_allowed_backgrounds_includes_generation(self):
        """Test that allowed_backgrounds includes generation (pseudo-generation)."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertIn("generation", revenant.allowed_backgrounds)

    def test_allowed_backgrounds_excludes_domain(self):
        """Test that allowed_backgrounds excludes domain."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertNotIn("domain", revenant.allowed_backgrounds)


class TestRevenantFamilyFlaw(RevenantModelTestCase):
    """Test family flaw tracking."""

    def test_family_flaw_can_be_set(self):
        """Test that family_flaw can be set."""
        revenant = Revenant.objects.create(
            name="Test",
            owner=self.user,
            family=self.bratovich,
            family_flaw="Enjoys causing pain",
        )
        self.assertEqual(revenant.family_flaw, "Enjoys causing pain")

    def test_family_flaw_defaults_empty(self):
        """Test that family_flaw defaults to empty string."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertEqual(revenant.family_flaw, "")


class TestRevenantAge(RevenantModelTestCase):
    """Test age tracking for revenants."""

    def test_actual_age_default(self):
        """Test that actual_age defaults to 0."""
        revenant = Revenant.objects.create(name="Test", owner=self.user)
        self.assertEqual(revenant.actual_age, 0)

    def test_actual_age_can_be_set(self):
        """Test that actual_age can be set."""
        revenant = Revenant.objects.create(
            name="Ancient Revenant",
            owner=self.user,
            actual_age=200,
        )
        self.assertEqual(revenant.actual_age, 200)


class TestRevenantFamilyRevenants(RevenantModelTestCase):
    """Test family-revenants relationship."""

    def test_family_can_have_revenants(self):
        """Test that revenants relationship is accessible from family."""
        rev1 = Revenant.objects.create(
            name="Rev 1",
            owner=self.user,
            family=self.bratovich,
        )
        rev2 = Revenant.objects.create(
            name="Rev 2",
            owner=self.user,
            family=self.bratovich,
        )
        revenants = list(self.bratovich.revenants.all())
        self.assertEqual(len(revenants), 2)
        self.assertIn(rev1, revenants)
        self.assertIn(rev2, revenants)
