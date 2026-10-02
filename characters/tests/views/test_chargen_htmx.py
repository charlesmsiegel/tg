"""The htmx request/response contract of interactive chargen (Vampire pilot).

See docs/architecture/character-creation.md. Every mode is
served by the ordinary wizard URL, so every test goes through the router,
the middleware and ``CHARGEN_STEP`` exactly as a browser request would.
"""

import json
import re

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.chargen import get_workflow
from characters.chargen.definitions import WORKFLOWS
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire

HX = {"HX-Request": "true"}
ATTRIBUTES_VALID = {
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
WRITES = re.compile(r"^\s*(INSERT|UPDATE|DELETE)\b", re.IGNORECASE)


def writes(queries):
    return [q["sql"] for q in queries if WRITES.match(q["sql"])]


class InteractiveChargenTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("owner", password="pw")
        cls.other = User.objects.create_user("other", password="pw")
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.presence = Discipline.objects.create(name="Presence", property_name="presence")
        cls.brujah = VampireClan.objects.create(name="Brujah")
        cls.brujah.disciplines.add(cls.potence, cls.celerity, cls.presence)
        cls.resources, _ = Background.objects.get_or_create(
            name="Resources", property_name="resources"
        )

    def setUp(self):
        self.client.login(username="owner", password="pw")

    def vampire(self, step, **fields):
        fields.setdefault("clan", self.brujah)
        return Vampire.objects.create(
            name="Pilot", owner=self.owner, creation_status=step, **fields
        )

    def url(self, character):
        return reverse("characters:character", kwargs={"pk": character.pk})

    def browser_data(self, character, **changes):
        """What a browser posts for the current step: every field's shown value."""
        form = self.client.get(self.url(character)).context["form"]
        forms = [form]
        if hasattr(form, "management_form"):
            forms = [form.management_form, *form.forms]
        data = {}
        for each in forms:
            for name in each.fields:
                value = each[name].value()
                if value is not None and value is not False:
                    data[each.add_prefix(name)] = value
        data.update(changes)
        return data


class RegistryFlagTests(TestCase):
    def test_only_the_pilot_workflow_is_interactive(self):
        interactive = {key for key, workflow in WORKFLOWS.items() if workflow.interactive}
        self.assertEqual(interactive, {"vampire"})


class FullPageAndFragmentTests(InteractiveChargenTestCase):
    def test_full_page_renders_interactive_shell_with_vendored_scripts(self):
        character = self.vampire(1)
        response = self.client.get(self.url(character))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="chargen-root"')
        self.assertContains(response, '<form id="chargen-step"')
        self.assertContains(response, f'hx-post="{self.url(character)}"')
        self.assertContains(response, "vendor/htmx/2.0.11/htmx.min.js")
        self.assertContains(response, 'integrity="sha384-')
        self.assertContains(response, "characters/js/chargen-components.js")
        self.assertContains(response, "<html")
        for header in ("HX-Request", "HX-History-Restore-Request", "HX-Boosted"):
            self.assertIn(header, response["Vary"])
        self.assertNotIn("TG-Fragment", response)

    def test_fragment_is_the_form_plus_out_of_band_progress_and_messages(self):
        character = self.vampire(2)
        response = self.client.get(self.url(character), headers=HX)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["TG-Fragment"], "chargen-step")
        self.assertIn("HX-Request", response["Vary"])
        html = response.content.decode()
        self.assertNotIn("<html", html)
        self.assertTrue(html.lstrip().startswith('<form id="chargen-step"'))
        self.assertIn('data-step="abilities"', html)
        self.assertRegex(html, r'<div id="chargen-progress" hx-swap-oob="true">')
        self.assertRegex(html, r'<div id="tg-messages"[^>]*hx-swap-oob="true"')
        self.assertTemplateUsed(response, "characters/core/chargen/step_fragment.html")
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/ability_block_form.html")

    def test_history_restore_and_boosted_requests_get_full_pages(self):
        character = self.vampire(1)
        for extra in ({"HX-History-Restore-Request": "true"}, {"HX-Boosted": "true"}):
            with self.subTest(extra=extra):
                response = self.client.get(self.url(character), headers={**HX, **extra})
                self.assertContains(response, "<html")
                self.assertNotIn("TG-Fragment", response)

    def test_every_pilot_step_renders_as_fragment(self):
        character = self.vampire(1, freebies=15, freebies_approved=True)
        workflow = get_workflow("vampire")
        for position, step in enumerate(workflow.steps, 1):
            with self.subTest(step=step.key):
                Vampire.objects.filter(pk=character.pk).update(creation_status=position)
                response = self.client.get(self.url(character), headers=HX)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["TG-Fragment"], "chargen-step")
                self.assertContains(response, f'data-step="{step.key}"')

    def test_valid_post_redirects_inside_the_wizard_and_the_follow_is_a_fragment(self):
        character = self.vampire(1)
        response = self.client.post(self.url(character), ATTRIBUTES_VALID, headers=HX)
        self.assertRedirects(response, self.url(character), fetch_redirect_response=False)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 2)
        # Browsers keep HX-Request when an XHR follows a same-origin redirect.
        follow = self.client.get(response["Location"], headers=HX)
        self.assertEqual(follow["TG-Fragment"], "chargen-step")
        self.assertContains(follow, 'data-step="abilities"')

    def test_invalid_post_rerenders_the_step_fragment_with_errors(self):
        character = self.vampire(1)
        response = self.client.post(
            self.url(character), {**ATTRIBUTES_VALID, "strength": 5}, headers=HX
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["TG-Fragment"], "chargen-step")
        self.assertContains(response, 'id="chargen-errors"')
        self.assertContains(response, "Attributes must be distributed 7/5/3")
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 1)

    def test_terminal_step_leaves_the_wizard_with_hx_redirect(self):
        character = self.vampire(13)
        response = self.client.post(self.url(character), {}, headers=HX)
        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Redirect"], character.get_absolute_url())

    def test_router_sends_a_character_outside_the_wizard_to_a_full_page(self):
        character = self.vampire(13)
        Vampire.objects.filter(pk=character.pk).update(status="Sub")
        response = self.client.get(self.url(character), headers=HX)
        self.assertEqual(response["HX-Redirect"], character.get_absolute_url())
        # The character's own page renders the sheet through the router's
        # declared detail fallback.
        page = self.client.get(self.url(character))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "characters/vampire/vampire/detail.html")

    def test_back_through_htmx_returns_previous_step_fragment_and_messages(self):
        character = self.vampire(3)
        back = reverse("characters:chargen_back", kwargs={"pk": character.pk})
        response = self.client.post(back, headers=HX)
        self.assertRedirects(response, self.url(character), fetch_redirect_response=False)
        follow = self.client.get(self.url(character), headers=HX)
        self.assertContains(follow, 'data-step="abilities"')
        self.assertContains(follow, f'hx-post="{back}"')

    def test_messages_are_delivered_out_of_band(self):
        character = self.vampire(4)
        data = self.browser_data(character, potence=1, celerity=1, presence=1)
        self.assertEqual(self.client.post(self.url(character), data, headers=HX).status_code, 302)
        follow = self.client.get(self.url(character), headers=HX)
        self.assertContains(follow, "Disciplines allocated successfully!")
        # Drained: the next full page does not repeat it.
        self.assertNotContains(self.client.get(self.url(character)), "allocated successfully")


class NonInteractiveWorkflowTests(InteractiveChargenTestCase):
    def test_other_gamelines_ignore_htmx_headers(self):
        ghoul = Ghoul.objects.create(name="Ghoul", owner=self.owner, creation_status=1)
        for headers in ({}, HX):
            with self.subTest(headers=headers):
                response = self.client.get(self.url(ghoul), headers=headers)
                self.assertContains(response, "<html")
                self.assertNotContains(response, 'id="chargen-step"')
                self.assertNotContains(response, "htmx.min.js")
                self.assertNotContains(response, "x-data")
                self.assertContains(response, "characters/js/attribute-validation.js")
                self.assertNotIn("TG-Fragment", response)

    def test_other_gamelines_ignore_validate_and_options_params(self):
        ghoul = Ghoul.objects.create(name="Ghoul", owner=self.owner, creation_status=1)
        response = self.client.post(
            self.url(ghoul), {**ATTRIBUTES_VALID, "_validate": "1"}, headers=HX
        )
        # Handled as an ordinary submit: a redirect or a full page, never feedback.
        self.assertIn(response.status_code, {200, 302})
        self.assertNotIn("TG-Fragment", response)
        if response.status_code == 200:
            self.assertContains(response, "<html")


class ValidateOnlyTests(InteractiveChargenTestCase):
    def validate(self, character, data, **headers):
        return self.client.post(
            self.url(character), {**data, "_validate": "1"}, headers={**HX, **headers}
        )

    def test_invalid_allocation_reports_first_error_and_totals_without_writing(self):
        character = self.vampire(1)
        with CaptureQueriesContext(connection) as queries:
            response = self.validate(character, {**ATTRIBUTES_VALID, "strength": 5})
        self.assertEqual(writes(queries.captured_queries), [])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["TG-Fragment"], "chargen-feedback")
        self.assertEqual(response["TG-Step"], "attributes")
        self.assertContains(response, "Attributes must be distributed 7/5/3")
        self.assertContains(response, "Physical 11")
        self.assertContains(response, "need 10/8/6")
        # One dot more than the 10/8/6 targets hold in total.
        self.assertContains(response, '<span class="tl-chargen__tag is-over">Too many</span>')
        character.refresh_from_db()
        self.assertEqual((character.creation_status, character.strength), (1, 1))

    def test_misshapen_allocation_within_budget_is_in_progress(self):
        character = self.vampire(1)
        response = self.validate(character, {**ATTRIBUTES_VALID, "strength": 3, "wits": 3})
        self.assertContains(response, "Attributes must be distributed 7/5/3")
        self.assertContains(response, '<span class="tl-chargen__tag">In progress</span>')
        self.assertNotContains(response, "Too many")

    def test_valid_allocation_is_ready_but_never_saved_or_advanced(self):
        character = self.vampire(1)
        with CaptureQueriesContext(connection) as queries:
            response = self.validate(character, ATTRIBUTES_VALID)
        self.assertEqual(writes(queries.captured_queries), [])
        self.assertContains(response, "Ready to save.")
        self.assertContains(response, '<span class="tl-chargen__tag is-ready">Ready</span>')
        character.refresh_from_db()
        self.assertEqual((character.creation_status, character.strength), (1, 1))

    def test_verdict_matches_submit_for_virtues(self):
        character = self.vampire(5)
        for changes, ok in (
            ({"conscience": 3, "self_control": 2, "courage": 2}, True),
            ({"conscience": 3, "self_control": 3, "courage": 3}, False),
        ):
            data = self.browser_data(character, **changes)
            with self.subTest(changes=changes):
                feedback = self.validate(character, data)
                self.assertEqual("Ready to save." in feedback.content.decode(), ok)
                submit = self.client.post(self.url(character), data, headers=HX)
                self.assertEqual(submit.status_code == 302, ok)
                Vampire.objects.filter(pk=character.pk).update(creation_status=5)

    def test_background_totals_use_the_formset_arithmetic(self):
        character = self.vampire(3)
        resources = self.resources
        data = {
            "backgrounds-TOTAL_FORMS": "1",
            "backgrounds-INITIAL_FORMS": "0",
            "backgrounds-MIN_NUM_FORMS": "0",
            "backgrounds-MAX_NUM_FORMS": "1000",
            "backgrounds-0-bg": resources.pk,
            "backgrounds-0-rating": 3,
        }
        with CaptureQueriesContext(connection) as queries:
            response = self.validate(character, data)
        self.assertEqual(writes(queries.captured_queries), [])
        self.assertContains(response, "Background points:")
        self.assertContains(response, f"{3 * resources.multiplier} / {character.background_points}")
        self.assertFalse(BackgroundRating.objects.filter(char=character).exists())

    def test_skippable_step_is_not_advanced_by_validation(self):
        character = self.vampire(9)  # allies, with no Allies background: skipped
        response = self.validate(character, {})
        self.assertEqual(response.status_code, 204)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 9)

    def test_freebies_awaiting_approval_answer_no_content(self):
        character = self.vampire(7, freebies=15, freebies_approved=False)
        self.assertEqual(self.validate(character, {"category": "Willpower"}).status_code, 204)

    def test_freebies_report_the_remaining_pool_and_never_spend(self):
        character = self.vampire(7, freebies=15, freebies_approved=True)
        # Building the form lazily creates reference rows (ObjectType); any
        # render does that, so warm it first and require no further writes.
        self.client.get(self.url(character))
        with CaptureQueriesContext(connection) as queries:
            response = self.validate(character, {"category": "Willpower"})
        self.assertEqual(writes(queries.captured_queries), [])
        self.assertContains(response, "Freebies remaining:")
        # The spending service only runs on submit, so a clean form is not
        # announced as a guaranteed save.
        self.assertNotContains(response, "Ready to save.")
        self.assertContains(response, "No problems found so far")
        character.refresh_from_db()
        self.assertEqual(character.freebies, 15)

    def test_freebies_feedback_runs_the_submits_choice_resolution(self):
        character = self.vampire(7, freebies=15, freebies_approved=True)
        # The chained form accepts a Discipline without a trait; the submit's
        # get_spending_kwargs() refuses it, and so must the live feedback.
        response = self.validate(character, {"category": "Discipline"})
        self.assertContains(response, "Must Choose Trait")
        self.assertNotContains(response, "No problems found")
        submit = self.client.post(self.url(character), {"category": "Discipline"}, headers=HX)
        self.assertContains(submit, "Must Choose Trait")

    @override_settings(CHARGEN_PARTIAL_LIMIT=2)
    def test_partial_requests_are_throttled_per_character(self):
        cache.clear()
        character = self.vampire(1)
        codes = [self.validate(character, ATTRIBUTES_VALID).status_code for _ in range(3)]
        self.assertEqual(codes, [200, 200, 204])

    def test_validate_without_hx_request_is_an_ordinary_submit(self):
        character = self.vampire(1)
        response = self.client.post(self.url(character), {**ATTRIBUTES_VALID, "_validate": "1"})
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 2)


class OptionsTests(InteractiveChargenTestCase):
    def setUp(self):
        super().setUp()
        self.character = self.vampire(7, freebies=15, freebies_approved=True)

    def options(self, **params):
        return self.client.get(self.url(self.character), params, headers=HX)

    def test_child_options_come_from_the_steps_own_form(self):
        response = self.options(_options="example", category="Discipline")
        self.assertEqual(response["TG-Fragment"], "chargen-options")
        self.assertEqual(response["TG-Step"], "freebies")
        html = response.content.decode()
        self.assertIn(f'<option value="{self.potence.pk}">Potence</option>', html)
        self.assertIn('<option value="">---------</option>', html)
        # The grandchild is reset out of band.
        self.assertIn('<select id="id_value" hx-swap-oob="innerHTML">', html)
        # Applied only if the options are actually swapped in (not on a
        # response the client drops as stale).
        self.assertNotIn("HX-Trigger", response)
        visibility = json.loads(response["HX-Trigger-After-Swap"])["tg-visibility"]
        self.assertEqual(
            visibility,
            {"example": True, "value": False, "note": False, "pooled": False},
        )
        self.assertEqual(json.loads(response["TG-Chain"]), {"category": "Discipline"})

    def test_visibility_follows_the_selected_example_metadata(self):
        resources = self.resources
        response = self.options(
            _options="value", category="Background", example=f"bg_{resources.pk}"
        )
        visibility = json.loads(response["HX-Trigger-After-Swap"])["tg-visibility"]
        self.assertEqual(
            json.loads(response["TG-Chain"]),
            {"category": "Background", "example": f"bg_{resources.pk}"},
        )
        self.assertTrue(visibility["note"])
        self.assertFalse(visibility["pooled"])  # not a group member

    def test_unknown_and_root_fields_are_rejected(self):
        for name in ("category", "note", "owner", "nope"):
            with self.subTest(name=name):
                self.assertEqual(self.options(_options=name).status_code, 400)

    def test_full_page_uses_server_options_not_embedded_trees(self):
        strength = Attribute.objects.create(name="Strength", property_name="strength")
        cache.clear()  # the freebie form reads Attributes through the reference cache
        response = self.client.get(self.url(self.character))
        self.assertNotContains(response, "data-chain-tree")
        self.assertNotContains(response, "widgets/chained.js")
        self.assertNotContains(response, "widgets/conditional.js")
        self.assertNotContains(response, "data-conditional-rules")
        self.assertContains(response, 'hx-vals="{&quot;_options&quot;: &quot;example&quot;}"')
        self.assertContains(response, 'hx-include="#id_category, #id_example, #id_value"')
        # The first affordable category (Attribute) needs a trait but no rating.
        html = response.content.decode()
        self.assertNotRegex(html, r'id="example_wrap"[^>]* hidden')
        self.assertRegex(html, r'id="value_wrap"[^>]* hidden')
        # ...and its Trait select already offers the Attributes.
        example = re.search(r'<select name="example".*?</select>', html, re.S).group(0)
        self.assertIn(f'<option value="{strength.pk}">Strength</option>', example)

    def test_cost_table_comes_from_the_cost_source(self):
        response = self.client.get(self.url(self.character))
        self.assertContains(response, "<td>Discipline</td><td>7</td>")
        self.assertContains(response, "<td>MeritFlaw</td><td>Rating</td>")


class NoJavaScriptTests(InteractiveChargenTestCase):
    def test_chained_freebies_work_in_two_round_trips(self):
        character = self.vampire(7, freebies=15, freebies_approved=True)
        first = self.client.post(self.url(character), {"category": "Discipline"})
        self.assertEqual(first.status_code, 200)
        self.assertContains(first, "Must Choose Trait")
        html = first.content.decode()
        self.assertIn(f'<option value="{self.potence.pk}">Potence</option>', html)
        self.assertNotRegex(html, r'id="example_wrap"[^>]* hidden')
        second = self.client.post(
            self.url(character), {"category": "Discipline", "example": self.potence.pk}
        )
        self.assertEqual(second.status_code, 302)
        character.refresh_from_db()
        self.assertEqual((character.potence, character.freebies), (1, 8))

    def test_bound_background_choice_with_option_metadata_rerenders(self):
        character = self.vampire(7, freebies=15, freebies_approved=True)
        response = self.client.post(self.url(character), {"category": "Background"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'<option value="bg_{self.resources.pk}">')
        self.assertNotRegex(response.content.decode(), r'id="note_wrap"[^>]* hidden')

    def test_dot_widget_keeps_the_number_input_as_the_control(self):
        character = self.vampire(1)
        html = self.client.get(self.url(character)).content.decode()
        self.assertRegex(html, r'<input type="number" name="strength"[^>]*x-ref="input"')
        self.assertIn('x-data="tgDots" data-min="1" data-max="5"', html)
        Vampire.objects.filter(pk=character.pk).update(creation_status=2)
        html = self.client.get(self.url(character)).content.decode()
        self.assertIn('x-data="tgDots" data-min="0" data-max="3"', html)


class AuthorizationTests(InteractiveChargenTestCase):
    def test_other_players_get_nothing_from_any_mode(self):
        character = self.vampire(1)
        self.client.login(username="other", password="pw")
        requests = (
            lambda: self.client.get(self.url(character), headers=HX),
            lambda: self.client.post(
                self.url(character), {**ATTRIBUTES_VALID, "_validate": "1"}, headers=HX
            ),
            lambda: self.client.post(self.url(character), ATTRIBUTES_VALID, headers=HX),
            lambda: self.client.get(
                self.url(character), {"_options": "example", "category": "Discipline"}, headers=HX
            ),
        )
        for request in requests:
            with CaptureQueriesContext(connection) as queries:
                response = request()
            self.assertNotIn(
                response.get("TG-Fragment"), {"chargen-step", "chargen-feedback", "chargen-options"}
            )
            self.assertEqual(writes(queries.captured_queries), [])
            self.assertNotContains(response, "chargen-step", status_code=response.status_code)
        character.refresh_from_db()
        self.assertEqual((character.creation_status, character.strength), (1, 1))

    def test_anonymous_requests_get_no_fragments(self):
        character = self.vampire(1)
        self.client.logout()
        for response in (
            self.client.get(self.url(character), headers=HX),
            self.client.post(self.url(character), {"_validate": "1"}, headers=HX),
        ):
            self.assertNotIn("TG-Fragment", response)
            self.assertNotContains(response, "chargen-step", status_code=response.status_code)

    def test_submitted_characters_accept_no_partials(self):
        character = self.vampire(7, freebies=15, freebies_approved=True)
        Vampire.objects.filter(pk=character.pk).update(status="Sub")
        response = self.client.get(
            self.url(character), {"_options": "example", "category": "Discipline"}, headers=HX
        )
        self.assertNotEqual(response.get("TG-Fragment"), "chargen-options")
