"""The item create / edit forms are native Spread markup and render every form field."""

import re

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from items.models.core.weapon import Weapon
from items.models.mage import Charm, SorcererArtifact
from items.models.mummy import Vessel
from items.models.vampire import VampireArtifact
from items.registry import registry

LEGACY_CLASS = re.compile(
    r"^(row|col(-[a-z0-9-]+)?|card[a-z-]*|btn[a-z-]*|tg-[a-z-]+|badge[a-z-]*|form-control"
    r"|form-row|form-check[a-z-]*|form-label|alert[a-z-]*|d-flex|text-[a-z]+|mb-[0-9]"
    r"|[a-z]+_heading)$"
)


def create_route(entry):
    name = next(name for name, _ in entry.actions["create"].routes)
    prefix = "" if entry.group == "core" else f"{entry.group}:"
    return f"items:{prefix}create:{name}"


def main_markup(response):
    """The page's <main> element (the form), without scripts."""
    html = response.content.decode()
    main = html[html.index("<main") : html.index("</main>")]
    return re.sub(r"<script[\s\S]*?</script>", "", main)


class ItemFormsSpreadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser("item_admin", "a@example.com", "pw")

    def setUp(self):
        self.client.force_login(self.admin)

    def assert_native_form(self, response):
        self.assertEqual(response.status_code, 200)
        main = main_markup(response)
        self.assertNotIn("tl-legacy", main.split(">", 1)[0], "form still in the legacy wrapper")
        legacy = [
            cls
            for value in re.findall(r'class="([^"]*)"', main)
            for cls in value.split()
            if LEGACY_CLASS.match(cls)
        ]
        self.assertEqual(legacy, [])
        self.assertNotIn('style="', main)
        form = response.context["form"]
        for field in form:
            self.assertIn(f'name="{field.html_name}"', main, f"{field.html_name} not rendered")

    def test_every_create_form_is_native_and_complete(self):
        for entry in registry:
            with self.subTest(model=entry.model_label):
                response = self.client.get(reverse(create_route(entry)))
                self.assert_native_form(response)

    def test_create_page_uses_the_item_gameline(self):
        response = self.client.get(reverse("items:mage:create:charm"))
        self.assertContains(response, 'data-gameline="mta"')
        self.assertContains(response, "tl-cover--line")

    def test_charm_can_be_created_from_the_rendered_fields(self):
        """The old template omitted background cost, maximum Quintessence and power."""
        response = self.client.post(
            reverse("items:mage:create:charm"),
            {
                "name": "Lucky coin",
                "rank": 1,
                "background_cost": 2,
                "quintessence_max": 5,
                "arete": 1,
                "description": "A coin",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Charm.objects.filter(name="Lucky coin").exists())

    def test_sorcerer_artifact_create_view_renders(self):
        """Its registry fields named power and background_cost, which the model lacks."""
        response = self.client.get(reverse("items:mage:create:sorcerer_artifact"))
        self.assert_native_form(response)
        response = self.client.post(
            reverse("items:mage:create:sorcerer_artifact"),
            {"name": "Bone flute", "rank": 2, "description": "Carved"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SorcererArtifact.objects.get(name="Bone flute").rank, 2)

    def test_update_forms_are_native(self):
        weapon = Weapon.objects.create(name="Sword", owner=self.admin)
        vessel = Vessel.objects.create(name="Canopic jar", owner=self.admin)
        artifact = VampireArtifact.objects.create(name="Chalice", owner=self.admin)
        for url in (
            reverse("items:update:weapon", kwargs={"pk": weapon.pk}),
            reverse("items:mummy:update:vessel", kwargs={"pk": vessel.pk}),
            reverse("items:vampire:update:artifact", kwargs={"pk": artifact.pk}),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assert_native_form(response)
        self.assertContains(
            self.client.get(reverse("items:mummy:update:vessel", kwargs={"pk": vessel.pk})),
            'name="current_ba"',
        )

    def test_field_errors_show_in_the_summary_and_the_field(self):
        response = self.client.post(reverse("items:create:weapon"), {"name": ""})
        self.assertContains(response, "tl-errsum")
        self.assertContains(response, "tl-field is-invalid")
        self.assertContains(response, "tl-field__error")
