"""Tests for the background trait-name parser shared by the spending appliers."""

from django.test import SimpleTestCase

from characters.services.trait_names import split_background_trait_name


class SplitBackgroundTraitNameTests(SimpleTestCase):
    def test_name_without_note(self):
        self.assertEqual(split_background_trait_name("Resources"), ("Resources", ""))

    def test_name_with_note(self):
        self.assertEqual(
            split_background_trait_name("Resources (Family wealth)"),
            ("Resources", "Family wealth"),
        )

    def test_note_containing_parentheses(self):
        self.assertEqual(
            split_background_trait_name("Contacts (Police (Vice))"),
            ("Contacts", "Police (Vice)"),
        )

    def test_surrounding_whitespace_is_dropped(self):
        self.assertEqual(
            split_background_trait_name("  Allies ( Street gang )  "),
            ("Allies", "Street gang"),
        )
