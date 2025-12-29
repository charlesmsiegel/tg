"""
Tests for HumanFreebiesForm.

Tests cover:
- Form initialization with different character states
- Category choices based on available freebies
- Validator method for checking freebie costs
- Form validation for required fields
- Clean method validation for different categories
- Example queryset population based on category
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.core.freebies import CATEGORY_CHOICES, HumanFreebiesForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from game.models import ObjectType


class HumanFreebiesFormTestCase(TestCase):
    """Base test case with common setup for HumanFreebiesForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create human object type
        cls.human_type = ObjectType.objects.create(name="human", type="char", gameline="wod")

        # Create attributes
        cls.strength = Attribute.objects.create(name="Strength", property_name="strength")
        cls.dexterity = Attribute.objects.create(name="Dexterity", property_name="dexterity")
        cls.stamina = Attribute.objects.create(name="Stamina", property_name="stamina")

        # Create abilities
        cls.alertness = Ability.objects.create(name="Alertness", property_name="alertness")
        cls.athletics = Ability.objects.create(name="Athletics", property_name="athletics")
        cls.brawl = Ability.objects.create(name="Brawl", property_name="brawl")

        # Create backgrounds
        cls.contacts = Background.objects.create(name="Contacts", property_name="contacts")
        cls.resources = Background.objects.create(name="Resources", property_name="resources")
        cls.allies = Background.objects.create(name="Allies", property_name="allies")

        # Create merits and flaws
        cls.merit = MeritFlaw.objects.create(name="Acute Senses")
        cls.merit.add_rating(1)
        cls.merit.add_rating(2)
        cls.merit.add_rating(3)
        cls.merit.allowed_types.add(cls.human_type)

        cls.flaw = MeritFlaw.objects.create(name="Bad Sight")
        cls.flaw.add_rating(-1)
        cls.flaw.add_rating(-2)
        cls.flaw.allowed_types.add(cls.human_type)

    def setUp(self):
        """Set up test user and character."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.character = Human.objects.create(
            name="Test Human",
            owner=self.user,
            freebies=15,  # Standard starting freebies
        )


class TestHumanFreebiesFormInitialization(HumanFreebiesFormTestCase):
    """Test form initialization with different character states."""

    def test_form_initializes_with_character_instance(self):
        """Form initializes correctly with character instance."""
        form = HumanFreebiesForm(instance=self.character)

        self.assertIn("category", form.fields)
        self.assertIn("example", form.fields)
        self.assertIn("value", form.fields)
        self.assertIn("note", form.fields)
        self.assertIn("pooled", form.fields)

    def test_form_category_choices_with_full_freebies(self):
        """Form shows all categories with 15+ freebies."""
        self.character.freebies = 15
        self.character.save()

        form = HumanFreebiesForm(instance=self.character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Attribute", category_values)
        self.assertIn("Ability", category_values)
        self.assertIn("New Background", category_values)
        self.assertIn("Existing Background", category_values)
        self.assertIn("Willpower", category_values)
        self.assertIn("MeritFlaw", category_values)

    def test_form_excludes_attributes_with_low_freebies(self):
        """Attribute category excluded when freebies < 5."""
        self.character.freebies = 4
        self.character.save()

        form = HumanFreebiesForm(instance=self.character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Attribute", category_values)
        # Other categories should still be available
        self.assertIn("Ability", category_values)

    def test_form_excludes_abilities_with_very_low_freebies(self):
        """Ability category excluded when freebies < 2."""
        self.character.freebies = 1
        self.character.save()

        form = HumanFreebiesForm(instance=self.character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Ability", category_values)
        # Willpower at cost 1 should still be available
        self.assertIn("Willpower", category_values)


class TestHumanFreebiesFormValidator(HumanFreebiesFormTestCase):
    """Test the validator method for category choices."""

    def test_validator_returns_true_for_affordable_trait(self):
        """Validator returns True when character can afford trait."""
        self.character.freebies = 10
        self.character.save()

        form = HumanFreebiesForm(instance=self.character)

        # Ability costs 2, should be affordable with 10 freebies
        self.assertTrue(form.validator("Ability"))

    def test_validator_returns_false_for_unaffordable_trait(self):
        """Validator returns False when character cannot afford trait."""
        self.character.freebies = 3
        self.character.save()

        form = HumanFreebiesForm(instance=self.character)

        # Attribute costs 5, should not be affordable with 3 freebies
        self.assertFalse(form.validator("Attribute"))

    def test_validator_returns_true_for_unknown_trait(self):
        """Validator returns True for unknown traits (freebie_cost returns non-int)."""
        form = HumanFreebiesForm(instance=self.character)

        # Unknown traits should return True (handled elsewhere)
        self.assertTrue(form.validator("unknown_trait_type"))

    def test_validator_returns_true_for_very_high_cost(self):
        """Validator returns True for 10000 cost (indicates special handling)."""
        form = HumanFreebiesForm(instance=self.character)

        # Traits with 10000 cost are handled specially
        self.assertTrue(form.validator("-----"))


class TestHumanFreebiesFormBoundData(HumanFreebiesFormTestCase):
    """Test form behavior when bound with data."""

    def test_bound_form_sets_attribute_queryset(self):
        """Bound form with Attribute category sets attribute queryset."""
        form = HumanFreebiesForm(
            data={"category": "Attribute", "example": "", "value": ""},
            instance=self.character,
        )

        # Check that example queryset contains attributes
        example_qs = form.fields["example"].queryset
        self.assertTrue(example_qs.filter(name="Strength").exists())

    def test_bound_form_sets_ability_queryset(self):
        """Bound form with Ability category sets ability queryset."""
        form = HumanFreebiesForm(
            data={"category": "Ability", "example": "", "value": ""},
            instance=self.character,
        )

        example_qs = form.fields["example"].queryset
        self.assertTrue(example_qs.filter(name="Alertness").exists())

    def test_bound_form_sets_new_background_queryset(self):
        """Bound form with New Background sets all backgrounds queryset."""
        form = HumanFreebiesForm(
            data={"category": "New Background", "example": "", "value": ""},
            instance=self.character,
        )

        example_qs = form.fields["example"].queryset
        self.assertTrue(example_qs.filter(name="Contacts").exists())

    def test_bound_form_sets_existing_background_queryset(self):
        """Bound form with Existing Background sets character's backgrounds."""
        # Add a background to the character
        bg_rating = BackgroundRating.objects.create(
            char=self.character,
            bg=self.contacts,
            rating=2,
        )

        form = HumanFreebiesForm(
            data={"category": "Existing Background", "example": "", "value": ""},
            instance=self.character,
        )

        example_qs = form.fields["example"].queryset
        # Should only include character's existing backgrounds
        # The queryset is the character's backgrounds, which returns BackgroundRating objects
        self.assertTrue(example_qs.filter(bg=self.contacts).exists())

    def test_bound_form_sets_meritflaw_queryset_and_value_choices(self):
        """Bound form with MeritFlaw sets merit/flaw queryset and value choices."""
        form = HumanFreebiesForm(
            data={"category": "MeritFlaw", "example": "", "value": ""},
            instance=self.character,
        )

        example_qs = form.fields["example"].queryset
        self.assertTrue(example_qs.filter(name="Acute Senses").exists())

        # Value choices should be range -100 to 100
        value_choices = form.fields["value"].choices
        self.assertTrue(len(value_choices) > 0)


class TestHumanFreebiesFormCleanValidation(HumanFreebiesFormTestCase):
    """Test clean method validation."""

    def test_clean_rejects_default_category(self):
        """Clean raises error when default category selected."""
        form = HumanFreebiesForm(
            data={"category": "-----", "example": "", "value": ""},
            instance=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Must Choose Freebie Expenditure Type", str(form.errors))

    def test_clean_rejects_meritflaw_without_example(self):
        """Clean raises error when MeritFlaw selected without example."""
        form = HumanFreebiesForm(
            data={"category": "MeritFlaw", "example": "", "value": "1"},
            instance=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Must Choose Merit/Flaw and rating", str(form.errors))

    def test_clean_rejects_meritflaw_without_value(self):
        """Clean raises error when MeritFlaw selected without value."""
        form = HumanFreebiesForm(
            data={
                "category": "MeritFlaw",
                "example": str(self.merit.pk),
                "value": "",
            },
            instance=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Must Choose Merit/Flaw and rating", str(form.errors))

    def test_clean_rejects_attribute_without_example(self):
        """Clean raises error when Attribute selected without example."""
        form = HumanFreebiesForm(
            data={"category": "Attribute", "example": "", "value": ""},
            instance=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Must Choose Trait", str(form.errors))

    def test_clean_rejects_ability_without_example(self):
        """Clean raises error when Ability selected without example."""
        form = HumanFreebiesForm(
            data={"category": "Ability", "example": "", "value": ""},
            instance=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Must Choose Trait", str(form.errors))

    def test_clean_rejects_new_background_without_example(self):
        """Clean raises error when New Background selected without example."""
        form = HumanFreebiesForm(
            data={"category": "New Background", "example": "", "value": ""},
            instance=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Must Choose Trait", str(form.errors))

    def test_clean_rejects_existing_background_without_example(self):
        """Clean raises error when Existing Background selected without example."""
        # Add a background to the character
        BackgroundRating.objects.create(
            char=self.character,
            bg=self.contacts,
            rating=2,
        )

        form = HumanFreebiesForm(
            data={"category": "Existing Background", "example": "", "value": ""},
            instance=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Must Choose Trait", str(form.errors))


class TestHumanFreebiesFormValidSubmission(HumanFreebiesFormTestCase):
    """Test valid form submissions."""

    def test_valid_attribute_submission(self):
        """Valid attribute submission passes validation."""
        form = HumanFreebiesForm(
            data={
                "category": "Attribute",
                "example": str(self.strength.pk),
                "value": "",
                "note": "",
            },
            instance=self.character,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_ability_submission(self):
        """Valid ability submission passes validation."""
        form = HumanFreebiesForm(
            data={
                "category": "Ability",
                "example": str(self.alertness.pk),
                "value": "",
                "note": "",
            },
            instance=self.character,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_new_background_submission(self):
        """Valid new background submission passes validation."""
        form = HumanFreebiesForm(
            data={
                "category": "New Background",
                "example": str(self.contacts.pk),
                "value": "",
                "note": "Work contacts",
            },
            instance=self.character,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_willpower_submission(self):
        """Valid willpower submission passes validation."""
        form = HumanFreebiesForm(
            data={
                "category": "Willpower",
                "example": "",
                "value": "",
                "note": "",
            },
            instance=self.character,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_meritflaw_submission(self):
        """Valid merit/flaw submission passes validation."""
        form = HumanFreebiesForm(
            data={
                "category": "MeritFlaw",
                "example": str(self.merit.pk),
                "value": "1",
                "note": "",
            },
            instance=self.character,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")


class TestHumanFreebiesFormFieldAttributes(HumanFreebiesFormTestCase):
    """Test form field attributes and defaults."""

    def test_note_field_max_length(self):
        """Note field has max length of 300."""
        form = HumanFreebiesForm(instance=self.character)
        self.assertEqual(form.fields["note"].max_length, 300)

    def test_pooled_field_is_boolean(self):
        """Pooled field is a boolean field."""
        form = HumanFreebiesForm(instance=self.character)
        self.assertFalse(form.fields["pooled"].required)

    def test_value_field_not_required(self):
        """Value field is not required."""
        form = HumanFreebiesForm(instance=self.character)
        self.assertFalse(form.fields["value"].required)

    def test_example_field_not_required(self):
        """Example field is not required."""
        form = HumanFreebiesForm(instance=self.character)
        self.assertFalse(form.fields["example"].required)


class TestCategoryChoicesConstant(TestCase):
    """Test the CATEGORY_CHOICES constant."""

    def test_category_choices_contains_expected_options(self):
        """CATEGORY_CHOICES contains all expected options."""
        category_values = [choice[0] for choice in CATEGORY_CHOICES]

        self.assertIn("-----", category_values)
        self.assertIn("Attribute", category_values)
        self.assertIn("Ability", category_values)
        self.assertIn("New Background", category_values)
        self.assertIn("Existing Background", category_values)
        self.assertIn("Willpower", category_values)
        self.assertIn("MeritFlaw", category_values)

    def test_category_choices_has_correct_format(self):
        """CATEGORY_CHOICES has correct tuple format."""
        for choice in CATEGORY_CHOICES:
            self.assertEqual(len(choice), 2)
            self.assertEqual(choice[0], choice[1])  # Value equals display name
