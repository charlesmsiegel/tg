"""The PRI / SEC / TER picker and clickable dots on the Attributes and Abilities steps.

Mage is a plain (non-interactive) workflow; Vampire is the interactive pilot.
Every request goes through the wizard URL, as a browser's would.
"""

import re

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.mage.mage import Mage
from characters.models.vampire.vampire import Vampire
from characters.views.mage.mage import MageAbilityView

HX = {"HX-Request": "true"}
# Physical 10, Social 8, Mental 6: primary / secondary / tertiary.
ATTRIBUTES = {
    "strength": 4,
    "dexterity": 3,
    "stamina": 3,
    "charisma": 3,
    "manipulation": 3,
    "appearance": 2,
    "perception": 2,
    "intelligence": 2,
    "wits": 2,
}


def ranks(physical, social, mental):
    return {
        "priority_physical": physical,
        "priority_social": social,
        "priority_mental": mental,
    }


def section(html, group):
    """The markup of one ranked column."""
    match = re.search(rf'<section[^>]*data-priority-group="{group}".*?</section>', html, re.S)
    return match.group(0) if match else ""


class PriorityTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("owner", password="pw")

    def setUp(self):
        self.client.login(username="owner", password="pw")

    def url(self, character):
        return reverse("characters:character", kwargs={"pk": character.pk})

    def mage(self, step=1):
        return Mage.objects.create(name="Ranked", owner=self.owner, creation_status=step)


class AttributePickerRenderTests(PriorityTestCase):
    def test_picker_counts_and_dots_render_without_javascript(self):
        html = self.client.get(self.url(self.mage())).content.decode()
        physical = section(html, "physical")
        self.assertNotIn("data-priority-picker", physical)
        self.assertIn('data-priority-targets="10,8,6"', physical)
        for group, rank in (("physical", "Primary"), ("social", "Secondary"), ("mental", "Tertiary")):
            self.assertIn(f'<small data-inferred-priority>{rank}</small>', section(html, group))
        # Each column counts down from its rank's target (every Attribute starts at 1).
        for group, left in (("physical", 7), ("social", 5), ("mental", 3)):
            self.assertRegex(
                html,
                rf'<span class="tl-alloc__left" id="{group}-status" data-priority-count>'
                rf"{left} left</span>",
            )
        self.assertIn('data-priority="attributes"', html)
        self.assertIn("characters/js/chargen-priority.js", html)

    def test_plain_workflows_get_clickable_dots_over_the_number_input(self):
        html = self.client.get(self.url(self.mage())).content.decode()
        self.assertRegex(html, r'<input type="number" name="strength"[^>]*class="tg-dots-number"')
        self.assertIn(
            '<span class="tg-dots-control" data-dot-rating data-min="1" data-max="5">', html
        )
        self.assertIn(
            '<span class="tg-dot-buttons" role="group" aria-label="Strength" hidden>', html
        )
        self.assertIn(
            '<button type="button" class="tg-dot is-filled" data-value="1" '
            'aria-label="Strength 1" aria-pressed="true"></button>',
            html,
        )
        self.assertIn(
            '<button type="button" class="tg-dot" data-value="2" '
            'aria-label="Strength 2" aria-pressed="false"></button>',
            html,
        )
        self.assertIn("widgets/dot_rating.js", html)
        # No Alpine, htmx or their hooks on a plain workflow.
        self.assertNotIn("x-data", html)
        self.assertNotIn("x-ref", html)
        self.assertNotIn("htmx.min.js", html)

    def test_saved_dots_imply_the_ranking_shown(self):
        character = self.mage()
        Mage.objects.filter(pk=character.pk).update(
            strength=1, charisma=4, manipulation=3, appearance=3, perception=3, intelligence=2
        )
        html = self.client.get(self.url(character)).content.decode()
        for group, rank in (("social", "Primary"), ("mental", "Secondary"), ("physical", "Tertiary")):
            self.assertIn(f'<small data-inferred-priority>{rank}</small>', section(html, group))
        self.assertIn('id="social-status" data-priority-count>done<', html)
        self.assertIn('id="physical-status" data-priority-count>3 left<', html)


class AttributeRankValidationTests(PriorityTestCase):
    def test_chosen_ranks_that_match_the_dots_advance(self):
        character = self.mage()
        data = {
            **ATTRIBUTES,
            "strength": 2,
            "charisma": 4,
            "manipulation": 4,
            **ranks("secondary", "primary", "tertiary"),
        }
        response = self.client.post(self.url(character), data)
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual((character.creation_status, character.charisma), (2, 4))

    def test_posted_ranks_cannot_override_dots(self):
        character = self.mage()
        response = self.client.post(
            self.url(character), {**ATTRIBUTES, **ranks("secondary", "primary", "tertiary")}
        )
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual((character.creation_status, character.strength), (2, 4))

    def test_missing_ranks_are_inferred_from_the_dots(self):
        character = self.mage()
        # Physical 6, Social 8, Mental 10.
        data = {
            **ATTRIBUTES,
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
        }
        response = self.client.post(self.url(character), data)
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual((character.creation_status, character.perception), (2, 4))

    def test_repeated_rank_is_ignored(self):
        character = self.mage()
        response = self.client.post(
            self.url(character), {**ATTRIBUTES, **ranks("primary", "primary", "tertiary")}
        )
        self.assertEqual(response.status_code, 302)

    def test_unknown_rank_values_count_as_no_choice(self):
        # Clients that post every field with a placeholder still get the inference.
        character = self.mage()
        response = self.client.post(self.url(character), {**ATTRIBUTES, **ranks("0", "0", "x")})
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 2)
        # A mixed set of old picker values is likewise ignored.
        character = self.mage()
        response = self.client.post(
            self.url(character), {**ATTRIBUTES, **ranks("first", "secondary", "tertiary")}
        )
        self.assertEqual(response.status_code, 302)


class AbilityPickerTests(PriorityTestCase):
    def test_mage_columns_rank_the_same_fields_the_rule_counts(self):
        character = self.mage(step=2)
        response = self.client.get(self.url(character))
        html = response.content.decode()
        rule = MageAbilityView(object=character).get_allocation_rules()[0]
        for group, names in rule.groups:
            with self.subTest(group=group):
                column = section(html, group)
                shown = re.findall(r'<input type="number" name="(\w+)"', column)
                self.assertEqual(sorted(shown), sorted(names))
                self.assertNotIn(f'name="priority_{group}"', column)
                self.assertIn(f'id="{group}-status"', column)
        self.assertIn('<small data-inferred-priority>Primary</small>', section(html, "talents"))
        self.assertIn('id="talents-status" data-priority-count>13 left<', html)
        self.assertIn('id="knowledges-status" data-priority-count>5 left<', html)
        self.assertIn('data-dot-rating data-min="0" data-max="3"', html)
        self.assertIn('id="abilities-validation-status"', html)

    def test_ability_ranks_are_validated(self):
        character = self.mage(step=2)
        abilities = {
            **{name: 0 for name in Mage.primary_abilities},
            "alertness": 3,
            "athletics": 3,
            "awareness": 3,
            "brawl": 3,
            "empathy": 1,
            "crafts": 3,
            "drive": 3,
            "etiquette": 3,
            "academics": 3,
            "computer": 2,
        }
        swapped = {
            **abilities,
            "priority_talents": "secondary",
            "priority_skills": "primary",
            "priority_knowledges": "tertiary",
        }
        response = self.client.post(self.url(character), swapped)
        self.assertEqual(response.status_code, 302)
        chosen = {
            **abilities,
            "priority_talents": "primary",
            "priority_skills": "secondary",
            "priority_knowledges": "tertiary",
        }
        character.creation_status = 2
        character.save(update_fields=["creation_status"])
        self.assertEqual(self.client.post(self.url(character), chosen).status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 3)


class InteractivePickerTests(PriorityTestCase):
    def vampire(self, step=1):
        return Vampire.objects.create(name="Pilot", owner=self.owner, creation_status=step)

    def test_interactive_steps_render_the_picker_beside_alpine_dots(self):
        html = self.client.get(self.url(self.vampire())).content.decode()
        self.assertIn("data-priority-picker", section(html, "mental"))
        self.assertIn('x-data="tgDots" data-min="1" data-max="5"', html)
        self.assertNotIn("data-dot-rating", html)
        self.assertNotIn("widgets/dot_rating.js", html)
        self.assertIn("characters/js/chargen-priority.js", html)
        abilities = self.client.get(self.url(self.vampire(step=2))).content.decode()
        self.assertRegex(section(abilities, "skills"), r'value="secondary" data-target="9" checked')
        self.assertIn('id="abilities-1"', abilities)

    def test_validation_reports_each_group_against_its_chosen_rank(self):
        character = self.vampire()
        response = self.client.post(
            self.url(character),
            {**ATTRIBUTES, **ranks("secondary", "primary", "tertiary"), "_validate": "1"},
            headers=HX,
        )
        self.assertEqual(response["TG-Fragment"], "chargen-feedback")
        self.assertContains(response, "as ranked (Physical secondary, Social primary")
        self.assertContains(response, "Physical 10/8 (2 over)")
        self.assertContains(response, "Social 8/10 (2 left)")
        # The dots fit 10/8/6 in total, but Physical is above its chosen target.
        self.assertContains(response, '<span class="tl-chargen__tag is-over">Too many</span>')
        ready = self.client.post(
            self.url(character),
            {**ATTRIBUTES, **ranks("primary", "secondary", "tertiary"), "_validate": "1"},
            headers=HX,
        )
        self.assertContains(ready, "Ready to save.")
        self.assertContains(ready, "Physical 10/10 (done)")
