"""Real-browser tests for the PRI / SEC / TER picker and the clickable dots.

Mage is a plain (non-interactive) workflow: its dots come from
widgets/dot_rating.js and its counts from chargen-priority.js, with no Alpine
or htmx. The Vampire pilot shows the same picker beside its Alpine dots.
Skips without playwright or Chromium, like test_chargen_interactive.
"""

from django.urls import reverse

from characters.models.mage.mage import Mage
from characters.tests.browser.test_chargen_interactive import BrowserTestCase


class PlainWorkflowTests(BrowserTestCase):
    def mage(self, step=1):
        return Mage.objects.create(name="Plain", owner=self.owner, creation_status=step)

    def open_plain(self, character):
        self.page.goto(self.live_server_url + reverse("characters:character", args=[character.pk]))
        self.page.wait_for_function("window.TGDots && window.TGPriority")

    def count(self, group):
        return self.page.inner_text(f"#{group}-status")

    def rank(self, group):
        return self.page.eval_on_selector(
            f'input[name="priority_{group}"]:checked', "radio => radio.value"
        )

    def choose(self, group, rank):
        self.page.click(f'label[for="id_priority_{group}_{rank}"]')

    def dot(self, name, value):
        return f'.tg-dots-control:has(input[name="{name}"]) .tg-dot[data-value="{value}"]'

    def plain_value(self, name):
        return self.page.input_value(f'form.tl-chargen [name="{name}"]')

    def test_dots_drive_the_input_and_the_counts(self):
        self.open_plain(self.mage())
        self.assertTrue(self.page.is_hidden('input[name="strength"]'))
        self.assertTrue(self.page.is_visible(self.dot("strength", 5)))
        self.assertEqual(self.page.locator("[x-data]").count(), 0)
        self.assertEqual(self.count("physical"), "7 left")
        self.dots("strength", 4)
        self.assertEqual(self.plain_value("strength"), "4")
        self.assertEqual(self.page.get_attribute(self.dot("strength", 4), "aria-pressed"), "true")
        self.assertIn("is-filled", self.page.get_attribute(self.dot("strength", 3), "class"))
        self.assertEqual(self.count("physical"), "4 left")
        self.dots("strength", 4)  # the current top dot lowers the rating by one
        self.assertEqual(self.plain_value("strength"), "3")
        self.dots("strength", 1)
        self.dots("strength", 1)  # never below the rule's minimum
        self.assertEqual(self.plain_value("strength"), "1")
        # Keyboard: the dots are buttons.
        self.page.focus(self.dot("dexterity", 3))
        self.page.keyboard.press("Enter")
        self.assertEqual(self.plain_value("dexterity"), "3")
        self.page.focus(self.dot("stamina", 5))
        self.page.keyboard.press("Space")
        self.assertEqual(self.plain_value("stamina"), "5")
        self.assertEqual(self.count("physical"), "1 left")
        self.dots("strength", 2)
        self.assertEqual(self.count("physical"), "done")
        self.dots("strength", 3)
        self.assertEqual(self.count("physical"), "1 over")
        self.assertIn("is-over", self.page.get_attribute("#physical-status", "class"))
        self.assertEqual(self.errors, [])

    def test_choosing_a_taken_rank_swaps_and_retargets(self):
        self.open_plain(self.mage())
        self.assertEqual(
            [self.rank(g) for g in ("physical", "social", "mental")],
            ["primary", "secondary", "tertiary"],
        )
        self.choose("mental", "primary")
        self.assertEqual(
            [self.rank(g) for g in ("physical", "social", "mental")],
            ["tertiary", "secondary", "primary"],
        )
        self.assertEqual(
            [self.count(g) for g in ("physical", "social", "mental")],
            ["3 left", "5 left", "7 left"],
        )
        # Keyboard: arrows move within one radio group, and the swap follows.
        self.page.focus("#id_priority_social_secondary")
        self.page.keyboard.press("ArrowLeft")
        self.assertEqual(
            [self.rank(g) for g in ("physical", "social", "mental")],
            ["tertiary", "primary", "secondary"],
        )
        # Fill the chosen targets: Physical 6, Social 10, Mental 8.
        for name, value in (
            ("strength", 2),
            ("dexterity", 2),
            ("stamina", 2),
            ("charisma", 4),
            ("manipulation", 3),
            ("appearance", 3),
            ("perception", 3),
            ("intelligence", 3),
            ("wits", 2),
        ):
            self.dots(name, value)
        self.assertEqual(
            [self.count(g) for g in ("physical", "social", "mental")], ["done", "done", "done"]
        )
        self.assertEqual(self.page.text_content("[data-allocation-tag]"), "Ready")
        # A swap that no longer fits the dots is reported at once.
        self.choose("physical", "primary")
        self.assertEqual(self.rank("social"), "tertiary")
        self.assertEqual(self.count("physical"), "4 left")
        self.assertEqual(self.count("social"), "4 over")
        self.assertIn("is-over", self.page.get_attribute("#social-status", "class"))
        self.assertEqual(self.page.text_content("[data-allocation-tag]"), "Too many")
        self.choose("physical", "tertiary")
        self.choose("social", "primary")
        self.page.click("form.tl-chargen button.tl-btn[type='submit']:not([formaction])")
        self.page.wait_for_selector("h1:has-text('Abilities')")
        character = Mage.objects.get(name="Plain")
        self.assertEqual((character.creation_status, character.charisma), (2, 4))
        self.assertEqual(self.errors, [])

    def test_abilities_count_against_the_chosen_ranks(self):
        self.open_plain(self.mage(step=2))
        self.assertEqual(self.count("talents"), "13 left")
        self.choose("knowledges", "primary")
        self.assertEqual(self.rank("talents"), "tertiary")
        self.assertEqual(
            [self.count(g) for g in ("talents", "skills", "knowledges")],
            ["5 left", "9 left", "13 left"],
        )
        self.dots("alertness", 3)
        self.dots("academics", 2)
        self.assertEqual(self.count("talents"), "2 left")
        self.assertEqual(self.count("knowledges"), "11 left")
        self.assertIn("as ranked", self.page.inner_text("#abilities-validation-status"))
        self.assertEqual(self.errors, [])

    def test_phone_tap_targets(self):
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.open_plain(self.mage())
        box = self.page.locator(self.dot("strength", 1)).bounding_box()
        self.assertEqual((round(box["width"]), round(box["height"])), (32, 44))
        segment = self.page.locator('label[for="id_priority_physical_primary"]').bounding_box()
        self.assertGreaterEqual(segment["height"], 44)
        overflow = self.page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        self.assertFalse(overflow)


class InteractiveWorkflowTests(BrowserTestCase):
    def test_picker_swaps_and_the_pool_and_verdict_follow_the_ranks(self):
        self.open(self.vampire(1))
        self.page.click('label[for="id_priority_mental_primary"]')
        self.assertEqual(
            self.page.eval_on_selector(
                'input[name="priority_physical"]:checked', "radio => radio.value"
            ),
            "tertiary",
        )
        self.assertEqual(self.page.inner_text("#mental-status"), "7 left")
        self.assertIn("Mental 3/10", self.page.inner_text(".tl-chargen__pool"))
        self.dots("strength", 5)
        self.assertEqual(self.page.inner_text("#physical-status"), "1 over")
        self.page.wait_for_function(
            "document.querySelector('#chargen-feedback').innerText.includes('Physical 7/6')"
        )
        self.assertIn("Physical 7/6 (1 over)", self.feedback())
        self.assertIn(
            "as ranked (Physical tertiary, Social secondary, Mental primary)", self.feedback()
        )
        self.assertEqual(self.errors, [])
