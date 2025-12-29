"""Comprehensive tests for mage freebie forms."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.mage.freebies import (
    CompanionFreebiesForm,
    MageFreebiesForm,
    SorcererFreebiesForm,
)
from characters.models.core.ability_block import Ability
from characters.models.mage.companion import Companion
from characters.models.mage.focus import Practice
from characters.models.mage.mage import Mage
from characters.models.mage.resonance import Resonance
from characters.models.mage.sorcerer import LinearMagicPath, Sorcerer
from characters.models.mage.sphere import Sphere
from characters.tests.utils import mage_setup


class TestMageFreebiesForm(TestCase):
    """Test MageFreebiesForm."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.player,
            arete=2,
            freebies=21,
        )

    def test_form_initialization(self):
        """Test form initializes correctly."""
        form = MageFreebiesForm(instance=self.mage)
        self.assertIn("category", form.fields)
        self.assertIn("resonance", form.fields)

    def test_form_category_choices_include_mage_options(self):
        """Test form includes mage-specific category choices."""
        form = MageFreebiesForm(instance=self.mage)
        choices = [c[0] for c in form.fields["category"].choices]
        # Sphere requires 7 freebies
        self.assertIn("Sphere", choices)

    def test_form_excludes_arete_when_at_max(self):
        """Test Arete excluded when at character creation max."""
        self.mage.arete = 3
        self.mage.save()
        form = MageFreebiesForm(instance=self.mage)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertNotIn("Arete", choices)

    def test_form_excludes_sphere_when_not_enough_freebies(self):
        """Test Sphere excluded when not enough freebies."""
        self.mage.freebies = 5
        self.mage.save()
        form = MageFreebiesForm(instance=self.mage)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertNotIn("Sphere", choices)

    def test_form_excludes_resonance_when_not_enough_freebies(self):
        """Test Resonance excluded when not enough freebies."""
        self.mage.freebies = 2
        self.mage.save()
        form = MageFreebiesForm(instance=self.mage)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertNotIn("Resonance", choices)

    def test_form_bound_sphere_category(self):
        """Test form bound with Sphere category."""
        sphere = Sphere.objects.first()
        form = MageFreebiesForm(
            instance=self.mage,
            data={
                "category": "Sphere",
                "example": sphere.id,
                "value": "",
                "note": "",
            }
        )
        self.assertIsNotNone(form.fields["example"].queryset)

    def test_form_save_returns_instance(self):
        """Test form save returns the instance."""
        form = MageFreebiesForm(instance=self.mage)
        form.is_bound = False
        result = form.save()
        self.assertEqual(result, self.mage)

    def test_form_with_suggestions(self):
        """Test form with custom suggestions."""
        suggestions = ["Test1", "Test2"]
        form = MageFreebiesForm(instance=self.mage, suggestions=suggestions)
        self.assertEqual(form.fields["resonance"].widget.suggestions, suggestions)


class TestSorcererFreebiesForm(TestCase):
    """Test SorcererFreebiesForm."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.player,
            sorcerer_type="hedge_mage",
            freebies=21,
            willpower=5,
        )

    def test_form_initialization(self):
        """Test form initializes correctly."""
        form = SorcererFreebiesForm(instance=self.sorcerer)
        self.assertIn("category", form.fields)
        self.assertIn("practice", form.fields)
        self.assertIn("ability", form.fields)

    def test_form_includes_path_options_for_hedge_mage(self):
        """Test form includes path options for hedge mages."""
        form = SorcererFreebiesForm(instance=self.sorcerer)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertIn("Existing Path", choices)
        self.assertIn("New Path", choices)

    def test_form_includes_ritual_options_for_hedge_mage(self):
        """Test form includes ritual options for hedge mages."""
        form = SorcererFreebiesForm(instance=self.sorcerer)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertIn("Create Ritual", choices)
        self.assertIn("Select Ritual", choices)

    def test_form_excludes_ritual_options_for_psychic(self):
        """Test form excludes ritual options for psychics."""
        self.sorcerer.sorcerer_type = "psychic"
        self.sorcerer.save()
        form = SorcererFreebiesForm(instance=self.sorcerer)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertNotIn("Create Ritual", choices)
        self.assertNotIn("Select Ritual", choices)

    def test_validator_true_when_enough_freebies(self):
        """Test validator returns True when enough freebies."""
        form = SorcererFreebiesForm(instance=self.sorcerer)
        self.assertTrue(form.validator("Attribute"))

    def test_validator_false_when_not_enough_freebies(self):
        """Test validator returns False when not enough freebies."""
        self.sorcerer.freebies = 0
        self.sorcerer.save()
        form = SorcererFreebiesForm(instance=self.sorcerer)
        # Most traits should be excluded
        self.assertFalse(form.validator("Attribute"))

    def test_form_save_returns_instance(self):
        """Test form save returns the instance."""
        form = SorcererFreebiesForm(instance=self.sorcerer)
        result = form.save()
        self.assertEqual(result, self.sorcerer)


class TestCompanionFreebiesForm(TestCase):
    """Test CompanionFreebiesForm."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.player,
            companion_type="familiar",
            freebies=25,
            willpower=5,
        )

    def test_form_initialization(self):
        """Test form initializes correctly."""
        form = CompanionFreebiesForm(instance=self.companion)
        self.assertIn("category", form.fields)

    def test_form_includes_advantage_option(self):
        """Test form includes Advantage option."""
        form = CompanionFreebiesForm(instance=self.companion)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertIn("Advantage", choices)

    def test_form_includes_charms_for_familiar(self):
        """Test form includes Charms option for familiars."""
        form = CompanionFreebiesForm(instance=self.companion)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertIn("Charms", choices)

    def test_form_excludes_charms_for_non_familiar(self):
        """Test form excludes Charms option for non-familiars."""
        self.companion.companion_type = "consor"
        self.companion.save()
        form = CompanionFreebiesForm(instance=self.companion)
        choices = [c[0] for c in form.fields["category"].choices]
        self.assertNotIn("Charms", choices)

    def test_form_save_returns_instance(self):
        """Test form save returns the instance."""
        form = CompanionFreebiesForm(instance=self.companion)
        result = form.save()
        self.assertEqual(result, self.companion)

    def test_form_with_custom_suggestions(self):
        """Test form initializes with custom suggestions."""
        suggestions = ["Test Suggestion"]
        form = CompanionFreebiesForm(instance=self.companion, suggestions=suggestions)
        # Form should initialize without errors
        self.assertIsNotNone(form)
