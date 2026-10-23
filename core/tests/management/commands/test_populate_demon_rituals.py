"""Ritual seed scripts preserve field names, requirements and source citations."""

import ast
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase

from characters.models.demon.ritual import Ritual

ROOT = Path(settings.BASE_DIR) / "populate_db/demon"


def ritual_scripts():
    return sorted([*ROOT.glob("demon_rituals*.py"), ROOT / "demon_earthbound_rituals.py"])


class RitualSeedContractTests(SimpleTestCase):
    def test_assignments_use_model_fields_and_durable_lore_keys(self):
        fields = {field.name for field in Ritual._meta.get_fields()}
        for path in ritual_scripts():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            ritual_names = {
                node.targets[0].id
                for node in ast.walk(tree)
                if isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Subscript)
                and isinstance(node.value.value, ast.Call)
                and ast.unparse(node.value.value.func) == "Ritual.objects.get_or_create"
            }
            self.assertTrue(ritual_names, path.name)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Assign):
                    continue
                for target in node.targets:
                    if not (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id in ritual_names
                    ):
                        continue
                    with self.subTest(script=path.name, line=node.lineno):
                        self.assertIn(target.attr, fields)
                        if target.attr == "secondary_lore_requirements":
                            for requirement in node.value.elts:
                                self.assertEqual(
                                    {key.value for key in requirement.keys}, {"lore", "rating"}
                                )


class PopulateDemonRitualTests(TestCase):
    def load_scripts(self):
        # Imported seed instances must belong to this test's database transaction.
        with patch.dict(sys.modules):
            for name in list(sys.modules):
                if name.startswith("populate_db.demon"):
                    del sys.modules[name]
            for selection in ("00_books", "demon_rituals", "demon_earthbound_rituals"):
                call_command("populate_gamedata", only=selection, stdout=StringIO())

    def test_dpg_requirements_survive_reload_and_all_rituals_have_citations(self):
        self.load_scripts()
        expected = {
            "Hadrisel's Libation": (2, [("awakening", 1)]),
            "Siren's Song": (3, [("radiance", 2), ("humanity", 1)]),
            "Fiery Vision": (3, [("light", 2), ("radiance", 2), ("humanity", 1)]),
        }
        for name, (rating, secondary) in expected.items():
            with self.subTest(ritual=name):
                ritual = Ritual.objects.get(name=name)
                self.assertEqual(ritual.primary_lore_rating, rating)
                self.assertEqual(
                    ritual.secondary_lore_requirements,
                    [{"lore": lore, "rating": dots} for lore, dots in secondary],
                )
        self.assertEqual(
            Ritual.objects.filter(sources__book__name="Demon Players Guide").distinct().count(), 47
        )
        for ritual in Ritual.objects.all():
            with self.subTest(source=ritual.name):
                self.assertTrue(ritual.sources.exists())
                self.assertFalse(ritual.sources.filter(page=0).exists())
        libation = Ritual.objects.get(name="Hadrisel's Libation")
        self.assertEqual(
            set(libation.sources.values_list("book__name", "page")),
            {("Demon Players Guide", 187), ("Demon Players Guide", 188)},
        )
        identities = dict(Ritual.objects.values_list("name", "pk"))
        references = libation.sources.count()
        self.load_scripts()
        self.assertEqual(dict(Ritual.objects.values_list("name", "pk")), identities)
        self.assertEqual(libation.sources.count(), references)
