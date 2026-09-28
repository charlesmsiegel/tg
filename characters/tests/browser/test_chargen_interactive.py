"""Real-browser tests for interactive (htmx + Alpine) Vampire chargen.

Needs the ``playwright`` Python package and a Chromium binary; both are
development-only and the tests skip without them. The binary is taken from
TG_BROWSER_BINARY, then Playwright's own install, then the preinstalled
/opt/pw-browsers/chromium-*/chrome-linux/chrome. Never run ``playwright install``.
"""

import glob
import json
import os
import shutil
import unittest

from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse

from characters.models.core.background_block import Background
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.vampire import Vampire

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # development-only dependency
    sync_playwright = None


def chromium_binary():
    candidates = [os.environ.get("TG_BROWSER_BINARY")]
    candidates += sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True)
    candidates += [shutil.which("chromium"), shutil.which("chromium-browser")]
    return next((path for path in candidates if path and os.path.isfile(path)), None)


# Every test reuses the same user and character ids, and a walkthrough alone
# sends about 60 partial requests in seconds; the throttle has its own test.
@override_settings(CHARGEN_PARTIAL_LIMIT=10_000)
class BrowserTestCase(StaticLiveServerTestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        if sync_playwright is None:
            raise unittest.SkipTest("Install the playwright package to run browser tests")
        binary = chromium_binary()
        if binary is None:
            raise unittest.SkipTest("Set TG_BROWSER_BINARY to a Chromium binary")
        # Playwright's sync API runs an event loop in this thread; the ORM
        # calls made by the tests themselves are still synchronous.
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(executable_path=binary)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    def setUp(self):
        cache.clear()
        self.owner = User.objects.create_user("owner", password="pw")
        self.potence = Discipline.objects.create(name="Potence", property_name="potence")
        self.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        self.presence = Discipline.objects.create(name="Presence", property_name="presence")
        self.brujah = VampireClan.objects.create(name="Brujah")
        self.brujah.disciplines.add(self.potence, self.celerity, self.presence)
        self.resources = Background.objects.create(name="Resources", property_name="resources")
        self.allies = Background.objects.create(name="Allies", property_name="allies")
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(10000)
        # Only the live server is reachable; external CDNs (jQuery, fonts) are
        # cut off so the tests are deterministic. Bootstrap then fails on the
        # missing jQuery; that error is not the wizard's.
        self.context.route(
            "**/*",
            lambda route: (
                route.continue_()
                if route.request.url.startswith(self.live_server_url)
                else route.abort()
            ),
        )
        self.errors = []
        self.page.on(
            "pageerror",
            lambda error: "boot/js/bootstrap" not in (error.stack or "")
            and self.errors.append(str(error)),
        )
        self.page.on(
            "console",
            lambda message: message.type == "error"
            and not message.text.startswith("Failed to load resource")
            and self.errors.append(message.text),
        )
        self.login()

    def tearDown(self):
        self.context.close()

    def login(self):
        self.client.login(username="owner", password="pw")
        cookie = self.client.cookies["sessionid"]
        self.context.add_cookies(
            [{"name": "sessionid", "value": cookie.value, "url": self.live_server_url}]
        )

    def vampire(self, step, **fields):
        fields.setdefault("clan", self.brujah)
        return Vampire.objects.create(
            name="Pilot", owner=self.owner, creation_status=step, **fields
        )

    def open(self, character):
        self.page.goto(self.live_server_url + reverse("characters:character", args=[character.pk]))
        self.wait_ready()

    def wait_ready(self):
        self.page.wait_for_function("window.Alpine && window.htmx && window.TGChargen")

    def wait_step(self, key):
        self.page.wait_for_selector(f'form#chargen-step[data-step="{key}"]')
        self.page.wait_for_load_state("networkidle")

    def dots(self, name, value):
        self.page.click(f'.tg-dots-control:has(input[name="{name}"]) .tg-dot[data-value="{value}"]')

    def value(self, name):
        return self.page.input_value(f'#chargen-step [name="{name}"]')

    def feedback(self):
        return self.page.inner_text("#chargen-feedback")

    def save(self):
        self.page.click('#chargen-step button[type="submit"]:not([formaction])')


class AlpineComponentTests(BrowserTestCase):
    def test_dots_set_clamp_and_drive_the_pool(self):
        self.open(self.vampire(1))
        self.assertTrue(self.page.is_hidden('input[name="strength"]'))
        self.dots("strength", 4)
        self.assertEqual(self.value("strength"), "4")
        self.assertIn("Physical 6", self.page.inner_text(".tl-chargen__pool"))
        self.assertEqual(
            self.page.get_attribute(
                '.tg-dots-control:has(input[name="strength"]) .tg-dot[data-value="4"]',
                "aria-pressed",
            ),
            "true",
        )
        self.dots("strength", 4)  # clicking the top dot lowers it by one
        self.assertEqual(self.value("strength"), "3")
        self.dots("strength", 1)
        self.dots("strength", 1)  # never below the rule's minimum
        self.assertEqual(self.value("strength"), "1")
        self.assertEqual(
            self.page.locator('.tg-dots-control:has(input[name="alertness"])').count(), 0
        )
        self.assertEqual(self.errors, [])

    def test_validator_reports_server_verdict_after_debounce(self):
        self.open(self.vampire(1))
        self.page.wait_for_selector("#chargen-feedback .tl-chargen__line")
        self.dots("strength", 5)
        self.page.wait_for_function(
            "document.querySelector('#chargen-feedback').innerText.includes('Physical 7')"
        )
        self.assertIn("Attributes must be distributed 7/5/3", self.feedback())

    def test_chained_options_and_conditional_fields_come_from_the_server(self):
        self.open(self.vampire(7, freebies=15, freebies_approved=True))
        self.assertTrue(self.page.is_visible("#example_wrap"))
        self.assertTrue(self.page.is_hidden("#value_wrap"))
        self.page.select_option("#id_category", "Discipline")
        self.page.wait_for_selector(
            f'#id_example option[value="{self.potence.pk}"]', state="attached"
        )
        self.assertTrue(self.page.is_hidden("#note_wrap"))
        self.page.select_option("#id_category", "Background")
        self.page.wait_for_selector(
            f'#id_example option[value="bg_{self.resources.pk}"]', state="attached"
        )
        self.page.wait_for_selector("#note_wrap", state="visible")
        self.assertTrue(self.page.is_hidden("#pooled_wrap"))
        self.assertEqual(self.page.locator("script[data-chain-tree]").count(), 0)
        self.assertEqual(self.errors, [])


class ContractSafetyTests(BrowserTestCase):
    def test_validation_in_flight_at_save_never_paints_the_next_step(self):
        character = self.vampire(1)
        held = []

        def hold_validation(route):
            if "_validate" in (route.request.post_data or ""):
                held.append(route)
            else:
                route.continue_()

        self.open(character)
        self.page.wait_for_selector("#chargen-feedback .tl-chargen__line")
        self.page.route("**/characters/*/", hold_validation)
        for name, dots in (
            ("strength", 4),
            ("dexterity", 3),
            ("stamina", 3),
            ("charisma", 3),
            ("manipulation", 3),
            ("appearance", 2),
            ("perception", 2),
            ("intelligence", 2),
            ("wits", 2),
        ):
            self.dots(name, dots)
        self.page.wait_for_function("document.querySelector('#chargen-validator.htmx-request')")
        self.save()
        self.wait_step("abilities")
        for route in held:
            try:
                route.continue_()
            except Exception:  # already aborted by the page
                pass
        self.page.wait_for_timeout(500)
        self.assertNotIn("Physical", self.feedback())
        self.assertEqual(self.page.locator("form#chargen-step").count(), 1)

    def test_stale_options_answer_never_repaints_a_changed_chain(self):
        self.open(self.vampire(7, freebies=15, freebies_approved=True))
        held = []

        def hold_value_options(route):
            if "_options=value" in route.request.url:
                held.append(route)
            else:
                route.continue_()

        self.page.select_option("#id_category", "Background")
        self.page.wait_for_selector(
            f'#id_example option[value="bg_{self.resources.pk}"]', state="attached"
        )
        self.page.wait_for_selector("#note_wrap", state="visible")
        self.page.route("**/characters/*/?*", hold_value_options)
        self.page.select_option("#id_example", f"bg_{self.resources.pk}")
        self.page.wait_for_function("document.querySelector('#id_example.htmx-request')")
        # While that answer is held, the player picks another category.
        self.page.select_option("#id_category", "Discipline")
        self.page.wait_for_selector(
            f'#id_example option[value="{self.potence.pk}"]', state="attached"
        )
        self.page.wait_for_selector("#note_wrap", state="hidden")
        for route in held:
            route.continue_()
        self.page.wait_for_timeout(500)
        # The Background answer arrived last but belongs to the old chain.
        self.assertTrue(self.page.is_hidden("#note_wrap"))
        self.assertEqual(self.page.input_value("#id_category"), "Discipline")
        self.assertEqual(self.errors, [])

    def test_slow_options_swap_revalidates_the_reset_chain(self):
        self.open(self.vampire(7, freebies=15, freebies_approved=True))
        held = []

        def hold_example_options(route):
            if "_options=example" in route.request.url:
                held.append(route)
            else:
                route.continue_()

        self.page.select_option("#id_category", "Discipline")
        self.page.wait_for_selector(
            f'#id_example option[value="{self.potence.pk}"]', state="attached"
        )
        self.page.select_option("#id_example", str(self.potence.pk))
        self.page.route("**/characters/*/?*", hold_example_options)
        self.page.select_option("#id_category", "Willpower")
        # Validation runs first, with the new category and the old trait...
        self.page.wait_for_function(
            "document.querySelector('#chargen-feedback').innerText"
            ".includes('Invalid selection for the chosen category')"
        )
        # ...then the held options answer resets the trait.
        for route in held:
            route.continue_()
        self.page.wait_for_function(
            "document.querySelector('#chargen-feedback').innerText"
            ".includes('No problems found so far')"
        )
        self.assertEqual(self.page.input_value("#id_example"), "")
        self.assertEqual(self.errors, [])

    def test_non_fragment_response_loads_as_a_full_page(self):
        character = self.vampire(1)
        self.open(character)
        self.context.clear_cookies()  # session expired
        self.save()
        self.page.wait_for_load_state("load")
        self.page.wait_for_timeout(300)
        self.assertEqual(self.page.locator("#chargen-root").count(), 0)
        self.assertEqual(self.page.locator("html").count(), 1)


class WizardWalkthroughTests(BrowserTestCase):
    """All 13 Vampire steps on one page load; the terminal step navigates away."""

    def test_full_walkthrough_uses_one_page_load(self):
        character = self.vampire(1, freebies=15, freebies_approved=True)
        documents, xhrs = [], []
        self.page.on(
            "request",
            lambda request: (
                (documents if request.resource_type == "document" else xhrs).append(request.url)
                if request.resource_type in {"document", "xhr", "fetch"}
                else None
            ),
        )
        self.open(character)

        allocations = {
            "attributes": {
                "strength": 4,
                "dexterity": 3,
                "stamina": 3,
                "charisma": 3,
                "manipulation": 3,
                "appearance": 2,
                "perception": 2,
                "intelligence": 2,
                "wits": 2,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 3,
                "awareness": 3,
                "brawl": 3,
                "empathy": 1,
                "animal_ken": 3,
                "crafts": 3,
                "drive": 3,
                "academics": 3,
                "computer": 2,
            },
        }
        for key, ratings in allocations.items():
            self.wait_step(key)
            for name, dots in ratings.items():
                self.dots(name, dots)
            self.page.wait_for_function(
                "document.querySelector('#chargen-feedback').innerText.includes('Ready to save')"
            )
            self.save()

        self.wait_step("backgrounds")
        self.page.select_option('[name="backgrounds-0-bg"]', str(self.resources.pk))
        self.page.fill('[name="backgrounds-0-rating"]', "4")
        self.page.click("[data-formset-add]")
        self.page.select_option('[name="backgrounds-1-bg"]', str(self.allies.pk))
        self.page.fill('[name="backgrounds-1-rating"]', "1")
        self.page.wait_for_function(
            "document.querySelector('#chargen-feedback').innerText.includes('5 / 5')"
        )
        self.save()

        self.wait_step("disciplines")
        for name in ("potence", "celerity", "presence"):
            self.dots(name, 1)
        self.save()

        self.wait_step("virtues")
        for name, dots in (("conscience", 3), ("self_control", 2), ("courage", 2)):
            self.dots(name, dots)
        self.save()

        self.wait_step("biography")
        self.page.fill('[name="age"]', "150")
        self.page.fill('[name="apparent_age"]', "25")
        self.page.fill('[name="date_of_birth"]', "1875-03-01")
        self.save()

        self.wait_step("freebies")
        for category, example in (
            ("Discipline", str(self.potence.pk)),
            ("Willpower", None),
            ("Willpower", None),
            ("Willpower", None),
            ("Willpower", None),
            ("Willpower", None),
            ("Willpower", None),
            ("Willpower", None),
            ("Willpower", None),
        ):
            remaining = self.page.inner_text("#chargen-step p strong")
            self.page.select_option("#id_category", category)
            if example:
                self.page.wait_for_selector(
                    f'#id_example option[value="{example}"]', state="attached"
                )
                self.page.select_option("#id_example", example)
            self.save()
            self.page.wait_for_function(
                "r => { const s = document.querySelector('#chargen-step'); "
                "const p = s && s.querySelector('p strong'); "
                "return s.dataset.step !== 'freebies' || (p && p.innerText !== r); }",
                arg=remaining,
            )

        # Languages and the Mentor/Contacts/Retainers steps are skipped.
        self.wait_step("allies")
        self.page.select_option('[name="npc_type"]', "vtmhuman")
        self.page.fill('[name="name"]', "Loyal Ghoul")
        self.save()

        self.wait_step("specialties")
        progress = self.page.inner_text("#chargen-progress")
        self.assertIn("Specialties", progress)
        with self.page.expect_navigation():
            self.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")
        self.assertEqual(self.page.url, self.live_server_url + character.get_absolute_url())
        self.assertEqual(self.errors, [])
        # One page load for the wizard, one for the submitted character page.
        self.assertEqual(len(documents), 2, documents)
        self.__class__.walkthrough_requests = {"documents": len(documents), "xhr": len(xhrs)}
        print(f"\nWALKTHROUGH {json.dumps(self.__class__.walkthrough_requests)}")


class VisibilityParityTests(BrowserTestCase):
    """widgets/conditional.js and ConditionalFieldsMixin.field_visibility agree."""

    def test_browser_and_server_evaluators_agree(self):
        from widgets.tests.test_conditional_visibility import RULES, Form

        cases = [
            {"category": "-----"},
            {"category": "Willpower"},
            {"category": "MeritFlaw"},
            {"category": "Background", "example": "bg_1"},
            {"category": "Background", "example": "bg_2"},
            {"category": "Background", "example": "bg_1", "flag": True},
        ]
        script = finders.find("widgets/conditional.js")
        for member in (False, True):
            for case in cases:
                with self.subTest(case=case, member=member):
                    form = Form(conditional_context={"is_group_member": member})
                    expected = form.field_visibility(case)
                    wrappers = "".join(
                        f'<div id="{name}_wrap" class="d-none"></div>' for name in RULES
                    )
                    options = "".join(
                        f'<option value="{v}" {attrs}>{v}</option>'
                        for v, attrs in (
                            ("", ""),
                            ("bg_1", 'data-poolable="true" data-kind="a"'),
                            ("bg_2", 'data-poolable="false"'),
                        )
                    )
                    categories = "".join(
                        f"<option>{c}</option>"
                        for c in ("-----", "Willpower", "MeritFlaw", "Background")
                    )
                    rules = json.dumps({"rules": RULES, "context": {"is_group_member": member}})
                    # A fresh window: conditional.js refuses to load twice per window.
                    self.page.goto("about:blank")
                    self.page.set_content(
                        f'<select id="id_category">{categories}</select>'
                        f'<select id="id_example">{options}</select>'
                        f'<input type="checkbox" id="id_flag"{" checked" if case.get("flag") else ""}>'
                        f"{wrappers}"
                        f'<script type="application/json" data-conditional-rules>{rules}</script>'
                    )
                    self.page.select_option("#id_category", case["category"])
                    self.page.select_option("#id_example", case.get("example", ""))
                    self.page.add_script_tag(path=script)
                    actual = self.page.evaluate(
                        "names => Object.fromEntries(names.map(n => "
                        "[n, !document.getElementById(n + '_wrap').classList.contains('d-none')]))",
                        list(RULES),
                    )
                    self.assertEqual(actual, expected)
