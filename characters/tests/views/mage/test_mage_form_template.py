"""The Mage create/edit forms (Spread): every field renders, in form_layout sections."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.core.specialty import Specialty
from characters.models.mage.companion import Companion
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.views.mage.form_layout import MAGE_LAYOUT, build_form_sections, section_fields


class MageFormTemplateTest(TestCase):
    def setUp(self):
        self.st = User.objects.create_superuser("st", "st@example.com", "pw")
        self.client.force_login(self.st)

    def edit(self, mage):
        return self.client.get(reverse("characters:mage:update:mage_full", kwargs={"pk": mage.pk}))

    def test_technocracy_labels_follow_the_affiliation(self):
        union = MageFaction.objects.create(name="Technocratic Union")
        mage = Mage.objects.create(name="Agent", owner=self.st, affiliation=union)
        response = self.edit(mage)
        self.assertContains(response, "Enlightenment")
        self.assertContains(response, "Primal Energy")
        self.assertTrue(response.context["technocratic"])

    def test_traditions_keep_the_default_labels(self):
        mage = Mage.objects.create(name="Hermetic", owner=self.st)
        response = self.edit(mage)
        self.assertContains(response, ">Arete<")
        self.assertNotContains(response, "Enlightenment")

    def test_ability_columns_show_specialties(self):
        mage = Mage.objects.create(name="Seer", owner=self.st, art=4)
        mage.specialties.add(Specialty.objects.create(name="Keen Eye", stat="art"))
        response = self.edit(mage)
        abilities = next(s for s in response.context["form_sections"] if s["title"] == "Abilities")
        talents = dict((heading, rows) for heading, rows in abilities["columns"])["Talents"]
        self.assertIn("Art (Keen Eye)", [label for _field, label in talents])
        self.assertContains(response, "Art (Keen Eye)")

    def test_create_page_renders_without_an_object(self):
        response = self.client.get(reverse("characters:mage:create:mage_full"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["technocratic"])

    def test_page_is_native_spread(self):
        response = self.edit(Mage.objects.create(name="Native", owner=self.st))
        self.assertNotContains(response, 'class="tl-content tl-legacy"')
        self.assertContains(response, 'id="form-section-01"')


class MageFamilyFormsRenderEveryFieldTest(TestCase):
    """The old templates left required fields (secondary abilities, all MtA Human
    abilities, faction years) or the whole Companion form unrendered, so a Storyteller's
    save could never validate. Every visible field now has an input on the page."""

    def setUp(self):
        self.st = User.objects.create_superuser("st", "st@example.com", "pw")
        self.client.force_login(self.st)

    def assert_every_field_rendered(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        html = response.content.decode()
        for name in form.fields:
            with self.subTest(field=name):
                self.assertIn(f'name="{form.add_prefix(name)}"', html)
        return response

    def test_character_edit_forms(self):
        cases = [
            ("mage_full", Mage.objects.create(name="M", owner=self.st)),
            ("mta_human_full", MtAHuman.objects.create(name="H", owner=self.st)),
            ("sorcerer_full", Sorcerer.objects.create(name="S", owner=self.st)),
            ("companion_full", Companion.objects.create(name="C", owner=self.st)),
        ]
        for route, obj in cases:
            with self.subTest(route=route):
                response = self.assert_every_field_rendered(
                    reverse(f"characters:mage:update:{route}", kwargs={"pk": obj.pk})
                )
                placed = {
                    f.name for s in response.context["form_sections"] for f in section_fields(s)
                }
                self.assertEqual(placed, set(response.context["form"].fields))

    def test_create_forms(self):
        for route in (
            "mage_full",
            "companion_full",
            "mage",
            "mta_human",
            "companion",
            "sorcerer",
            "effect",
            "resonance",
            "paradigm",
            "practice",
            "specialized_practice",
            "corrupted_practice",
            "tenet",
            "mage_faction",
            "sorcerer_fellowship",
            "rote",
            "path",
            "ritual",
            "sphere",
        ):
            with self.subTest(route=route):
                self.assert_every_field_rendered(reverse(f"characters:mage:create:{route}"))

    def test_limited_form_keeps_only_its_sections(self):
        mage = Mage.objects.create(name="Mine", owner=self.st)
        form = LimitedHumanEditForm(instance=mage)
        sections = build_form_sections(form, Mage, mage, MAGE_LAYOUT)
        self.assertEqual([s["title"] for s in sections], ["Identity", "Biography", "Story"])
        placed = {f.name for s in sections for f in section_fields(s)}
        self.assertEqual(placed, {n for n in form.fields if not form[n].is_hidden})

    def test_unplaced_fields_fall_into_other(self):
        mage = Mage.objects.create(name="Mine", owner=self.st)
        form = LimitedHumanEditForm(instance=mage)
        sections = build_form_sections(form, Mage, mage, (("Story", ("history",)),))
        self.assertEqual([s["title"] for s in sections], ["Story", "Other"])
        self.assertEqual([s["num"] for s in sections], ["01", "02"])
