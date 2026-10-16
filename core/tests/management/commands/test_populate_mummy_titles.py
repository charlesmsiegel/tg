"""The structured pilot preserves the existing twelve titles and script entry point."""

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

from characters.models.mummy.mummy_title import MummyTitle
from core.management.commands.populate_gamedata import Command

SCRIPT = Path(settings.BASE_DIR) / "populate_db/mummy/titles.py"

EXPECTED = {
    "pharaoh": {
        "name": "Pharaoh",
        "rank_level": 10,
        "description": "Supreme leader of an Amenti community. Rare and powerful.",
    },
    "high_priest": {
        "name": "High Priest/Priestess",
        "rank_level": 8,
        "description": "Religious leader and keeper of ancient rites.",
    },
    "vizier": {
        "name": "Vizier",
        "rank_level": 7,
        "description": "Chief administrator and advisor to higher-ranking Amenti.",
    },
    "keeper_of_balance": {
        "name": "Keeper of Balance",
        "rank_level": 6,
        "description": "Guardian of Ma'at and cosmic order. Associated with the Web " "of Ma'at.",
    },
    "judge_of_souls": {
        "name": "Judge of Souls",
        "rank_level": 6,
        "description": "Weighs hearts and pronounces judgment. Associated with the Web "
        "of Osiris.",
    },
    "guardian": {
        "name": "Guardian",
        "rank_level": 5,
        "description": "Protector of sacred places and fellow Amenti. Associated with the "
        "Web of Horus.",
    },
    "preserver": {
        "name": "Preserver",
        "rank_level": 5,
        "description": "Keeper of knowledge and sacred objects. Associated with the Web of "
        "Isis.",
    },
    "lorekeeper": {
        "name": "Lorekeeper",
        "rank_level": 5,
        "description": "Scholar and keeper of wisdom. Associated with the Web of Thoth.",
    },
    "elder": {
        "name": "Elder",
        "rank_level": 4,
        "description": "Respected Amenti with many incarnations and much experience.",
    },
    "mentor": {
        "name": "Mentor",
        "rank_level": 3,
        "description": "Teacher of newly awakened Amenti.",
    },
    "seeker": {
        "name": "Seeker",
        "rank_level": 2,
        "description": "Amenti on a quest for knowledge or redemption.",
    },
    "neophyte": {
        "name": "Neophyte",
        "rank_level": 1,
        "description": "Newly awakened Amenti, still learning their purpose.",
    },
}


class PopulateMummyTitleTests(TestCase):
    def test_wrapper_exports_original_objects_and_content(self):
        exports = runpy.run_path(str(SCRIPT))
        self.assertEqual(MummyTitle.objects.count(), 12)
        for name, fields in EXPECTED.items():
            with self.subTest(export=name):
                title = exports[name]
                self.assertEqual(title.seed_key, f"mummy.title.{name}")
                self.assertEqual({field: getattr(title, field) for field in fields}, fields)

    def test_reload_updates_existing_title_without_changing_identity(self):
        command = Command(stdout=StringIO())
        command.load_file(SCRIPT, SCRIPT.parents[1])
        original = MummyTitle.objects.get(name="Pharaoh")
        MummyTitle.objects.filter(pk=original.pk).update(description="Staff edit", rank_level=1)
        command.load_file(SCRIPT, SCRIPT.parents[1])
        original.refresh_from_db()
        self.assertEqual(original.description, EXPECTED["pharaoh"]["description"])
        self.assertEqual(original.rank_level, 10)
        self.assertEqual(MummyTitle.objects.count(), 12)

    def test_import_entry_point_exposes_title_instances(self):
        name = "populate_db.mummy.titles"
        parent = importlib.import_module("populate_db.mummy")
        old_attribute = getattr(parent, "titles", None)
        try:
            with mock.patch.dict(sys.modules):
                sys.modules.pop(name, None)
                module = importlib.import_module(name)
                self.assertEqual(module.pharaoh.seed_key, "mummy.title.pharaoh")
                self.assertEqual(module.pharaoh.pk, MummyTitle.objects.get(name="Pharaoh").pk)
        finally:
            if old_attribute is None:
                if hasattr(parent, "titles"):
                    del parent.titles
            else:
                parent.titles = old_attribute

    def test_command_filters_discover_wrapper_once_and_not_data_or_helper(self):
        output = StringIO()
        call_command("populate_gamedata", gameline="mummy", only="titles", stdout=output)
        self.assertIn("Found 1 file(s)", output.getvalue())
        self.assertNotIn("titles.json", output.getvalue())
        self.assertNotIn("seed_data.py", output.getvalue())
        self.assertEqual(MummyTitle.objects.count(), 12)
        self.assertEqual(MummyTitle.objects.exclude(seed_key=None).count(), 12)

    def test_failed_direct_import_rolls_back_updates_and_adoption(self):
        original = MummyTitle.objects.create(name="Pharaoh", description="Keep original")
        with TemporaryDirectory() as directory:
            script = Path(directory) / "titles.py"
            shutil.copyfile(SCRIPT, script)
            records = json.loads(SCRIPT.with_suffix(".json").read_text(encoding="utf-8"))
            records[0]["export"] = "pharoah"
            records[0]["fields"]["description"] = "Should roll back"
            script.with_suffix(".json").write_text(json.dumps(records), encoding="utf-8")
            spec = importlib.util.spec_from_file_location("isolated_mummy_titles", script)
            module = importlib.util.module_from_spec(spec)
            with self.assertRaises(KeyError):
                spec.loader.exec_module(module)
        original.refresh_from_db()
        self.assertEqual(original.description, "Keep original")
        self.assertIsNone(original.seed_key)
        self.assertEqual(MummyTitle.objects.count(), 1)
