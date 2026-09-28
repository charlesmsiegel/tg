"""The shared character create / edit forms and chargen steps render natively in Spread.

They render outside the legacy wrapper, carry no Bootstrap / tg-card markup, and
render every field of the form the view supplies: the old templates hard-coded a
field list and silently dropped fields (abilities on the gameline human edit form,
description / chronicle on the character form, allowed types on the merit form).
"""

import re

from django.contrib.auth.models import User
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import TestCase
from django.urls import reverse

from characters.models.core.archetype import Archetype
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.wraith.wtohuman import WtOHuman
from characters.tests.utils import human_setup
from core.models import CharacterTemplate

LEGACY = ('class="row', "col-sm", "tg-card", "tg-badge", "btn-primary", 'style="')


class SpreadFormAssertions:
    def assertNative(self, response):
        self.assertEqual(response.status_code, 200)
        main = response.content.decode().split('id="main"', 1)[0].rsplit("<main", 1)[1]
        self.assertNotIn("tl-legacy", main, "the form must render outside the legacy wrapper")
        body = response.content.decode().split('id="main"', 1)[1]
        for marker in LEGACY:
            self.assertNotIn(marker, body)

    def assertEveryFieldRendered(self, response):
        html = response.content.decode()
        form = response.context["form"]
        for name in form.fields:
            with self.subTest(field=name):
                self.assertRegex(html, rf'name="{re.escape(form.add_prefix(name))}"')


class TestCharacterFormsAreNative(SpreadFormAssertions, TestCase):
    @classmethod
    def setUpTestData(cls):
        human_setup()
        cls.admin = User.objects.create_superuser("admin", "admin@example.com", "pw")
        cls.owner = User.objects.create_user("owner", password="pw")
        Archetype.objects.get_or_create(name="Survivor")

    def setUp(self):
        self.client.login(username="admin", password="pw")

    def test_human_create_form(self):
        response = self.client.get(reverse("characters:create:human_full"))
        self.assertNative(response)
        self.assertEveryFieldRendered(response)
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, "tl-alloc__col")

    def test_human_basics_form(self):
        response = self.client.get(reverse("characters:create:human"))
        self.assertNative(response)
        self.assertEveryFieldRendered(response)

    def test_gameline_human_edit_form_renders_its_abilities(self):
        human = VtMHuman.objects.create(name="Edit Me", owner=self.owner)
        response = self.client.get(human.get_update_url())
        self.assertNative(response)
        self.assertIn("alertness", response.context["form"].fields)
        self.assertEveryFieldRendered(response)

    def test_character_create_form(self):
        response = self.client.get(reverse("characters:create:character"))
        self.assertNative(response)
        self.assertEveryFieldRendered(response)

    def test_merit_flaw_form_renders_allowed_types(self):
        response = self.client.get(reverse("characters:create:meritflaw"))
        self.assertNative(response)
        self.assertEveryFieldRendered(response)
        self.assertContains(response, 'name="allowed_types"')

    def test_specialty_and_reference_forms(self):
        for url in (reverse("characters:create:specialty"), reverse("characters:create:archetype")):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNative(response)
                self.assertEveryFieldRendered(response)

    def test_errors_use_the_summary(self):
        response = self.client.post(reverse("characters:create:specialty"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="tl-errsum"')
        self.assertContains(response, "tl-field is-invalid")


class TestTemplateSelectIsNative(SpreadFormAssertions, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("owner", password="pw")
        cls.template = CharacterTemplate.objects.create(
            name="Street Tough",
            gameline="vtm",
            character_type="vampire",
            concept="Enforcer",
            status="App",
            is_public=True,
        )

    def test_tiles_are_radios_with_scratch_checked(self):
        human = VtMHuman.objects.create(name="Picker", owner=self.owner, creation_status=0)
        self.client.login(username="owner", password="pw")
        url = reverse("characters:vampire:vtmhuman_template", kwargs={"pk": human.pk})
        response = self.client.get(url)
        self.assertNative(response)
        self.assertContains(response, 'type="radio" name="template" value="" checked')
        self.assertContains(response, f'name="template" value="{self.template.pk}"')
        self.assertNotContains(response, "template-select.js")

        response = self.client.post(url, {"template": ""})
        self.assertEqual(response.status_code, 302)
        human.refresh_from_db()
        self.assertEqual(human.creation_status, 1)


class TestBackgroundsStep(TestCase):
    """The step renders each rating's hidden id, so saving updates instead of duplicating."""

    def setUp(self):
        human_setup()
        self.owner = User.objects.create_user("owner", password="pw")
        self.char = WtOHuman.objects.create(name="Bg", owner=self.owner, creation_status=3)
        self.bg = Background.objects.filter(
            property_name__in=self.char.allowed_backgrounds, multiplier=1
        ).first()
        self.rating = BackgroundRating.objects.create(char=self.char, bg=self.bg, rating=2)
        self.client.login(username="owner", password="pw")

    def test_existing_rating_carries_its_id(self):
        response = self.client.get(self.char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertRegex(html, rf'name="backgrounds-0-id" value="{self.rating.pk}"')
        self.assertIn('class="tl-bgrow"', html)
        self.assertNotIn("col-sm", html)

    def test_saving_the_step_updates_the_existing_rating(self):
        budget = self.char.background_points
        response = self.client.post(
            self.char.get_absolute_url(),
            {
                "backgrounds-TOTAL_FORMS": "1",
                "backgrounds-INITIAL_FORMS": "1",
                "backgrounds-MIN_NUM_FORMS": "0",
                "backgrounds-MAX_NUM_FORMS": "1000",
                "backgrounds-0-id": str(self.rating.pk),
                "backgrounds-0-char": str(self.char.pk),
                "backgrounds-0-bg": str(self.bg.pk),
                "backgrounds-0-rating": str(budget),
                "backgrounds-0-note": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.char.backgrounds.count(), 1)
        self.rating.refresh_from_db()
        self.assertEqual(self.rating.rating, budget)


class TestLegacyLeftoversRemoved(TestCase):
    def test_unreferenced_legacy_templates_are_gone(self):
        for name in (
            "core/includes/scene_list.html",
            "core/includes/references.html",
            "core/includes/description.html",
            "core/includes/messages.html",
            "core/includes/title.html",
            "core/includes/status.html",
            "core/includes/buttons.html",
            "core/includes/image.html",
            "characters/core/character/char_scene_display.html",
            "characters/core/character/not_owner.html",
            "characters/core/human/basics_block_display.html",
            "characters/core/meritflaw/display_includes/meritflaw_block.html",
        ):
            with self.subTest(template=name):
                with self.assertRaises(TemplateDoesNotExist):
                    get_template(name)
