"""
Tests for VampireFreebiesForm and GhoulFreebiesForm.

Tests cover:
- Form initialization with vampire/ghoul instance
- Category choices including vampire-specific options
- Validator method for checking freebie costs
- Discipline queryset population
- Form validation for different categories
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.vampire.freebies import (
    VAMPIRE_CATEGORY_CHOICES,
    GhoulFreebiesForm,
    VampireFreebiesForm,
)
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire


class VampireFreebiesFormTestCase(TestCase):
    """Base test case with common setup for VampireFreebiesForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.presence = Discipline.objects.create(name="Presence", property_name="presence")
        cls.dominate = Discipline.objects.create(name="Dominate", property_name="dominate")

        # Create clan
        cls.brujah = VampireClan.objects.create(
            name="Brujah",
            nickname="Rabble",
        )
        cls.brujah.disciplines.add(cls.potence, cls.celerity, cls.presence)

    def setUp(self):
        """Set up test user and character."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            freebies=15,
        )


class TestVampireCategoryChoices(VampireFreebiesFormTestCase):
    """Test vampire-specific category choices."""

    def test_vampire_category_choices_includes_discipline(self):
        """VAMPIRE_CATEGORY_CHOICES includes Discipline option."""
        category_values = [choice[0] for choice in VAMPIRE_CATEGORY_CHOICES]
        self.assertIn("Discipline", category_values)

    def test_vampire_category_choices_includes_virtue(self):
        """VAMPIRE_CATEGORY_CHOICES includes Virtue option."""
        category_values = [choice[0] for choice in VAMPIRE_CATEGORY_CHOICES]
        self.assertIn("Virtue", category_values)

    def test_vampire_category_choices_includes_humanity(self):
        """VAMPIRE_CATEGORY_CHOICES includes Humanity option."""
        category_values = [choice[0] for choice in VAMPIRE_CATEGORY_CHOICES]
        self.assertIn("Humanity", category_values)

    def test_vampire_category_choices_includes_path_rating(self):
        """VAMPIRE_CATEGORY_CHOICES includes Path Rating option."""
        category_values = [choice[0] for choice in VAMPIRE_CATEGORY_CHOICES]
        self.assertIn("Path Rating", category_values)


class TestVampireFreebiesFormInitialization(VampireFreebiesFormTestCase):
    """Test form initialization."""

    def test_form_initializes_with_instance(self):
        """Form initializes correctly with vampire instance."""
        form = VampireFreebiesForm(instance=self.vampire)
        self.assertEqual(form.instance, self.vampire)

    def test_form_filters_unaffordable_categories(self):
        """Form filters out categories the vampire cannot afford."""
        self.vampire.freebies = 5
        self.vampire.save()

        form = VampireFreebiesForm(instance=self.vampire)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        # Should include Attribute (cost 5)
        self.assertIn("Attribute", category_values)

    def test_form_includes_base_categories_with_sufficient_freebies(self):
        """Form includes base categories when vampire has enough freebies."""
        self.vampire.freebies = 15
        self.vampire.save()

        form = VampireFreebiesForm(instance=self.vampire)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        # Base categories from HumanFreebiesForm should be present
        self.assertIn("Attribute", category_values)
        self.assertIn("Ability", category_values)
        self.assertIn("Willpower", category_values)


class TestVampireFreebiesFormValidator(VampireFreebiesFormTestCase):
    """Test validator method for category affordability."""

    def test_validator_returns_true_for_affordable_discipline(self):
        """Validator returns True when vampire can afford disciplines."""
        self.vampire.freebies = 10
        self.vampire.save()

        form = VampireFreebiesForm(instance=self.vampire)
        # Discipline costs 7, should be affordable with 10 freebies
        self.assertTrue(form.validator("Discipline"))

    def test_validator_returns_false_for_unaffordable_discipline(self):
        """Validator returns False when vampire cannot afford disciplines."""
        self.vampire.freebies = 5
        self.vampire.save()

        form = VampireFreebiesForm(instance=self.vampire)
        # Discipline costs 7, should not be affordable with 5 freebies
        self.assertFalse(form.validator("Discipline"))

    def test_validator_returns_true_for_affordable_virtue(self):
        """Validator returns True when vampire can afford virtues."""
        self.vampire.freebies = 3
        self.vampire.save()

        form = VampireFreebiesForm(instance=self.vampire)
        # Virtue costs 2, should be affordable with 3 freebies
        self.assertTrue(form.validator("Virtue"))

    def test_validator_returns_true_for_affordable_humanity(self):
        """Validator returns True when vampire can afford humanity."""
        self.vampire.freebies = 2
        self.vampire.save()

        form = VampireFreebiesForm(instance=self.vampire)
        # Humanity costs 1, should be affordable with 2 freebies
        self.assertTrue(form.validator("Humanity"))

    def test_validator_returns_true_for_affordable_path_rating(self):
        """Validator returns True when vampire can afford path rating."""
        self.vampire.freebies = 2
        self.vampire.save()

        form = VampireFreebiesForm(instance=self.vampire)
        # Path Rating costs 2, should be affordable with 2 freebies
        self.assertTrue(form.validator("Path Rating"))


class TestVampireFreebiesFormBoundData(VampireFreebiesFormTestCase):
    """Test form behavior when bound with data."""

    def test_discipline_queryset_populated_when_bound(self):
        """Discipline queryset includes all disciplines when form is bound."""
        form = VampireFreebiesForm(
            data={"category": "Discipline", "example": "", "value": ""},
            instance=self.vampire,
        )
        example_qs = form.fields["example"].queryset
        self.assertIn(self.potence, example_qs)
        self.assertIn(self.dominate, example_qs)


class TestVampireFreebiesFormSave(VampireFreebiesFormTestCase):
    """Test form save functionality."""

    def test_save_returns_instance(self):
        """Saving form returns the character instance."""
        form = VampireFreebiesForm(
            data={"category": "Discipline", "example": "", "value": ""},
            instance=self.vampire,
        )
        result = form.save()
        self.assertEqual(result, self.vampire)


class GhoulFreebiesFormTestCase(TestCase):
    """Base test case with common setup for GhoulFreebiesForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.fortitude = Discipline.objects.create(name="Fortitude", property_name="fortitude")

    def setUp(self):
        """Set up test user and character."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            freebies=15,
        )


class TestGhoulFreebiesFormInitialization(GhoulFreebiesFormTestCase):
    """Test form initialization."""

    def test_form_initializes_with_instance(self):
        """Form initializes correctly with ghoul instance."""
        form = GhoulFreebiesForm(instance=self.ghoul)
        self.assertEqual(form.instance, self.ghoul)

    def test_form_includes_base_categories(self):
        """Form includes base categories for ghouls."""
        form = GhoulFreebiesForm(instance=self.ghoul)
        category_values = [choice[0] for choice in form.fields["category"].choices]
        # Base categories from HumanFreebiesForm should be present
        self.assertIn("Attribute", category_values)
        self.assertIn("Ability", category_values)

    def test_form_excludes_vampire_specific_categories(self):
        """Form excludes vampire-specific categories like Virtue, Humanity."""
        form = GhoulFreebiesForm(instance=self.ghoul)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        # Ghouls shouldn't have Virtue, Humanity, Path Rating categories
        self.assertNotIn("Virtue", category_values)
        self.assertNotIn("Humanity", category_values)
        self.assertNotIn("Path Rating", category_values)


class TestGhoulFreebiesFormValidator(GhoulFreebiesFormTestCase):
    """Test validator method for category affordability."""

    def test_validator_returns_true_for_affordable_discipline(self):
        """Validator returns True when ghoul can afford disciplines."""
        self.ghoul.freebies = 10
        self.ghoul.save()

        form = GhoulFreebiesForm(instance=self.ghoul)
        # Discipline costs 7 for ghouls, should be affordable with 10 freebies
        self.assertTrue(form.validator("Discipline"))

    def test_validator_returns_false_for_unaffordable_discipline(self):
        """Validator returns False when ghoul cannot afford disciplines."""
        self.ghoul.freebies = 5
        self.ghoul.save()

        form = GhoulFreebiesForm(instance=self.ghoul)
        # Discipline costs 7, should not be affordable with 5 freebies
        self.assertFalse(form.validator("Discipline"))


class TestGhoulFreebiesFormBoundData(GhoulFreebiesFormTestCase):
    """Test form behavior when bound with data."""

    def test_discipline_queryset_populated_when_bound(self):
        """Discipline queryset includes all disciplines when form is bound."""
        form = GhoulFreebiesForm(
            data={"category": "Discipline", "example": "", "value": ""},
            instance=self.ghoul,
        )
        example_qs = form.fields["example"].queryset
        self.assertIn(self.potence, example_qs)
        self.assertIn(self.celerity, example_qs)


class TestGhoulFreebiesFormSave(GhoulFreebiesFormTestCase):
    """Test form save functionality."""

    def test_save_returns_instance(self):
        """Saving form returns the character instance."""
        form = GhoulFreebiesForm(
            data={"category": "Discipline", "example": "", "value": ""},
            instance=self.ghoul,
        )
        result = form.save()
        self.assertEqual(result, self.ghoul)
