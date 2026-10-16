"""Legacy trait spending must not hide lookup or trait-update failures."""

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.test import SimpleTestCase

from characters.models.core.human import Ability, Attribute, Human


class HumanSpendingErrorsTests(SimpleTestCase):
    def test_lookup_errors_propagate_without_spending(self):
        for method in ("spend_xp", "spend_freebies"):
            for catalogue in (Attribute, Ability):
                for error_type in (DatabaseError, RuntimeError):
                    with self.subTest(method=method, catalogue=catalogue, error=error_type):
                        character = Human(xp=100, freebies=100)
                        initial_willpower = character.willpower
                        error = error_type("catalogue lookup failed")
                        with (
                            patch.object(Attribute.objects, "filter") as attributes,
                            patch.object(Ability.objects, "filter") as abilities,
                            patch.object(character, "save"),
                            patch.object(character, "add_to_spend"),
                        ):
                            attributes.return_value.first.return_value = None
                            abilities.return_value.first.return_value = None
                            lookup = attributes if catalogue is Attribute else abilities
                            lookup.return_value.first.side_effect = error
                            with self.assertRaises(error_type) as caught:
                                getattr(character, method)("willpower")
                            self.assertIs(caught.exception, error)
                            self.assertEqual(character.xp, 100)
                            self.assertEqual(character.freebies, 100)
                            self.assertEqual(character.willpower, initial_willpower)
                            if catalogue is Attribute:
                                abilities.assert_not_called()

    def test_trait_update_errors_propagate_without_trying_other_categories(self):
        for method in ("spend_xp", "spend_freebies"):
            for catalogue, trait, adder in (
                (Attribute, "strength", "add_attribute"),
                (Ability, "alertness", "add_ability"),
            ):
                with self.subTest(method=method, catalogue=catalogue):
                    character = Human(xp=100, freebies=100)
                    initial_value = getattr(character, trait)
                    error = ValidationError("trait update rejected")
                    with (
                        patch.object(Attribute.objects, "filter") as attributes,
                        patch.object(Ability.objects, "filter") as abilities,
                        patch.object(character, adder, side_effect=error),
                    ):
                        attributes.return_value.first.return_value = (
                            object() if catalogue is Attribute else None
                        )
                        abilities.return_value.first.return_value = object()
                        with self.assertRaises(ValidationError) as caught:
                            getattr(character, method)(trait)
                        self.assertIs(caught.exception, error)
                        self.assertEqual(character.xp, 100)
                        self.assertEqual(character.freebies, 100)
                        self.assertEqual(getattr(character, trait), initial_value)
                        if catalogue is Attribute:
                            abilities.assert_not_called()

    def test_unknown_trait_still_returns_name(self):
        character = Human(xp=100, freebies=100)
        with (
            patch.object(Attribute.objects, "filter") as attributes,
            patch.object(Ability.objects, "filter") as abilities,
        ):
            attributes.return_value.first.return_value = None
            abilities.return_value.first.return_value = None
            self.assertEqual(character.spend_xp("custom_trait"), "custom_trait")
            self.assertEqual(character.spend_freebies("custom_trait"), "custom_trait")
        self.assertEqual(character.xp, 100)
        self.assertEqual(character.freebies, 100)

    def test_successful_trait_spending_still_updates_rating_and_pool(self):
        for method, pool in (("spend_xp", "xp"), ("spend_freebies", "freebies")):
            for catalogue, trait in ((Attribute, "strength"), (Ability, "alertness")):
                with self.subTest(method=method, catalogue=catalogue):
                    character = Human(xp=100, freebies=100)
                    initial_value = getattr(character, trait)
                    with (
                        patch.object(Attribute.objects, "filter") as attributes,
                        patch.object(Ability.objects, "filter") as abilities,
                        patch.object(character, "save"),
                        patch.object(character, "add_to_spend"),
                    ):
                        attributes.return_value.first.return_value = (
                            object() if catalogue is Attribute else None
                        )
                        abilities.return_value.first.return_value = object()
                        self.assertIs(getattr(character, method)(trait), True)
                    self.assertEqual(getattr(character, trait), initial_value + 1)
                    self.assertLess(getattr(character, pool), 100)
                    other_pool = "freebies" if pool == "xp" else "xp"
                    self.assertEqual(getattr(character, other_pool), 100)
