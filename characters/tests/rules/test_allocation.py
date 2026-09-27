"""Pure allocation rules: no database, no views."""

from dataclasses import replace
from types import SimpleNamespace
from unittest import TestCase

from characters.rules.allocation import (
    BOUNDS,
    CHOICES,
    TOTALS,
    AllocationRule,
    first_violation,
)
from characters.rules.limits import (
    CHANGELING_ARTS,
    CHANGELING_REALMS,
    GHOUL_DISCIPLINES,
    VAMPIRE_DISCIPLINES,
    WRAITH_ARCANOI,
    ability_rule,
    attribute_rule,
)

ATTRIBUTES = {
    "strength": 3,
    "dexterity": 3,
    "stamina": 4,
    "charisma": 2,
    "manipulation": 3,
    "appearance": 3,
    "perception": 2,
    "intelligence": 2,
    "wits": 2,
}


class AttributeRuleTest(TestCase):
    rule = attribute_rule(7, 5, 3)

    def test_valid_distribution(self):
        self.assertIsNone(first_violation([self.rule], ATTRIBUTES))

    def test_range_is_checked_before_distribution(self):
        values = {**ATTRIBUTES, "strength": 0}
        self.assertEqual(
            first_violation([self.rule], values).message, "Attributes must range from 1-5"
        )

    def test_wrong_distribution_message(self):
        values = {**ATTRIBUTES, "strength": 4}
        self.assertEqual(
            first_violation([self.rule], values).message,
            "Attributes must be distributed 7/5/3",
        )

    def test_client_data(self):
        self.assertEqual(
            self.rule.client_data(),
            {
                "name": "attributes",
                "primary": 7,
                "secondary": 5,
                "tertiary": 3,
                "min": 1,
                "max": 5,
                "base": 1,
            },
        )


class AbilityRuleTest(TestCase):
    model = SimpleNamespace(
        talents=["alertness", "athletics", "secret_talent"],
        skills=["crafts", "drive"],
        knowledges=["academics", "occult"],
        primary_abilities=["alertness", "athletics", "crafts", "drive", "academics", "occult"],
    )
    fields = tuple(model.primary_abilities)

    def rule(self, **kwargs):
        return ability_rule(self.model, self.fields, 6, 4, 2, **kwargs)

    def test_groups_only_count_form_fields(self):
        rule = self.rule()
        self.assertEqual(rule.groups[0], ("talents", ("alertness", "athletics")))

    def test_valid(self):
        values = {
            "alertness": 3,
            "athletics": 3,
            "crafts": 2,
            "drive": 2,
            "academics": 1,
            "occult": 1,
        }
        self.assertIsNone(first_violation([self.rule()], values))

    def test_range_flash(self):
        values = {
            "alertness": 4,
            "athletics": 2,
            "crafts": 2,
            "drive": 2,
            "academics": 1,
            "occult": 1,
        }
        violation = first_violation([self.rule(range_flash="too high")], values)
        self.assertEqual(violation.message, "Abilities must range from 0-3")
        self.assertEqual(violation.flash, "too high")

    def test_allocation_flash_uses_group_totals(self):
        values = {
            "alertness": 3,
            "athletics": 3,
            "crafts": 2,
            "drive": 2,
            "academics": 1,
            "occult": 0,
        }
        violation = first_violation(
            [self.rule(flash="{allocation}: {talents}/{skills}/{knowledges}")], values
        )
        self.assertEqual(violation.message, "Abilities must be distributed 6/4/2")
        self.assertEqual(violation.flash, "Abilities must be distributed 6/4/2: 6/4/1")


class AllocationRuleTest(TestCase):
    def test_totals_before_bounds_across_rules(self):
        values = {"autumn": 6, "actor": 1}
        violation = first_violation([CHANGELING_ARTS, CHANGELING_REALMS], values)
        self.assertEqual(violation.message, "Arts must total 3 dots (currently 6)")
        self.assertEqual(
            violation.flash, "Arts allocation error: You must spend exactly 3 dots. You have 6."
        )
        values = {"autumn": 3, "actor": 1}
        self.assertEqual(
            first_violation([CHANGELING_ARTS, CHANGELING_REALMS], values).message,
            "Realms must total 5 dots (currently 1)",
        )

    def test_bounds_are_field_errors(self):
        rule = replace(CHANGELING_ARTS, total=6)
        (violation,) = rule.violations({"dragons_ire": 6}, BOUNDS)
        self.assertEqual(violation.field, "dragons_ire")
        self.assertEqual(violation.message, "Cannot exceed 5 dots")
        self.assertEqual(violation.flash, "Dragons Ire cannot exceed 5 dots.")

    def test_wraith_messages(self):
        violation = first_violation([WRAITH_ARCANOI], {"argos": 4})
        self.assertEqual(violation.message, "Arcanoi must total exactly 5 dots (currently 4)")

    def test_allowed_only_checked_when_configured(self):
        values = {"celerity": 3}
        self.assertEqual(VAMPIRE_DISCIPLINES.violations(values, CHOICES), [])
        rule = replace(VAMPIRE_DISCIPLINES, allowed=frozenset({"potence"}))
        (violation,) = rule.violations(values, CHOICES)
        self.assertEqual(violation.field, "celerity")

    def test_at_most(self):
        self.assertEqual(GHOUL_DISCIPLINES.violations({"celerity": 2}, TOTALS), [])
        (violation,) = GHOUL_DISCIPLINES.violations({"celerity": 3}, TOTALS)
        self.assertEqual(
            violation.message, "You can spend up to 2 dots on additional Disciplines. Currently: 3"
        )

    def test_none_counts_as_zero(self):
        rule = AllocationRule(name="x", fields=("a", "b"), total=1, message="{current}")
        self.assertEqual(rule.violations({"a": None, "b": 1}, TOTALS), [])

    def test_client_data(self):
        self.assertEqual(
            WRAITH_ARCANOI.client_data(),
            {"name": "arcanoi", "total": 5, "comparison": "exact", "max": 5},
        )
