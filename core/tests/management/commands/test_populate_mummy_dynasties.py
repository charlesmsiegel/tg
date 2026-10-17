"""Dynasty reloads retain catalogue content, exports, and referenced identities."""

import importlib
import importlib.util
import json
import runpy
import shutil
import sys
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mummy import Mummy

SCRIPT = Path(settings.BASE_DIR) / "populate_db/mummy/dynasties.py"

EXPECTED = {
    "old_kingdom_1": {
        "name": "First Dynasty",
        "era": "Old Kingdom",
        "description": "The earliest unified Egyptian dynasty, beginning with "
        "Narmer/Menes. Amenti from this era remember the first "
        "unification of Upper and Lower Egypt.",
        "favored_hekau": "Nomenclature",
    },
    "old_kingdom_4": {
        "name": "Fourth Dynasty",
        "era": "Old Kingdom",
        "description": "The pyramid builders. Amenti from this golden age remember "
        "Khufu, Khafre, and the construction of the Great Pyramids "
        "at Giza.",
        "favored_hekau": "Effigy",
    },
    "middle_kingdom_11": {
        "name": "Eleventh Dynasty",
        "era": "Middle Kingdom",
        "description": "Reunification of Egypt after the First Intermediate "
        "Period. These Amenti remember bringing order from "
        "chaos.",
        "favored_hekau": "Judge",
    },
    "middle_kingdom_12": {
        "name": "Twelfth Dynasty",
        "era": "Middle Kingdom",
        "description": "The classical age of Egyptian literature and art. "
        "Amenti from this peaceful era are often scholars and "
        "diplomats.",
        "favored_hekau": "Celestial",
    },
    "new_kingdom_18": {
        "name": "Eighteenth Dynasty",
        "era": "New Kingdom",
        "description": "The dynasty of Hatshepsut, Akhenaten, Tutankhamun, and "
        "great imperial expansion. These Amenti remember Egypt at "
        "its zenith.",
        "favored_hekau": "Ushabti",
    },
    "new_kingdom_19": {
        "name": "Nineteenth Dynasty",
        "era": "New Kingdom",
        "description": "The Ramesside period, including Ramesses II the Great. "
        "Warriors and builders from an age of monumental "
        "construction.",
        "favored_hekau": "Phoenix",
    },
    "ptolemaic": {
        "name": "Ptolemaic Dynasty",
        "era": "Ptolemaic",
        "description": "Greek rulers of Egypt after Alexander. These Amenti bridge "
        "Egyptian and Hellenistic worlds, often multilingual and "
        "cosmopolitan.",
        "favored_hekau": "Alchemy",
    },
    "modern": {
        "name": "Modern Awakened",
        "era": "Modern",
        "description": "Amenti who first awakened in the modern era, or who have fully "
        "adapted to contemporary society across many incarnations.",
        "favored_hekau": "Necromancy",
    },
}


class PopulateMummyDynastyTests(TestCase):
    def test_wrapper_exports_original_objects_and_content(self):
        exports = runpy.run_path(str(SCRIPT))
        self.assertEqual(Dynasty.objects.count(), 8)
        for name, fields in EXPECTED.items():
            with self.subTest(export=name):
                dynasty = exports[name]
                self.assertEqual(dynasty.seed_key, f"mummy.dynasty.{name}")
                self.assertEqual({field: getattr(dynasty, field) for field in fields}, fields)

    def test_reload_updates_existing_dynasty_without_changing_identity(self):
        exports = runpy.run_path(str(SCRIPT))
        original = exports["old_kingdom_1"]
        Dynasty.objects.filter(pk=original.pk).update(description="Staff edit")
        reloaded = runpy.run_path(str(SCRIPT))["old_kingdom_1"]
        original.refresh_from_db()
        self.assertEqual(reloaded.pk, original.pk)
        self.assertEqual(original.description, EXPECTED["old_kingdom_1"]["description"])
        self.assertEqual(Dynasty.objects.count(), 8)

    def test_repeated_load_preserves_all_primary_keys(self):
        first = runpy.run_path(str(SCRIPT))
        second = runpy.run_path(str(SCRIPT))
        self.assertEqual(Dynasty.objects.count(), 8)
        self.assertEqual(
            {name: first[name].pk for name in EXPECTED},
            {name: second[name].pk for name in EXPECTED},
        )

    def test_legacy_adoption_preserves_character_reference(self):
        original = Dynasty.objects.create(name="First Dynasty", description="Legacy text")
        mummy = Mummy.objects.create(name="Legacy Mummy", dynasty=original)
        exported = runpy.run_path(str(SCRIPT))["old_kingdom_1"]
        original.refresh_from_db()
        mummy.refresh_from_db()
        self.assertEqual(exported.pk, original.pk)
        self.assertEqual(mummy.dynasty_id, original.pk)
        self.assertEqual(original.seed_key, "mummy.dynasty.old_kingdom_1")
        self.assertEqual(original.description, EXPECTED["old_kingdom_1"]["description"])

    def test_catalogue_description_edit_updates_same_primary_key(self):
        original = runpy.run_path(str(SCRIPT))["old_kingdom_1"]
        with TemporaryDirectory() as directory:
            script = Path(directory) / "dynasties.py"
            shutil.copyfile(SCRIPT, script)
            records = json.loads(SCRIPT.with_suffix(".json").read_text(encoding="utf-8"))
            records[0]["fields"]["description"] = "Corrected catalogue text"
            records[0]["fields"]["name"] = "Renamed First Dynasty"
            script.with_suffix(".json").write_text(json.dumps(records), encoding="utf-8")
            updated = runpy.run_path(str(script))["old_kingdom_1"]
        original.refresh_from_db()
        self.assertEqual(updated.pk, original.pk)
        self.assertEqual(original.name, "Renamed First Dynasty")
        self.assertEqual(original.description, "Corrected catalogue text")
        self.assertEqual(Dynasty.objects.count(), 8)

    def test_import_entry_point_exposes_dynasty_instances(self):
        name = "populate_db.mummy.dynasties"
        parent = importlib.import_module("populate_db.mummy")
        old_attribute = getattr(parent, "dynasties", None)
        try:
            with mock.patch.dict(sys.modules):
                sys.modules.pop(name, None)
                module = importlib.import_module(name)
                self.assertEqual(module.old_kingdom_1.seed_key, "mummy.dynasty.old_kingdom_1")
                self.assertEqual(
                    module.old_kingdom_1.pk, Dynasty.objects.get(name="First Dynasty").pk
                )
        finally:
            if old_attribute is None:
                if hasattr(parent, "dynasties"):
                    del parent.dynasties
            else:
                parent.dynasties = old_attribute

    def test_command_filters_discover_wrapper_once_and_not_data_or_helper(self):
        output = StringIO()
        call_command("populate_gamedata", gameline="mummy", only="dynasties", stdout=output)
        self.assertIn("Found 1 file(s)", output.getvalue())
        self.assertNotIn("dynasties.json", output.getvalue())
        self.assertNotIn("seed_data.py", output.getvalue())
        self.assertEqual(Dynasty.objects.count(), 8)
        self.assertEqual(Dynasty.objects.exclude(seed_key=None).count(), 8)

    def test_failed_direct_import_rolls_back_updates_and_adoption(self):
        original = Dynasty.objects.create(name="First Dynasty", description="Keep original")
        with TemporaryDirectory() as directory:
            script = Path(directory) / "dynasties.py"
            shutil.copyfile(SCRIPT, script)
            records = json.loads(SCRIPT.with_suffix(".json").read_text(encoding="utf-8"))
            records[0]["export"] = "old_kingdom_one"
            records[0]["fields"]["description"] = "Should roll back"
            script.with_suffix(".json").write_text(json.dumps(records), encoding="utf-8")
            spec = importlib.util.spec_from_file_location("isolated_mummy_dynasties", script)
            module = importlib.util.module_from_spec(spec)
            with self.assertRaises(KeyError):
                spec.loader.exec_module(module)
        original.refresh_from_db()
        self.assertEqual(original.description, "Keep original")
        self.assertIsNone(original.seed_key)
        self.assertEqual(Dynasty.objects.count(), 1)
