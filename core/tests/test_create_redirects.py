"""The new-character pickers offer only seeded types that have a create route."""

import re
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.forms.core.character_creation import CharacterCreationForm
from core.create_redirects import character_type_has_route, resolve_object_type_url
from game.forms import ChronicleCharacterCreationForm
from game.models import Chronicle, Gameline, ObjectType, STRelationship

SEED = Path(settings.BASE_DIR) / "populate_db" / "objects.py"
CHARACTER_SEED = re.compile(r'name="(\w+)", type="char", gameline="(\w+)"')


def seed_character_types():
    for name, gameline in CHARACTER_SEED.findall(SEED.read_text()):
        ObjectType.objects.get_or_create(name=name, type="char", gameline=gameline)


def offered(form):
    return {
        (gameline, name)
        for gameline, choices in form.fields["char_type"].choices_map.items()
        for name, _label in choices
    }


class CharacterPickerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_character_types()
        cls.user = get_user_model().objects.create_user("picker_st")
        cls.chronicle = Chronicle.objects.create(name="Picker", head_st=cls.user)
        STRelationship.objects.create(
            user=cls.user, chronicle=cls.chronicle, gameline=Gameline.objects.create(name="Mage")
        )

    def forms(self):
        return (
            CharacterCreationForm(user=self.user),
            ChronicleCharacterCreationForm(chronicle=self.chronicle, user=self.user),
        )

    def test_every_offered_type_redirects_to_a_create_page(self):
        self.client.force_login(self.user)
        for form in self.forms():
            choices = offered(form)
            self.assertGreater(len(choices), 20)
            for gameline, name in sorted(choices):
                with self.subTest(form=type(form).__name__, type=name):
                    response = self.client.get(
                        reverse(
                            "core:object_type_redirect",
                            kwargs={"kind": "character", "action": "create"},
                        ),
                        {"char_type": name, "gameline": gameline},
                    )
                    self.assertEqual(response.status_code, 302)

    def test_types_without_a_create_route_are_not_offered(self):
        hidden = {("wta", "spirit_character"), ("wta", "bastet"), ("wta", "rokea")}
        for form in self.forms():
            with self.subTest(form=type(form).__name__):
                choices = offered(form)
                self.assertFalse(hidden & choices)
                self.assertIn(("wta", "fera"), choices)

    def test_mortals_with_unseparated_route_names_are_routed(self):
        expected = {
            ("dtf_human", "dtf"): "characters:demon:create:dtfhuman",
            ("htr_human", "htr"): "characters:hunter:create:htrhuman",
            ("mtr_human", "mtr"): "characters:mummy:create:mtrhuman",
        }
        for (name, gameline), route in expected.items():
            with self.subTest(type=name):
                self.assertTrue(character_type_has_route(name, gameline))
                self.assertEqual(resolve_object_type_url("char", name), reverse(route))
                for form in self.forms():
                    self.assertIn((gameline, name), offered(form))
