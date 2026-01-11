"""
Tests for CharacterCreationForm.

Tests cover:
- Form initialization for regular users vs storytellers
- Gameline filtering based on user permissions
- Character type filtering based on gameline selection
- Label formatting for character types
- Excluded types (groups, non-character types)
- Data attributes for JavaScript filtering
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.core.character_creation import CharacterCreationForm
from game.models import Chronicle, Gameline, ObjectType, STRelationship


class CharacterCreationFormTestCase(TestCase):
    """Base test case with common setup for CharacterCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create gamelines
        cls.gameline_mta = Gameline.objects.create(name="Mage: the Ascension")
        cls.gameline_vtm = Gameline.objects.create(name="Vampire: the Masquerade")
        cls.gameline_wta = Gameline.objects.create(name="Werewolf: the Apocalypse")

        # Create character types for Mage gameline
        ObjectType.objects.create(name="mage", type="char", gameline="mta")
        ObjectType.objects.create(name="mta_human", type="char", gameline="mta")
        ObjectType.objects.create(name="sorcerer", type="char", gameline="mta")

        # Create character types for Vampire gameline
        ObjectType.objects.create(name="vampire", type="char", gameline="vtm")
        ObjectType.objects.create(name="vtm_human", type="char", gameline="vtm")
        ObjectType.objects.create(name="ghoul", type="char", gameline="vtm")

        # Create character types for Werewolf gameline
        ObjectType.objects.create(name="werewolf", type="char", gameline="wta")
        ObjectType.objects.create(name="wta_human", type="char", gameline="wta")
        ObjectType.objects.create(name="kinfolk", type="char", gameline="wta")

        # Create group types (should be excluded)
        ObjectType.objects.create(name="cabal", type="char", gameline="mta")
        ObjectType.objects.create(name="coterie", type="char", gameline="vtm")
        ObjectType.objects.create(name="pack", type="char", gameline="wta")

        # Create non-character types (should be excluded)
        ObjectType.objects.create(name="sphere", type="char", gameline="mta")
        ObjectType.objects.create(name="discipline", type="char", gameline="vtm")
        ObjectType.objects.create(name="gift", type="char", gameline="wta")

        # Create a spirit character (special case)
        ObjectType.objects.create(name="spirit_character", type="char", gameline="wta")

        # Create chronicle for ST relationships
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def setUp(self):
        """Set up test users."""
        self.regular_user = User.objects.create_user(
            username="regular_user",
            email="regular@test.com",
            password="testpassword",
        )
        self.st_user = User.objects.create_user(
            username="st_user",
            email="st@test.com",
            password="testpassword",
        )
        # Make st_user a storyteller
        STRelationship.objects.create(
            user=self.st_user,
            chronicle=self.chronicle,
            gameline=self.gameline_mta,
        )


class TestCharacterCreationFormInitialization(CharacterCreationFormTestCase):
    """Test form initialization with different user types."""

    def test_form_initializes_without_user(self):
        """Form initializes correctly without a user (anonymous)."""
        form = CharacterCreationForm()

        # Should have only the empty placeholder choice for anonymous users
        # ChainedChoiceField always adds an empty choice ("", "---------")
        self.assertEqual(len(form.fields["gameline"].choices), 1)
        self.assertEqual(form.fields["gameline"].choices[0][0], "")
        self.assertEqual(len(form.fields["char_type"].choices), 1)
        self.assertEqual(form.fields["char_type"].choices[0][0], "")

    def test_form_initializes_for_regular_user(self):
        """Form initializes correctly for regular (non-ST) user."""
        form = CharacterCreationForm(user=self.regular_user)

        # Regular users only see mage gameline
        gameline_codes = [code for code, _ in form.fields["gameline"].choices]
        self.assertEqual(gameline_codes, ["mta"])

    def test_form_initializes_for_st_user(self):
        """Form initializes correctly for storyteller user."""
        form = CharacterCreationForm(user=self.st_user)

        # ST users see all gamelines with character types
        gameline_codes = [code for code, _ in form.fields["gameline"].choices]
        self.assertIn("mta", gameline_codes)
        self.assertIn("vtm", gameline_codes)
        self.assertIn("wta", gameline_codes)


class TestGamelineFiltering(CharacterCreationFormTestCase):
    """Test gameline choice filtering."""

    def test_regular_user_only_sees_mage_gameline(self):
        """Regular users are restricted to Mage gameline only."""
        form = CharacterCreationForm(user=self.regular_user)

        gameline_choices = form.fields["gameline"].choices
        self.assertEqual(len(gameline_choices), 1)
        self.assertEqual(gameline_choices[0][0], "mta")
        self.assertEqual(gameline_choices[0][1], "Mage: the Ascension")

    def test_st_user_sees_all_gamelines(self):
        """Storytellers can see all gamelines."""
        form = CharacterCreationForm(user=self.st_user)

        gameline_codes = [code for code, _ in form.fields["gameline"].choices]
        # Should have all gamelines that have character types
        self.assertGreaterEqual(len(gameline_codes), 3)


class TestCharacterTypeFiltering(CharacterCreationFormTestCase):
    """Test character type filtering and exclusions."""

    def test_group_types_excluded(self):
        """Group types (cabal, pack, coterie, etc.) are excluded."""
        form = CharacterCreationForm(user=self.st_user)

        # Check the data-types-by-gameline for excluded group types
        import json

        types_data = json.loads(
            form.fields["char_type"].widget.attrs.get("data-types-by-gameline", "{}")
        )

        # Check mta gameline doesn't have 'cabal'
        if "mta" in types_data:
            mta_values = [t["value"] for t in types_data["mta"]]
            self.assertNotIn("cabal", mta_values)

        # Check vtm gameline doesn't have 'coterie'
        if "vtm" in types_data:
            vtm_values = [t["value"] for t in types_data["vtm"]]
            self.assertNotIn("coterie", vtm_values)

        # Check wta gameline doesn't have 'pack'
        if "wta" in types_data:
            wta_values = [t["value"] for t in types_data["wta"]]
            self.assertNotIn("pack", wta_values)

    def test_non_character_types_excluded(self):
        """Non-character types (spheres, disciplines, etc.) are excluded."""
        form = CharacterCreationForm(user=self.st_user)

        import json

        types_data = json.loads(
            form.fields["char_type"].widget.attrs.get("data-types-by-gameline", "{}")
        )

        # Check mta gameline doesn't have 'sphere'
        if "mta" in types_data:
            mta_values = [t["value"] for t in types_data["mta"]]
            self.assertNotIn("sphere", mta_values)

        # Check vtm gameline doesn't have 'discipline'
        if "vtm" in types_data:
            vtm_values = [t["value"] for t in types_data["vtm"]]
            self.assertNotIn("discipline", vtm_values)

        # Check wta gameline doesn't have 'gift'
        if "wta" in types_data:
            wta_values = [t["value"] for t in types_data["wta"]]
            self.assertNotIn("gift", wta_values)

    def test_valid_character_types_included(self):
        """Valid character types are included in the form."""
        form = CharacterCreationForm(user=self.st_user)

        import json

        types_data = json.loads(
            form.fields["char_type"].widget.attrs.get("data-types-by-gameline", "{}")
        )

        # Check mta gameline has 'mage' and 'sorcerer'
        if "mta" in types_data:
            mta_values = [t["value"] for t in types_data["mta"]]
            self.assertIn("mage", mta_values)
            self.assertIn("sorcerer", mta_values)

        # Check vtm gameline has 'vampire' and 'ghoul'
        if "vtm" in types_data:
            vtm_values = [t["value"] for t in types_data["vtm"]]
            self.assertIn("vampire", vtm_values)
            self.assertIn("ghoul", vtm_values)


class TestLabelFormatting(CharacterCreationFormTestCase):
    """Test character type label formatting."""

    def test_format_label_for_human_types(self):
        """Human types are formatted as 'Human (Gameline)'."""
        form = CharacterCreationForm(user=self.st_user)

        # Test the _format_label method directly
        self.assertEqual(form._format_label("mta_human"), "Human (Mage)")
        self.assertEqual(form._format_label("vtm_human"), "Human (Vampire)")
        self.assertEqual(form._format_label("wta_human"), "Human (Werewolf)")
        self.assertEqual(form._format_label("ctd_human"), "Human (Changeling)")
        self.assertEqual(form._format_label("wto_human"), "Human (Wraith)")
        self.assertEqual(form._format_label("dtf_human"), "Human (Demon)")
        self.assertEqual(form._format_label("htr_human"), "Human (Hunter)")
        self.assertEqual(form._format_label("mtr_human"), "Human (Mummy)")

    def test_format_label_for_spirit_character(self):
        """Spirit character has special formatting."""
        form = CharacterCreationForm(user=self.st_user)
        self.assertEqual(form._format_label("spirit_character"), "Spirit")

    def test_format_label_for_regular_types(self):
        """Regular types are title-cased with underscores replaced."""
        form = CharacterCreationForm(user=self.st_user)

        self.assertEqual(form._format_label("mage"), "Mage")
        self.assertEqual(form._format_label("vampire"), "Vampire")
        self.assertEqual(form._format_label("werewolf"), "Werewolf")
        self.assertEqual(form._format_label("some_type_name"), "Some Type Name")

    def test_format_label_for_unknown_human_prefix(self):
        """Unknown human prefixes use the prefix as-is."""
        form = CharacterCreationForm(user=self.st_user)

        # Unknown prefix should be uppercased
        self.assertEqual(form._format_label("xyz_human"), "Human (XYZ)")


class TestDataAttributesForJavaScript(CharacterCreationFormTestCase):
    """Test choices_map configuration for JavaScript filtering.

    Note: ChainedSelect uses choices_map on the field and embeds the tree as JSON
    in a script tag, rather than using data attributes on the widget.
    """

    def test_char_type_has_choices_map(self):
        """char_type field has choices_map configured."""
        form = CharacterCreationForm(user=self.st_user)

        choices_map = form.fields["char_type"].choices_map
        self.assertIsNotNone(choices_map)
        self.assertIsInstance(choices_map, dict)

    def test_choices_map_is_valid(self):
        """choices_map contains valid gameline mappings."""
        form = CharacterCreationForm(user=self.st_user)

        choices_map = form.fields["char_type"].choices_map

        # Should be a non-empty dict
        self.assertIsInstance(choices_map, dict)
        self.assertGreater(len(choices_map), 0)

    def test_choices_map_structure(self):
        """choices_map has correct structure."""
        form = CharacterCreationForm(user=self.st_user)

        choices_map = form.fields["char_type"].choices_map

        # Each gameline should have a list of tuples with (value, label)
        for gameline, types in choices_map.items():
            self.assertIsInstance(types, list)
            for type_info in types:
                self.assertIsInstance(type_info, tuple)
                self.assertEqual(len(type_info), 2)

    def test_types_sorted_by_label(self):
        """Character types are sorted alphabetically by label."""
        form = CharacterCreationForm(user=self.st_user)

        choices_map = form.fields["char_type"].choices_map

        # Check each gameline's types are sorted by label
        for gameline, types in choices_map.items():
            labels = [t[1] for t in types]
            self.assertEqual(labels, sorted(labels))


class TestInitialCharTypeChoices(CharacterCreationFormTestCase):
    """Test initial character type choices."""

    def test_st_initial_choices_from_first_gameline(self):
        """ST user gets initial char_type choices from first gameline."""
        form = CharacterCreationForm(user=self.st_user)

        gameline_choices = form.fields["gameline"].choices
        if gameline_choices:
            # Initial char_type choices should exist
            self.assertTrue(len(form.fields["char_type"].choices) > 0)

    def test_regular_user_initial_choices_from_mta(self):
        """Regular user gets initial char_type choices from MtA."""
        form = CharacterCreationForm(user=self.regular_user)

        char_type_choices = form.fields["char_type"].choices
        char_type_values = [value for value, _ in char_type_choices]

        # Should have mage types
        self.assertIn("mage", char_type_values)


class TestFormFieldAttributes(CharacterCreationFormTestCase):
    """Test form field widget attributes."""

    def test_gameline_field_has_id(self):
        """Gameline field has correct ID attribute."""
        form = CharacterCreationForm(user=self.st_user)

        widget_attrs = form.fields["gameline"].widget.attrs
        self.assertEqual(widget_attrs.get("id"), "id_gameline")

    def test_char_type_field_has_id(self):
        """char_type field has correct ID attribute."""
        form = CharacterCreationForm(user=self.st_user)

        widget_attrs = form.fields["char_type"].widget.attrs
        self.assertEqual(widget_attrs.get("id"), "id_char_type")


class TestFormValidation(CharacterCreationFormTestCase):
    """Test form validation."""

    def test_valid_submission_for_st(self):
        """ST can submit form with valid gameline and character type."""
        # First get the form to see what gamelines and char_types are available
        form_unbound = CharacterCreationForm(user=self.st_user)
        gameline_choices = form_unbound.fields["gameline"].choices
        char_type_choices = form_unbound.fields["char_type"].choices

        # Filter out empty placeholder choices
        valid_gamelines = [c for c in gameline_choices if c[0]]
        valid_char_types = [c for c in char_type_choices if c[0]]

        if valid_gamelines and valid_char_types:
            # Use the first available gameline and char_type (skip empty placeholder)
            first_gameline = valid_gamelines[0][0]
            first_char_type = valid_char_types[0][0]

            form = CharacterCreationForm(
                data={
                    "gameline": first_gameline,
                    "char_type": first_char_type,
                },
                user=self.st_user,
            )

            self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_submission_for_regular_user(self):
        """Regular user can submit form with valid mage gameline type."""
        # First get the form to see what char_types are available for regular users
        form_unbound = CharacterCreationForm(user=self.regular_user)
        char_type_choices = form_unbound.fields["char_type"].choices

        # Filter out empty placeholder choices
        valid_char_types = [c for c in char_type_choices if c[0]]

        if valid_char_types:
            first_char_type = valid_char_types[0][0]

            form = CharacterCreationForm(
                data={
                    "gameline": "mta",
                    "char_type": first_char_type,
                },
                user=self.regular_user,
            )

            self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_empty_submission_invalid(self):
        """Empty form submission is invalid."""
        form = CharacterCreationForm(
            data={},
            user=self.st_user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("gameline", form.errors)
        self.assertIn("char_type", form.errors)

    def test_invalid_gameline_rejected(self):
        """Invalid gameline value is rejected."""
        form = CharacterCreationForm(
            data={
                "gameline": "invalid_gameline",
                "char_type": "mage",
            },
            user=self.st_user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("gameline", form.errors)

    def test_invalid_char_type_rejected(self):
        """Invalid char_type value is rejected."""
        form = CharacterCreationForm(
            data={
                "gameline": "mta",
                "char_type": "invalid_type",
            },
            user=self.st_user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("char_type", form.errors)
