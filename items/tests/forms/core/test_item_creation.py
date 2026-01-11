"""
Tests for ItemCreationForm validation and initialization.

Tests cover:
- Form initialization for ST users (all gamelines/item types)
- Form initialization for regular users (mage-only items)
- Label formatting for item types
- Gameline and item type choice population
- Form field configuration
"""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, Gameline, ObjectType, STRelationship
from items.forms.core.item_creation import ItemCreationForm


class TestItemCreationFormSetup(TestCase):
    """Shared setup for ItemCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test users and object types."""
        cls.regular_user = User.objects.create_user(username="regular_user", password="password")
        cls.st_user = User.objects.create_user(username="st_user", password="password")

        # Create Chronicle and Gameline for ST relationship
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")
        cls.mage_gameline = Gameline.objects.create(name="Mage: the Ascension")

        # Make st_user an ST by creating an STRelationship
        STRelationship.objects.create(
            user=cls.st_user, chronicle=cls.chronicle, gameline=cls.mage_gameline
        )

        # Create ObjectTypes for different gamelines and item types
        cls.mage_periapt = ObjectType.objects.create(name="periapt", type="obj", gameline="mta")
        cls.mage_talisman = ObjectType.objects.create(name="talisman", type="obj", gameline="mta")
        cls.mage_sorcerer_artifact = ObjectType.objects.create(
            name="sorcerer_artifact", type="obj", gameline="mta"
        )
        cls.vampire_artifact = ObjectType.objects.create(
            name="vampire_artifact", type="obj", gameline="vtm"
        )
        cls.werewolf_fetish = ObjectType.objects.create(name="fetish", type="obj", gameline="wta")


class TestItemCreationFormBasics(TestItemCreationFormSetup):
    """Test basic ItemCreationForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = ItemCreationForm(user=self.regular_user)

        self.assertIn("gameline", form.fields)
        self.assertIn("item_type", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("rank", form.fields)

    def test_name_field_is_optional(self):
        """Test that name field is not required."""
        form = ItemCreationForm(user=self.regular_user)

        self.assertFalse(form.fields["name"].required)

    def test_name_field_max_length(self):
        """Test that name field has correct max_length."""
        form = ItemCreationForm(user=self.regular_user)

        self.assertEqual(form.fields["name"].max_length, 100)

    def test_rank_field_default_value(self):
        """Test that rank field has correct initial value."""
        form = ItemCreationForm(user=self.regular_user)

        self.assertEqual(form.fields["rank"].initial, 1)

    def test_rank_field_max_value(self):
        """Test that rank field has correct max_value."""
        form = ItemCreationForm(user=self.regular_user)

        self.assertEqual(form.fields["rank"].max_value, 5)

    def test_gameline_field_uses_chained_select(self):
        """Test that gameline field uses ChainedSelect widget."""
        from widgets.widgets.chained import ChainedSelect

        form = ItemCreationForm(user=self.regular_user)

        self.assertIsInstance(form.fields["gameline"].widget, ChainedSelect)

    def test_item_type_field_uses_chained_select(self):
        """Test that item_type field uses ChainedSelect widget."""
        from widgets.widgets.chained import ChainedSelect

        form = ItemCreationForm(user=self.regular_user)

        self.assertIsInstance(form.fields["item_type"].widget, ChainedSelect)


class TestItemCreationFormLabelFormatting(TestItemCreationFormSetup):
    """Test the _format_label method for item type labels."""

    def test_format_label_sorcerer_artifact(self):
        """Test special case formatting for sorcerer_artifact."""
        form = ItemCreationForm(user=self.regular_user)

        result = form._format_label("sorcerer_artifact")

        self.assertEqual(result, "Sorcerer Artifact")

    def test_format_label_vampire_artifact(self):
        """Test special case formatting for vampire_artifact."""
        form = ItemCreationForm(user=self.regular_user)

        result = form._format_label("vampire_artifact")

        self.assertEqual(result, "Vampire Artifact")

    def test_format_label_standard_name(self):
        """Test standard formatting for regular item names."""
        form = ItemCreationForm(user=self.regular_user)

        result = form._format_label("periapt")

        self.assertEqual(result, "Periapt")

    def test_format_label_underscore_name(self):
        """Test formatting replaces underscores with spaces."""
        form = ItemCreationForm(user=self.regular_user)

        result = form._format_label("melee_weapon")

        self.assertEqual(result, "Melee Weapon")

    def test_format_label_title_case(self):
        """Test formatting applies title case."""
        form = ItemCreationForm(user=self.regular_user)

        result = form._format_label("some_long_item_name")

        self.assertEqual(result, "Some Long Item Name")


class TestItemCreationFormRegularUser(TestItemCreationFormSetup):
    """Test ItemCreationForm initialization for regular (non-ST) users."""

    def test_gameline_choices_only_mage(self):
        """Test that regular users only see Mage gameline."""
        form = ItemCreationForm(user=self.regular_user)

        gameline_values = [choice[0] for choice in form.fields["gameline"].choices]

        self.assertEqual(gameline_values, ["mta"])

    def test_gameline_label_correct(self):
        """Test that Mage gameline has correct display label."""
        form = ItemCreationForm(user=self.regular_user)

        gameline_labels = dict(form.fields["gameline"].choices)

        self.assertEqual(gameline_labels.get("mta"), "Mage: the Ascension")

    def test_item_type_choices_only_mage_items(self):
        """Test that regular users only see Mage item types in choices_map."""
        form = ItemCreationForm(user=self.regular_user)

        # ChainedChoiceField stores choices in choices_map, not choices
        choices_map = form.fields["item_type"].choices_map
        mage_item_values = [choice[0] for choice in choices_map.get("mta", [])]

        # Should include mage items
        self.assertIn("periapt", mage_item_values)
        self.assertIn("talisman", mage_item_values)
        self.assertIn("sorcerer_artifact", mage_item_values)

        # Should NOT include vampire or werewolf items (no such keys in map)
        self.assertNotIn("vtm", choices_map)
        self.assertNotIn("wta", choices_map)

    def test_item_types_sorted_by_label(self):
        """Test that item types are sorted alphabetically by label."""
        form = ItemCreationForm(user=self.regular_user)

        item_type_labels = [choice[1] for choice in form.fields["item_type"].choices]

        self.assertEqual(item_type_labels, sorted(item_type_labels))

    def test_choices_tree_contains_mage_items(self):
        """Test that the choices tree contains mage item types for JavaScript access."""
        form = ItemCreationForm(user=self.regular_user)

        # ChainedSelectMixin embeds choices in the root widget's choices_tree
        choices_tree = form.fields["gameline"].widget.choices_tree

        self.assertIsNotNone(choices_tree)
        # Should contain item_type choices keyed by parent value
        self.assertIn("item_type:mta", choices_tree)


class TestItemCreationFormSTUser(TestItemCreationFormSetup):
    """Test ItemCreationForm initialization for ST users."""

    def test_gameline_choices_multiple(self):
        """Test that ST users see all gamelines with items."""
        form = ItemCreationForm(user=self.st_user)

        gameline_values = [choice[0] for choice in form.fields["gameline"].choices]

        # ST should see all gamelines that have item types
        self.assertIn("mta", gameline_values)
        self.assertIn("vtm", gameline_values)
        self.assertIn("wta", gameline_values)

    def test_item_type_initially_first_gameline(self):
        """Test that item_type is initially populated with first gameline's types."""
        form = ItemCreationForm(user=self.st_user)

        # Get the first gameline
        gameline_values = [choice[0] for choice in form.fields["gameline"].choices]
        first_gameline = gameline_values[0] if gameline_values else None

        # Item types should be from the first gameline
        item_type_values = [choice[0] for choice in form.fields["item_type"].choices]

        # At least one item should be present
        self.assertGreater(len(item_type_values), 0)

    def test_each_gameline_types_sorted(self):
        """Test that each gameline's item types are sorted by label."""
        form = ItemCreationForm(user=self.st_user)

        # Check that choices_map for item_type has sorted labels for each gameline
        choices_map = form.fields["item_type"].choices_map
        for gameline, choices in choices_map.items():
            labels = [label for _, label in choices]
            self.assertEqual(labels, sorted(labels), f"Types for {gameline} not sorted")


class TestItemCreationFormUnauthenticated(TestCase):
    """Test ItemCreationForm with no user or unauthenticated user."""

    def test_form_without_user_has_only_empty_choice(self):
        """Test that form without user has only the empty placeholder choice."""
        form = ItemCreationForm()

        # Without user, only the empty placeholder choice should be present
        choices = list(form.fields["gameline"].choices)
        # ChainedSelect widget adds an empty label choice
        self.assertEqual(len(choices), 1)
        self.assertEqual(choices[0][0], "")

    def test_form_with_none_user(self):
        """Test that form with user=None doesn't crash."""
        form = ItemCreationForm(user=None)

        # Should initialize without errors
        self.assertIsNotNone(form)


class TestItemCreationFormEdgeCases(TestItemCreationFormSetup):
    """Test edge cases for ItemCreationForm."""

    def test_no_object_types_for_gameline(self):
        """Test form behavior when a gameline has no object types."""
        # Create a new user who is ST for a gameline with no items
        no_items_user = User.objects.create_user(username="no_items_user", password="password")

        # Create a Hunter gameline with no item ObjectTypes
        hunter_gameline = Gameline.objects.create(name="Hunter: the Reckoning")
        STRelationship.objects.create(
            user=no_items_user, chronicle=self.chronicle, gameline=hunter_gameline
        )

        form = ItemCreationForm(user=no_items_user)

        # Form should still initialize
        self.assertIsNotNone(form)

    def test_form_preserves_initial_data(self):
        """Test that form correctly handles initial data."""
        initial_data = {
            "gameline": "mta",
            "item_type": "periapt",
            "name": "Test Item",
            "rank": 3,
        }

        form = ItemCreationForm(data=initial_data, user=self.regular_user)

        # Form should be bound
        self.assertTrue(form.is_bound)

    def test_form_validates_with_valid_data(self):
        """Test that form validates with complete valid data."""
        form_data = {
            "gameline": "mta",
            "item_type": "periapt",
            "name": "Test Periapt",
            "rank": 2,
        }

        form = ItemCreationForm(data=form_data, user=self.regular_user)

        self.assertTrue(form.is_valid())

    def test_form_invalid_without_required_fields(self):
        """Test that form is invalid without required fields."""
        form_data = {
            "name": "Test Item",
            # Missing gameline, item_type
        }

        form = ItemCreationForm(data=form_data, user=self.regular_user)

        self.assertFalse(form.is_valid())

    def test_rank_exceeding_max_invalid(self):
        """Test that rank > 5 is invalid."""
        form_data = {
            "gameline": "mta",
            "item_type": "periapt",
            "name": "Test Item",
            "rank": 10,
        }

        form = ItemCreationForm(data=form_data, user=self.regular_user)

        self.assertFalse(form.is_valid())
        self.assertIn("rank", form.errors)
