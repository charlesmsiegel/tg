"""Tests for DtFHuman model."""

from characters.models.demon.dtf_human import DtFHuman
from django.contrib.auth.models import User
from django.test import TestCase


class DtFHumanModelTests(TestCase):
    """Tests for DtFHuman model functionality."""

    def setUp(self):
        """Create a test user for character ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.human = DtFHuman.objects.create(name="Test Human", owner=self.user)

    def test_type_is_dtf_human(self):
        """Test that type is 'dtf_human'."""
        self.assertEqual(self.human.type, "dtf_human")

    def test_gameline_is_dtf(self):
        """Test that gameline is 'dtf'."""
        self.assertEqual(self.human.gameline, "dtf")

    def test_freebie_step_is_five(self):
        """Test that freebie_step is 5."""
        self.assertEqual(DtFHuman.freebie_step, 5)

    def test_background_points_is_five(self):
        """Test that background_points is 5."""
        self.assertEqual(self.human.background_points, 5)

    def test_ordering_by_name(self):
        """DtFHumans should be ordered by name by default."""
        human_c = DtFHuman.objects.create(name="Charlie", owner=self.user)
        human_a = DtFHuman.objects.create(name="Alice", owner=self.user)
        human_b = DtFHuman.objects.create(name="Bob", owner=self.user)

        humans = list(DtFHuman.objects.exclude(pk=self.human.pk))

        self.assertEqual(humans[0], human_a)
        self.assertEqual(humans[1], human_b)
        self.assertEqual(humans[2], human_c)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.human.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/dtfhuman/{self.human.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.human.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/dtfhuman/{self.human.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = DtFHuman.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/dtfhuman/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.human.get_heading(), "dtf_heading")


class DtFHumanAllowedBackgroundsTests(TestCase):
    """Tests for DtFHuman allowed backgrounds."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.human = DtFHuman.objects.create(name="Test Human", owner=self.user)

    def test_allowed_backgrounds_contains_expected_items(self):
        """Test that allowed_backgrounds contains expected items."""
        expected = [
            "contacts",
            "mentor",
            "allies",
            "eminence",
            "fame",
            "followers",
            "influence",
            "legacy",
            "pacts",
            "paragon",
            "resources",
        ]
        self.assertEqual(DtFHuman.allowed_backgrounds, expected)

    def test_allowed_backgrounds_has_eleven_items(self):
        """Test that allowed_backgrounds has 11 items."""
        self.assertEqual(len(DtFHuman.allowed_backgrounds), 11)


class DtFHumanAbilitiesTests(TestCase):
    """Tests for DtFHuman ability lists and fields."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.human = DtFHuman.objects.create(name="Test Human", owner=self.user)

    def test_talents_has_twelve_items(self):
        """Test that talents list has 12 items."""
        self.assertEqual(len(DtFHuman.talents), 12)

    def test_skills_has_twelve_items(self):
        """Test that skills list has 12 items."""
        self.assertEqual(len(DtFHuman.skills), 12)

    def test_knowledges_has_twelve_items(self):
        """Test that knowledges list has 12 items."""
        self.assertEqual(len(DtFHuman.knowledges), 12)

    def test_primary_abilities_has_36_items(self):
        """Test that primary_abilities combines all ability lists."""
        self.assertEqual(len(DtFHuman.primary_abilities), 36)

    def test_demon_specific_talents_included(self):
        """Test that Demon-specific talents are in the list."""
        demon_talents = ["awareness", "intuition", "leadership", "seduction"]
        for talent in demon_talents:
            self.assertIn(talent, DtFHuman.talents)

    def test_demon_specific_skills_included(self):
        """Test that Demon-specific skills are in the list."""
        demon_skills = ["performance", "security", "survival", "technology", "animal_ken", "demolitions"]
        for skill in demon_skills:
            self.assertIn(skill, DtFHuman.skills)

    def test_demon_specific_knowledges_included(self):
        """Test that Demon-specific knowledges are in the list."""
        demon_knowledges = ["finance", "law", "enigmas", "occult", "politics", "religion", "research"]
        for knowledge in demon_knowledges:
            self.assertIn(knowledge, DtFHuman.knowledges)


class DtFHumanAbilityFieldsTests(TestCase):
    """Tests for DtFHuman ability fields have correct defaults."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.human = DtFHuman.objects.create(name="Test Human", owner=self.user)

    def test_awareness_default_zero(self):
        """Test awareness defaults to 0."""
        self.assertEqual(self.human.awareness, 0)

    def test_intuition_default_zero(self):
        """Test intuition defaults to 0."""
        self.assertEqual(self.human.intuition, 0)

    def test_leadership_default_zero(self):
        """Test leadership defaults to 0."""
        self.assertEqual(self.human.leadership, 0)

    def test_seduction_default_zero(self):
        """Test seduction defaults to 0."""
        self.assertEqual(self.human.seduction, 0)

    def test_performance_default_zero(self):
        """Test performance defaults to 0."""
        self.assertEqual(self.human.performance, 0)

    def test_security_default_zero(self):
        """Test security defaults to 0."""
        self.assertEqual(self.human.security, 0)

    def test_survival_default_zero(self):
        """Test survival defaults to 0."""
        self.assertEqual(self.human.survival, 0)

    def test_technology_default_zero(self):
        """Test technology defaults to 0."""
        self.assertEqual(self.human.technology, 0)

    def test_animal_ken_default_zero(self):
        """Test animal_ken defaults to 0."""
        self.assertEqual(self.human.animal_ken, 0)

    def test_demolitions_default_zero(self):
        """Test demolitions defaults to 0."""
        self.assertEqual(self.human.demolitions, 0)

    def test_finance_default_zero(self):
        """Test finance defaults to 0."""
        self.assertEqual(self.human.finance, 0)

    def test_law_default_zero(self):
        """Test law defaults to 0."""
        self.assertEqual(self.human.law, 0)

    def test_enigmas_default_zero(self):
        """Test enigmas defaults to 0."""
        self.assertEqual(self.human.enigmas, 0)

    def test_occult_default_zero(self):
        """Test occult defaults to 0."""
        self.assertEqual(self.human.occult, 0)

    def test_politics_default_zero(self):
        """Test politics defaults to 0."""
        self.assertEqual(self.human.politics, 0)

    def test_religion_default_zero(self):
        """Test religion defaults to 0."""
        self.assertEqual(self.human.religion, 0)

    def test_research_default_zero(self):
        """Test research defaults to 0."""
        self.assertEqual(self.human.research, 0)


class DtFHumanVerboseNameTests(TestCase):
    """Tests for DtFHuman verbose names."""

    def test_verbose_name(self):
        """Test verbose_name is correct."""
        self.assertEqual(DtFHuman._meta.verbose_name, "Human (Demon)")

    def test_verbose_name_plural(self):
        """Test verbose_name_plural is correct."""
        self.assertEqual(DtFHuman._meta.verbose_name_plural, "Humans (Demon)")
