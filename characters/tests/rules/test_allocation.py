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
                "groups": [
                    ["physical", ["strength", "dexterity", "stamina"]],
                    ["social", ["charisma", "manipulation", "appearance"]],
                    ["mental", ["perception", "intelligence", "wits"]],
                ],
                "group_labels": {"physical": "Physical", "social": "Social", "mental": "Mental"},
                "targets": [10, 8, 6],
                "priority_fields": {
                    "physical": "priority_physical",
                    "social": "priority_social",
                    "mental": "priority_mental",
                },
            },
        )

    def test_status_reports_group_totals_against_targets(self):
        status = self.rule.status({**ATTRIBUTES, "strength": 4})
        self.assertEqual(
            [(g["name"], g["current"]) for g in status["groups"]],
            [("physical", 11), ("social", 8), ("mental", 6)],
        )
        self.assertEqual(status["targets"], [10, 8, 6])
        self.assertFalse(status["satisfied"])
        self.assertTrue(self.rule.status(ATTRIBUTES)["satisfied"])


def ranked(physical, social, mental):
    return {
        "priority_physical": physical,
        "priority_social": social,
        "priority_mental": mental,
    }


class PriorityRanksTest(TestCase):
    """The PRI / SEC / TER choice: chosen ranks set each group's target."""

    rule = attribute_rule(7, 5, 3)

    def test_chosen_ranks_matching_the_dots_are_valid(self):
        values = {**ATTRIBUTES, **ranked("primary", "secondary", "tertiary")}
        self.assertIsNone(first_violation([self.rule], values))
        self.assertEqual(
            self.rule.chosen_ranks(values),
            {"physical": "primary", "social": "secondary", "mental": "tertiary"},
        )

    def test_swapped_ranks_reject_a_distribution_valid_in_another_order(self):
        values = {**ATTRIBUTES, **ranked("secondary", "primary", "tertiary")}
        self.assertEqual(
            first_violation([self.rule], values).message,
            "Attributes must be distributed 7/5/3 as ranked "
            "(Physical secondary, Social primary, Mental tertiary)",
        )
        swapped = {
            **ATTRIBUTES,
            "strength": 2,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 4,
            **ranked("secondary", "primary", "tertiary"),
        }
        self.assertEqual(
            self.rule.group_totals(swapped), {"physical": 8, "social": 10, "mental": 6}
        )
        self.assertIsNone(first_violation([self.rule], swapped))

    def test_missing_ranks_are_inferred_from_the_dots(self):
        self.assertIsNone(self.rule.chosen_ranks(ATTRIBUTES))
        self.assertEqual(
            self.rule.ranks(ATTRIBUTES),
            ({"physical": "primary", "social": "secondary", "mental": "tertiary"}, False),
        )
        # Blank choices (an unticked radio group) count as missing.
        blank = {**ATTRIBUTES, **ranked("", "", "")}
        self.assertIsNone(first_violation([self.rule], blank))
        # Ties keep the groups' order.
        self.assertEqual(
            self.rule.inferred_ranks({}),
            {"physical": "primary", "social": "secondary", "mental": "tertiary"},
        )

    def test_partial_or_repeated_ranks_are_an_error(self):
        message = "Choose primary, secondary and tertiary once each for Physical, Social and Mental"
        for choice in (ranked("primary", "primary", "tertiary"), {"priority_physical": "primary"}):
            with self.subTest(choice=choice):
                values = {**ATTRIBUTES, **choice}
                self.assertEqual(first_violation([self.rule], values).message, message)
        # The range check still comes first.
        values = {**ATTRIBUTES, "strength": 0, **ranked("primary", "primary", "primary")}
        self.assertEqual(
            first_violation([self.rule], values).message, "Attributes must range from 1-5"
        )

    def test_columns_count_against_the_chosen_targets(self):
        values = {**ATTRIBUTES, "strength": 2, **ranked("tertiary", "secondary", "primary")}
        columns = self.rule.columns(values)
        self.assertEqual(
            [(c["name"], c["rank"], c["target"], c["current"], c["count"]) for c in columns],
            [
                ("physical", "tertiary", 6, 9, "3 over"),
                ("social", "secondary", 8, 8, "done"),
                ("mental", "primary", 10, 6, "4 left"),
            ],
        )
        self.assertEqual([c["state"] for c in columns], ["over", "done", "progress"])

    def test_columns_without_a_choice_use_the_inferred_ranking(self):
        values = {**ATTRIBUTES, "wits": 1}
        self.assertEqual(
            [(c["rank"], c["count"]) for c in self.rule.columns(values)],
            [("primary", "done"), ("secondary", "done"), ("tertiary", "1 left")],
        )

    def test_status_reports_each_group_against_its_chosen_target(self):
        status = self.rule.status({**ATTRIBUTES, **ranked("tertiary", "secondary", "primary")})
        self.assertTrue(status["ranked"])
        self.assertFalse(status["satisfied"])
        self.assertEqual(
            [(g["name"], g["current"], g["target"], g["count"]) for g in status["groups"]],
            [("physical", 10, 6, "4 over"), ("social", 8, 8, "done"), ("mental", 6, 10, "4 left")],
        )
        unranked = self.rule.status(ATTRIBUTES)
        self.assertFalse(unranked["ranked"])
        self.assertNotIn("target", unranked["groups"][0])

    def test_group_sizes_set_the_ability_targets(self):
        rule = ability_rule(AbilityRuleTest.model, AbilityRuleTest.fields, 6, 4, 2)
        self.assertEqual(rule.target("talents", "primary"), 6)
        self.assertEqual(
            rule.priority_fields, ("priority_talents", "priority_skills", "priority_knowledges")
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
            {
                "name": "arcanoi",
                "label": "Arcanoi",
                "total": 5,
                "comparison": "exact",
                "max": 5,
                "fields": list(WRAITH_ARCANOI.fields),
            },
        )

    def test_status_is_satisfied_exactly_as_the_totals_phase(self):
        exact = AllocationRule(name="x_y", fields=("a", "b"), total=3, message="")
        at_most = AllocationRule(
            name="z", fields=("a", "b"), total=3, message="", comparison="at_most"
        )
        self.assertEqual(
            exact.status({"a": 1, "b": 1}),
            {
                "name": "x_y",
                "label": "X Y",
                "current": 2,
                "target": 3,
                "comparison": "exact",
                "satisfied": False,
            },
        )
        self.assertTrue(at_most.status({"a": 1, "b": 1})["satisfied"])
        self.assertFalse(at_most.status({"a": 3, "b": 1})["satisfied"])
        for rule in (exact, at_most):
            for values in ({"a": 1, "b": 2}, {"a": 3, "b": 3}, {"a": 0, "b": 0}):
                self.assertEqual(
                    rule.status(values)["satisfied"], not rule.violations(values, TOTALS)
                )
