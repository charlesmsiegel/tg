"""The interactive Vampire wizard still works with JavaScript disabled.

Plain form posts (no HX-Request), exactly what a browser without scripts
sends: every rendered field with its current value plus the player's changes.
"""

from django.urls import reverse

from characters.models.core.background_block import Background
from characters.models.vampire.vampire import Vampire
from characters.tests.views.test_chargen_htmx import InteractiveChargenTestCase


class NoJavaScriptWalkthroughTests(InteractiveChargenTestCase):
    def post_step(self, character, key, **changes):
        page = self.client.get(self.url(character))
        self.assertEqual(page.context["step"].key, key)
        self.assertNotIn("TG-Fragment", page)
        data = self.browser_data(character, **changes)
        return self.client.post(self.url(character), data)

    def advance(self, character, key, **changes):
        response = self.post_step(character, key, **changes)
        errors = response.context["form"].errors if response.status_code == 200 else None
        self.assertEqual(response.status_code, 302, errors)
        return response

    def test_all_thirteen_steps_without_javascript(self):
        allies = Background.objects.get_or_create(name="Allies", property_name="allies")[0]
        character = self.vampire(1, freebies=15, freebies_approved=True)
        self.advance(
            character,
            "attributes",
            strength=4,
            dexterity=3,
            stamina=3,
            charisma=3,
            manipulation=3,
            appearance=2,
            perception=2,
            intelligence=2,
            wits=2,
        )
        self.advance(
            character,
            "abilities",
            alertness=3,
            athletics=3,
            awareness=3,
            brawl=3,
            empathy=1,
            animal_ken=3,
            crafts=3,
            drive=3,
            academics=3,
            computer=2,
        )
        # Without JS the page renders one background row; the second row
        # stands in for the formset's Add button, which has always needed JS
        # (formset_manager.js). A single-row allocation works without it.
        backgrounds = {
            "backgrounds-TOTAL_FORMS": "2",
            "backgrounds-0-bg": self.resources.pk,
            "backgrounds-0-rating": 4,
            "backgrounds-1-bg": allies.pk,
            "backgrounds-1-rating": 1,
        }
        self.advance(character, "backgrounds", **backgrounds)
        self.advance(character, "disciplines", potence=1, celerity=1, presence=1)
        self.advance(character, "virtues", conscience=3, self_control=2, courage=2)
        self.advance(character, "biography", age=150, apparent_age=25, date_of_birth="1875-03-01")

        # Chained freebies: first post the category alone; the bound
        # re-render offers that category's traits (the no-JS round trip).
        first = self.post_step(character, "freebies", category="Discipline")
        self.assertEqual(first.status_code, 200)
        self.assertContains(first, "Must Choose Trait")
        self.assertContains(first, f'<option value="{self.potence.pk}">Potence</option>')
        self.advance(character, "freebies", category="Discipline", example=self.potence.pk)
        for _ in range(8):
            self.advance(character, "freebies", category="Willpower")

        # Languages, Mentor, Contacts and Retainers do not apply and are skipped.
        self.advance(character, "allies", npc_type="vtmhuman", name="Loyal Ghoul", rank=1)
        response = self.advance(character, "specialties")

        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")
        self.assertEqual(character.freebies, 0)
        self.assertEqual((character.potence, character.celerity, character.presence), (2, 1, 1))
        self.assertEqual(character.backgrounds.get(bg=allies).complete, True)
        self.assertEqual(response["Location"], character.get_absolute_url())
        self.assertEqual(
            reverse("characters:character", kwargs={"pk": character.pk}), self.url(character)
        )
        self.assertIsInstance(character, Vampire)
