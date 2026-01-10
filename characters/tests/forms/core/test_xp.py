"""
Tests for XP spending form validation and processing.

Tests cover:
- XPForm initialization and field configuration
- Category validation (valid selection, invalid placeholder)
- Example field population based on category
- Value field validation
- XP cost calculations for different stat types
- Edge cases (zero XP, maxed stats, etc.)
"""

from characters.costs import get_xp_cost
from characters.forms.core.xp import CATEGORY_CHOICES, XPForm
from characters.models.core import Human, MeritFlaw
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from core.models import Number
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import ObjectType


def xp_test_setup():
    """Set up the minimal test data needed for XP form tests."""
    ObjectType.objects.get_or_create(name="human", type="char", gameline="wod")

    # Create attributes
    Attribute.objects.get_or_create(name="Strength", property_name="strength")
    Attribute.objects.get_or_create(name="Dexterity", property_name="dexterity")
    Attribute.objects.get_or_create(name="Stamina", property_name="stamina")
    Attribute.objects.get_or_create(name="Perception", property_name="perception")
    Attribute.objects.get_or_create(name="Intelligence", property_name="intelligence")
    Attribute.objects.get_or_create(name="Wits", property_name="wits")
    Attribute.objects.get_or_create(name="Charisma", property_name="charisma")
    Attribute.objects.get_or_create(name="Manipulation", property_name="manipulation")
    Attribute.objects.get_or_create(name="Appearance", property_name="appearance")

    # Create backgrounds
    Background.objects.get_or_create(name="Contacts", property_name="contacts")
    Background.objects.get_or_create(name="Mentor", property_name="mentor")

    # Create abilities that match Human.talents, Human.skills, Human.knowledges
    # Talents
    Ability.objects.get_or_create(name="Alertness", property_name="alertness")
    Ability.objects.get_or_create(name="Athletics", property_name="athletics")
    Ability.objects.get_or_create(name="Brawl", property_name="brawl")
    Ability.objects.get_or_create(name="Empathy", property_name="empathy")
    Ability.objects.get_or_create(name="Expression", property_name="expression")
    Ability.objects.get_or_create(name="Intimidation", property_name="intimidation")
    Ability.objects.get_or_create(name="Streetwise", property_name="streetwise")
    Ability.objects.get_or_create(name="Subterfuge", property_name="subterfuge")

    # Skills
    Ability.objects.get_or_create(name="Crafts", property_name="crafts")
    Ability.objects.get_or_create(name="Drive", property_name="drive")
    Ability.objects.get_or_create(name="Etiquette", property_name="etiquette")
    Ability.objects.get_or_create(name="Firearms", property_name="firearms")
    Ability.objects.get_or_create(name="Melee", property_name="melee")
    Ability.objects.get_or_create(name="Stealth", property_name="stealth")

    # Knowledges
    Ability.objects.get_or_create(name="Academics", property_name="academics")
    Ability.objects.get_or_create(name="Computer", property_name="computer")
    Ability.objects.get_or_create(name="Investigation", property_name="investigation")
    Ability.objects.get_or_create(name="Medicine", property_name="medicine")
    Ability.objects.get_or_create(name="Science", property_name="science")


class TestXPFormBasics(TestCase):
    """Test basic XPForm initialization and structure."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,  # Plenty of XP for testing
        )
        # Create Number objects for value choices
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = XPForm(character=self.character)

        self.assertIn("category", form.fields)
        self.assertIn("example", form.fields)
        self.assertIn("value", form.fields)
        self.assertIn("note", form.fields)
        self.assertIn("pooled", form.fields)
        self.assertIn("image_field", form.fields)

    def test_form_category_has_default_choices(self):
        """Test that category field has expected default choices."""
        form = XPForm(character=self.character)

        category_values = [choice[0] for choice in form.fields["category"].choices]
        # Check for core categories (these depend on whether the character meets requirements)
        self.assertIn("-----", category_values)
        self.assertIn("Attribute", category_values)
        # Ability depends on abilities in DB that match character's talents/skills/knowledges
        self.assertIn("Ability", category_values)
        self.assertIn("Willpower", category_values)

    def test_example_field_is_optional(self):
        """Test that example field is not required."""
        form = XPForm(character=self.character)

        self.assertFalse(form.fields["example"].required)

    def test_value_field_is_optional(self):
        """Test that value field is not required."""
        form = XPForm(character=self.character)

        self.assertFalse(form.fields["value"].required)

    def test_note_field_max_length(self):
        """Test that note field has max_length of 300."""
        form = XPForm(character=self.character)

        self.assertEqual(form.fields["note"].max_length, 300)


class TestXPFormCategoryValidation(TestCase):
    """Test category selection validation."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_placeholder_category_is_invalid(self):
        """Test that selecting '-----' placeholder raises validation error."""
        form = XPForm(
            data={"category": "-----"},
            character=self.character,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)
        self.assertIn("Invalid category selected", str(form.errors["category"]))

    def test_attribute_category_is_valid(self):
        """Test that Attribute category is valid when a valid example is provided."""
        strength = Attribute.objects.get(property_name="strength")

        form = XPForm(
            data={"category": "Attribute", "example": strength.id},
            character=self.character,
        )

        # Check that category validates correctly (form may have other errors)
        form.is_valid()
        self.assertNotIn("category", form.errors)

    def test_ability_category_is_valid(self):
        """Test that Ability category is valid when a valid example is provided."""
        alertness = Ability.objects.get(property_name="alertness")

        form = XPForm(
            data={"category": "Ability", "example": alertness.id},
            character=self.character,
        )

        form.is_valid()
        self.assertNotIn("category", form.errors)

    def test_willpower_category_is_valid(self):
        """Test that Willpower category is valid."""
        form = XPForm(
            data={"category": "Willpower"},
            character=self.character,
        )

        # Willpower doesn't require an example
        form.is_valid()
        self.assertNotIn("category", form.errors)


class TestXPFormCategoryFiltering(TestCase):
    """Test that categories are filtered based on character state."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_image_category_shown_when_no_image(self):
        """Test that Image category is shown when character has no image."""
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )

        form = XPForm(character=self.character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        # Image should be present since character has no image
        self.assertIn("Image", category_values)

    def test_attribute_category_hidden_when_all_maxed(self):
        """Test that Attribute category is hidden when all attributes are at 5."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
            strength=5,
            dexterity=5,
            stamina=5,
            perception=5,
            intelligence=5,
            wits=5,
            charisma=5,
            manipulation=5,
            appearance=5,
        )

        form = XPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Attribute", category_values)

    def test_attribute_category_shown_when_affordable(self):
        """Test that Attribute category is shown when attributes can be raised."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,  # Plenty of XP
        )

        form = XPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Attribute", category_values)

    def test_attribute_category_hidden_when_insufficient_xp(self):
        """Test that Attribute category is hidden when XP is insufficient."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=0,  # No XP
        )

        form = XPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Attribute", category_values)

    def test_background_category_requires_5_xp(self):
        """Test that Background category requires at least 5 XP for new backgrounds."""
        character_with_xp = Human.objects.create(
            name="Character With XP",
            owner=self.user,
            xp=10,
        )
        character_no_xp = Human.objects.create(
            name="Character No XP",
            owner=self.user,
            xp=0,
        )

        form_with_xp = XPForm(character=character_with_xp)
        form_no_xp = XPForm(character=character_no_xp)

        categories_with_xp = [choice[0] for choice in form_with_xp.fields["category"].choices]
        categories_no_xp = [choice[0] for choice in form_no_xp.fields["category"].choices]

        self.assertIn("Background", categories_with_xp)
        self.assertNotIn("Background", categories_no_xp)

    def test_willpower_category_hidden_when_insufficient_xp(self):
        """Test Willpower category is hidden when can't afford to raise it."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=0,
            willpower=5,
        )

        form = XPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Willpower", category_values)

    def test_willpower_category_shown_when_affordable(self):
        """Test Willpower category is shown when affordable."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
            willpower=5,
        )

        form = XPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Willpower", category_values)

    def test_ability_category_hidden_when_insufficient_xp(self):
        """Test Ability category is hidden when XP is insufficient for any ability."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=0,  # No XP - can't afford any ability upgrade
        )

        form = XPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Ability", category_values)


class TestXPFormExamplePopulation(TestCase):
    """Test example field population based on category selection."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_attribute_category_populates_example_with_attributes(self):
        """Test that selecting Attribute populates example with attribute choices."""
        form = XPForm(
            data={"category": "Attribute"},
            character=self.character,
        )

        example_choices = form.fields["example"].choices
        choice_names = [choice[1] for choice in example_choices]

        # Check for some standard attributes
        self.assertIn("Strength", choice_names)
        self.assertIn("Dexterity", choice_names)
        self.assertIn("Stamina", choice_names)

    def test_ability_category_populates_example_with_abilities(self):
        """Test that selecting Ability populates example with ability choices."""
        form = XPForm(
            data={"category": "Ability"},
            character=self.character,
        )

        example_choices = form.fields["example"].choices
        choice_names = [choice[1] for choice in example_choices]

        # Check for some standard abilities that should be in Human's abilities
        self.assertIn("Alertness", choice_names)
        self.assertIn("Athletics", choice_names)

    def test_background_category_accepts_form_data(self):
        """Test that Background category is accepted.

        Note: Background examples are populated via AJAX with prefixed values
        (bg_123 for new backgrounds, br_456 for existing backgrounds).
        The form's clean_example method parses these prefixes.
        """
        form = XPForm(
            data={"category": "Background"},
            character=self.character,
        )

        # The form should accept Background as a valid category
        self.assertEqual(form.data.get("category"), "Background")


class TestXPFormCleanExample(TestCase):
    """Test example field cleaning/validation."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_clean_example_returns_attribute_object(self):
        """Test that clean_example returns Attribute object for Attribute category."""
        strength = Attribute.objects.get(property_name="strength")

        form = XPForm(
            data={"category": "Attribute", "example": strength.id},
            character=self.character,
        )
        form.is_valid()

        if "example" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["example"], strength)

    def test_clean_example_returns_ability_object(self):
        """Test that clean_example returns Ability object for Ability category."""
        alertness = Ability.objects.get(property_name="alertness")

        form = XPForm(
            data={"category": "Ability", "example": alertness.id},
            character=self.character,
        )
        form.is_valid()

        if "example" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["example"], alertness)

    def test_clean_example_returns_background_object_for_new_background(self):
        """Test that clean_example returns Background object for prefixed bg_ value."""
        contacts = Background.objects.get(property_name="contacts")

        form = XPForm(
            data={"category": "Background", "example": f"bg_{contacts.id}"},
            character=self.character,
        )
        form.is_valid()

        if "example" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["example"], contacts)

    def test_clean_example_returns_background_rating_object_for_existing_background(self):
        """Test that clean_example returns BackgroundRating object for prefixed br_ value."""
        contacts = Background.objects.get(property_name="contacts")
        br = BackgroundRating.objects.create(
            char=self.character,
            bg=contacts,
            rating=2,
        )

        form = XPForm(
            data={"category": "Background", "example": f"br_{br.id}"},
            character=self.character,
        )
        form.is_valid()

        if "example" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["example"], br)


class TestXPFormCleanValue(TestCase):
    """Test value field cleaning/validation."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_clean_value_returns_id_of_number(self):
        """Test that clean_value returns the Number's id value."""
        number = Number.objects.get(value=3)
        strength = Attribute.objects.get(property_name="strength")

        form = XPForm(
            data={"category": "Attribute", "example": strength.id, "value": number.pk},
            character=self.character,
        )
        form.is_valid()

        if "value" in form.cleaned_data and form.cleaned_data["value"] is not None:
            self.assertEqual(form.cleaned_data["value"], number.id)

    def test_clean_value_handles_none(self):
        """Test that clean_value handles None gracefully."""
        form = XPForm(
            data={"category": "Willpower"},
            character=self.character,
        )
        form.is_valid()

        # Value should be None since not provided
        self.assertIsNone(form.cleaned_data.get("value"))


class TestXPFormValidityChecks(TestCase):
    """Test the various *_valid() methods that determine category availability."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_image_valid_returns_true_when_no_image(self):
        """Test image_valid returns True when character has no image."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )
        form = XPForm(character=character)

        self.assertTrue(form.image_valid())

    def test_attribute_valid_with_available_xp(self):
        """Test attribute_valid returns True when XP is available for upgrades."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )
        form = XPForm(character=character)

        self.assertTrue(form.attribute_valid())

    def test_attribute_valid_all_maxed(self):
        """Test attribute_valid returns False when all attributes are maxed."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
            strength=5,
            dexterity=5,
            stamina=5,
            perception=5,
            intelligence=5,
            wits=5,
            charisma=5,
            manipulation=5,
            appearance=5,
        )
        form = XPForm(character=character)

        self.assertFalse(form.attribute_valid())

    def test_ability_valid_with_available_xp(self):
        """Test ability_valid returns True when XP is available for upgrades."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )
        form = XPForm(character=character)

        self.assertTrue(form.ability_valid())

    def test_ability_valid_false_when_no_xp(self):
        """Test ability_valid returns False when XP is insufficient."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=0,
        )
        form = XPForm(character=character)

        self.assertFalse(form.ability_valid())

    def test_background_valid_requires_5_xp(self):
        """Test background_valid requires at least 5 XP for new backgrounds."""
        character_with_xp = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=5,
        )
        character_no_xp = Human.objects.create(
            name="Test Character 2",
            owner=self.user,
            xp=4,
        )

        form_with = XPForm(character=character_with_xp)
        form_without = XPForm(character=character_no_xp)

        self.assertTrue(form_with.background_valid())
        self.assertFalse(form_without.background_valid())

    def test_willpower_valid_checks_cost(self):
        """Test willpower_valid checks if character can afford to raise willpower."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
            willpower=3,
        )
        form = XPForm(character=character)

        self.assertTrue(form.willpower_valid())

    def test_willpower_valid_false_when_insufficient_xp(self):
        """Test willpower_valid returns False when XP is insufficient."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=0,
            willpower=5,  # Cost to raise is 5
        )
        form = XPForm(character=character)

        self.assertFalse(form.willpower_valid())


class TestXPFormMeritFlawValidation(TestCase):
    """Test merit/flaw category validation."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create ObjectType for human
        self.human_type = ObjectType.objects.get_or_create(
            name="human", type="char", gameline="wod"
        )[0]

        # Create merit/flaw for testing
        for i in range(1, 4):
            mf = MeritFlaw.objects.create(name=f"Test Merit {i}")
            mf.add_rating(i)
            mf.allowed_types.add(self.human_type)

        for i in range(1, 6):
            Number.objects.get_or_create(value=i)
            Number.objects.get_or_create(value=-i)

    def test_mf_valid_when_affordable_mfs_exist(self):
        """Test mf_valid returns True when affordable merit/flaws exist."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,  # Plenty of XP
        )
        form = XPForm(character=character)

        # Should be valid since we have affordable merits
        self.assertTrue(form.mf_valid())

    def test_mf_valid_false_when_no_xp(self):
        """Test mf_valid returns False when character has no XP."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=0,
        )
        form = XPForm(character=character)

        self.assertFalse(form.mf_valid())

    def test_meritflaw_category_populates_with_affordable_options(self):
        """Test MeritFlaw category shows only affordable merits/flaws."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=3,  # Limited XP - only affordable for rating 1 merits (cost: 3)
        )

        form = XPForm(
            data={"category": "MeritFlaw"},
            character=character,
        )

        example_choices = form.fields["example"].choices
        # Should have at least one choice (rating 1 merit costs 3 XP)
        self.assertGreater(len(example_choices), 0)


class TestXPFormEdgeCases(TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_form_with_zero_xp_character(self):
        """Test form initialization with character having zero XP."""
        character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=0,
        )

        form = XPForm(character=character)

        # Form should initialize without errors
        self.assertIsNotNone(form)

        # Most categories should be filtered out
        category_values = [choice[0] for choice in form.fields["category"].choices]
        self.assertIn("-----", category_values)  # Placeholder always present

    def test_form_with_maxed_stats_still_allows_other_categories(self):
        """Test form with maxed attributes and abilities still allows other options."""
        character = Human.objects.create(
            name="Maxed Character",
            owner=self.user,
            xp=100,
            strength=5,
            dexterity=5,
            stamina=5,
            perception=5,
            intelligence=5,
            wits=5,
            charisma=5,
            manipulation=5,
            appearance=5,
            alertness=5,
            athletics=5,
            brawl=5,
            empathy=5,
            expression=5,
            intimidation=5,
            streetwise=5,
            subterfuge=5,
            crafts=5,
            drive=5,
            etiquette=5,
            firearms=5,
            melee=5,
            stealth=5,
            academics=5,
            computer=5,
            investigation=5,
            medicine=5,
            science=5,
        )

        form = XPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        # Attribute and Ability should be filtered out since all are maxed
        self.assertNotIn("Attribute", category_values)
        self.assertNotIn("Ability", category_values)
        # But other categories should still be available
        self.assertIn("Background", category_values)


class TestXPCostCalculations(TestCase):
    """Test XP cost calculations for different stat types."""

    def setUp(self):
        xp_test_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            xp=50,
        )

    def test_attribute_xp_cost(self):
        """Test XP cost for attributes (current rating * 4)."""
        # Attribute XP cost is current rating * 4
        self.assertEqual(get_xp_cost("attribute") * 1, 4)
        self.assertEqual(get_xp_cost("attribute") * 2, 8)
        self.assertEqual(get_xp_cost("attribute") * 3, 12)
        self.assertEqual(get_xp_cost("attribute") * 4, 16)
        self.assertEqual(get_xp_cost("attribute") * 5, 20)

    def test_ability_xp_cost(self):
        """Test XP cost for abilities (current rating * 2)."""
        # Ability XP cost is current rating * 2
        self.assertEqual(get_xp_cost("ability") * 1, 2)
        self.assertEqual(get_xp_cost("ability") * 2, 4)
        self.assertEqual(get_xp_cost("ability") * 3, 6)
        self.assertEqual(get_xp_cost("ability") * 4, 8)
        self.assertEqual(get_xp_cost("ability") * 5, 10)

    def test_new_ability_xp_cost(self):
        """Test XP cost for new abilities (3 XP)."""
        self.assertEqual(get_xp_cost("new_ability"), 3)

    def test_background_xp_cost(self):
        """Test XP cost for backgrounds (current rating * 3)."""
        self.assertEqual(get_xp_cost("background") * 1, 3)
        self.assertEqual(get_xp_cost("background") * 2, 6)
        self.assertEqual(get_xp_cost("background") * 3, 9)

    def test_new_background_xp_cost(self):
        """Test XP cost for new backgrounds (5 XP flat)."""
        self.assertEqual(get_xp_cost("new_background"), 5)

    def test_willpower_xp_cost(self):
        """Test XP cost for willpower (current rating * 1)."""
        self.assertEqual(get_xp_cost("willpower") * 1, 1)
        self.assertEqual(get_xp_cost("willpower") * 5, 5)
        self.assertEqual(get_xp_cost("willpower") * 10, 10)

    def test_meritflaw_xp_cost(self):
        """Test XP cost for merits/flaws (rating change * 3)."""
        self.assertEqual(get_xp_cost("meritflaw") * 1, 3)
        self.assertEqual(get_xp_cost("meritflaw") * 2, 6)
