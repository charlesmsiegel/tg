"""Tests for character_edit_sections and the Spread character edit forms that use it."""

from django.contrib.auth.models import User
from django.forms import modelform_factory
from django.test import TestCase
from django.urls import reverse

from characters.forms.core.crud_fields import VAMPIRE_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.demon.demon import Demon
from characters.models.vampire.vampire import Vampire
from characters.models.wraith.guild import Guild
from characters.models.wraith.wraith import Wraith
from characters.templatetags.character_edit import character_edit_sections


def section_fields(edit):
    names = [field.name for field in edit["hidden"]]
    for section in edit["sections"]:
        if section["kind"] == "columns":
            names += [field.name for _, fields in section["columns"] for field in fields]
        else:
            names += [field.name for field in section["fields"]]
    return names


class TestCharacterEditSections(TestCase):
    def test_full_form_renders_every_field_once(self):
        form = modelform_factory(Vampire, fields=VAMPIRE_UPDATE_FIELDS)(instance=Vampire())
        names = section_fields(character_edit_sections(form))
        self.assertCountEqual(names, list(form.fields))

    def test_attributes_and_abilities_get_their_own_columns(self):
        fields = ["name", "strength", "charisma", "wits", "alertness", "crafts", "occult", "faith"]
        form = modelform_factory(Demon, fields=fields)(instance=Demon())
        sections = {s["title"]: s for s in character_edit_sections(form)["sections"]}
        self.assertEqual(list(sections), ["Identity", "Attributes", "Abilities", "Traits"])
        self.assertEqual(
            [title for title, _ in sections["Attributes"]["columns"]],
            ["Physical", "Social", "Mental"],
        )
        abilities = {t: [f.name for f in fs] for t, fs in sections["Abilities"]["columns"]}
        self.assertEqual(abilities["Knowledges"], ["occult"])
        self.assertEqual([f.name for _, fs in sections["Traits"]["columns"] for f in fs], ["faith"])
        self.assertEqual([s["num"] for s in sections.values()], ["01", "02", "03", "04"])

    def test_limited_owner_form_keeps_every_field(self):
        form = LimitedHumanEditForm(instance=Vampire())
        edit = character_edit_sections(form)
        self.assertCountEqual(section_fields(edit), list(form.fields))
        self.assertEqual([s["title"] for s in edit["sections"]], ["Identity", "Details"])


class TestWraithFullEditForm(TestCase):
    """characters/wraith/wraith/form.html was never written; the edit page returned a 500."""

    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password")
        self.guild = Guild.objects.create(name="Harbingers")
        self.wraith = Wraith.objects.create(name="Test Wraith", owner=self.admin, guild=self.guild)
        self.url = reverse("characters:wraith:update:wraith_full", kwargs={"pk": self.wraith.pk})
        self.client.force_login(self.admin)

    def test_renders_every_field_natively(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/wraith/wraith/form.html")
        self.assertNotContains(response, "tl-content tl-legacy")  # outside the legacy wrapper
        for name in response.context["form"].fields:
            self.assertContains(response, f'name="{name}"')

    def test_round_trip_saves(self):
        form = self.client.get(self.url).context["form"]
        data = {
            name: value
            for name, value in ((n, form[n].value()) for n in form.fields)
            if value is not None and name != "image"
        }
        data.update(name="Renamed Wraith", death_description="Drowned.")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.wraith.refresh_from_db()
        self.assertEqual(self.wraith.name, "Renamed Wraith")
        self.assertEqual(self.wraith.death_description, "Drowned.")
