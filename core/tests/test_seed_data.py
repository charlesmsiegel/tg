"""Structured input rejects ambiguous instructions before touching the database."""

import copy
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.test import SimpleTestCase, TestCase

from characters.models.mummy.mummy import Mummy
from characters.models.mummy.mummy_title import MummyTitle
from core import seed_data

FIELDS = frozenset({"name", "rank_level", "description"})
LEGACY = frozenset({"name"})
RECORD = {
    "key": "mummy.title.pharaoh",
    "export": "pharaoh",
    "legacy_lookup": {"name": "Pharaoh"},
    "fields": {"name": "Pharaoh", "rank_level": 10, "description": "Supreme leader."},
}


class SeedInputTests(SimpleTestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "titles.json"

    def write(self, records):
        self.path.write_text(json.dumps(records), encoding="utf-8")

    def read(self, model=MummyTitle, **options):
        return seed_data.read_seed_records(
            model,
            self.path,
            allowed_fields=options.get("fields", FIELDS),
            legacy_fields=options.get("legacy", LEGACY),
        )

    def test_reads_valid_records_without_database_access(self):
        self.write([RECORD])
        self.assertEqual(self.read(), [RECORD])

    def test_rejects_malformed_record_contracts(self):
        cases = [None, {}, [None], [[]], [dict(RECORD, extra=True)]]
        for missing in RECORD:
            cases.append([{key: value for key, value in RECORD.items() if key != missing}])
        for key in [None, [], "", "Upper.title", "a", "mummy..title", "a." + "x" * 150]:
            cases.append([dict(RECORD, key=key)])
        for export in [None, [], "", "two words", "class"]:
            cases.append([dict(RECORD, export=export)])
        for lookup in [None, [], {}, {"name__contains": "Ph"}, {"id": 1}, {"seed_key": "x"}]:
            cases.append([dict(RECORD, legacy_lookup=lookup)])
        for fields in [
            None,
            [],
            {},
            dict(RECORD["fields"], id=1),
            dict(RECORD["fields"], seed_key="other.key"),
        ]:
            cases.append([dict(RECORD, fields=fields)])
        cases.extend(
            [
                [RECORD, dict(RECORD, export="different")],
                [RECORD, dict(RECORD, key="mummy.title.other")],
            ]
        )
        for records in cases:
            with self.subTest(records=records):
                self.write(records)
                with self.assertRaisesRegex(seed_data.SeedDataError, re.escape(str(self.path))):
                    self.read()

    def test_rejects_unsafe_configuration(self):
        self.write([RECORD])
        for fields, legacy in [
            (FIELDS | {"id"}, LEGACY),
            (FIELDS, {"seed_key"}),
            (FIELDS | {"unknown"}, LEGACY),
            (set(), LEGACY),
        ]:
            with self.subTest(fields=fields, legacy=legacy):
                with self.assertRaisesRegex(seed_data.SeedDataError, re.escape(str(self.path))):
                    self.read(fields=fields, legacy=legacy)
        with self.assertRaises(seed_data.SeedDataError):
            self.read(model=Mummy, fields=frozenset({"titles"}))

    def test_duplicate_json_properties_are_not_silently_overwritten(self):
        raw = json.dumps([RECORD]).replace('"name": "Pharaoh"', '"name":"Other", "name":"Pharaoh"')
        self.path.write_text(raw, encoding="utf-8")
        with self.assertRaisesRegex(seed_data.SeedDataError, "duplicate"):
            self.read()

    def test_missing_and_malformed_files_report_the_path(self):
        with self.assertRaisesRegex(seed_data.SeedDataError, re.escape(str(self.path))):
            self.read()
        for text in ["[broken", "\ud800"]:
            self.path.write_bytes(text.encode("utf-8", errors="surrogatepass"))
            with self.assertRaisesRegex(seed_data.SeedDataError, re.escape(str(self.path))):
                self.read()


class SeedLoadTests(TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "titles.json"
        self.records = [copy.deepcopy(RECORD)]

    def load(self, *, fields=FIELDS, legacy=LEGACY):
        self.path.write_text(json.dumps(self.records), encoding="utf-8")
        return seed_data.load_seed_records(
            MummyTitle, self.path, allowed_fields=fields, legacy_fields=legacy
        )

    def test_fresh_and_repeated_load_keep_identity(self):
        first = self.load()["pharaoh"]
        second = self.load()["pharaoh"]
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(MummyTitle.objects.count(), 1)
        self.assertEqual(second.seed_key, RECORD["key"])
        self.assertEqual(second.description, RECORD["fields"]["description"])

    def test_adopts_existing_row_and_preserves_character_relation(self):
        original = MummyTitle.objects.create(name="Pharaoh", rank_level=1, description="Old")
        mummy = Mummy.objects.create(name="Amenti")
        mummy.titles.add(original)
        title = self.load()["pharaoh"]
        self.assertEqual(title.pk, original.pk)
        self.assertEqual(title.rank_level, 10)
        self.assertEqual(title.description, "Supreme leader.")
        self.records[0]["fields"].update(name="New Pharaoh", rank_level=9, description="Updated")
        renamed = self.load()["pharaoh"]
        self.assertEqual(renamed.pk, original.pk)
        self.assertEqual(mummy.titles.get().name, "New Pharaoh")
        self.assertEqual(renamed.description, "Updated")
        self.assertEqual(renamed.rank_level, 9)

    def test_unmanaged_fields_and_removed_records_are_retained(self):
        title = self.load()["pharaoh"]
        self.records[0]["fields"] = {"name": "Updated name"}
        self.load(fields=frozenset({"name"}))
        title.refresh_from_db()
        self.assertEqual(title.rank_level, 10)
        self.assertEqual(title.description, "Supreme leader.")
        self.records = []
        self.assertEqual(self.load(), {})
        self.assertTrue(MummyTitle.objects.filter(pk=title.pk).exists())

    def test_rejects_legacy_row_with_another_key(self):
        title = MummyTitle.objects.create(name="Pharaoh", seed_key="mummy.title.other")
        with self.assertRaisesRegex(seed_data.SeedDataError, "mummy.title.pharaoh.*Pharaoh"):
            self.load()
        title.refresh_from_db()
        self.assertEqual(title.seed_key, "mummy.title.other")

    def test_rejects_ambiguous_legacy_selector(self):
        MummyTitle.objects.create(name="First", rank_level=10)
        MummyTitle.objects.create(name="Second", rank_level=10)
        self.records[0]["legacy_lookup"] = {"rank_level": 10}
        with self.assertRaisesRegex(seed_data.SeedDataError, "mummy.title.pharaoh.*rank_level"):
            self.load(legacy=frozenset({"rank_level"}))
        self.assertEqual(MummyTitle.objects.filter(seed_key=None).count(), 2)

    def test_late_failure_rolls_back_adoption_and_updates(self):
        first = MummyTitle.objects.create(name="Pharaoh", description="Old")
        MummyTitle.objects.create(name="Conflict")
        second = copy.deepcopy(RECORD)
        second.update(key="mummy.title.second", export="second", legacy_lookup={"name": "Absent"})
        second["fields"]["name"] = "Conflict"
        self.records.append(second)
        with self.assertRaises(ValidationError):
            self.load()
        first.refresh_from_db()
        self.assertIsNone(first.seed_key)
        self.assertEqual(first.description, "Old")
        self.assertEqual(MummyTitle.objects.count(), 2)

    def test_keyed_rename_collision_does_not_adopt_the_other_row(self):
        title = self.load()["pharaoh"]
        other = MummyTitle.objects.create(name="Other", description="Keep")
        self.records[0]["fields"]["name"] = other.name
        with self.assertRaises(ValidationError):
            self.load()
        title.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(title.name, "Pharaoh")
        self.assertEqual(other.description, "Keep")
        self.assertIsNone(other.seed_key)

    def test_invalid_model_values_roll_back(self):
        self.records[0]["fields"]["rank_level"] = "not a number"
        with self.assertRaises(ValidationError):
            self.load()
        self.assertFalse(MummyTitle.objects.exists())

    def test_unexpected_database_errors_propagate(self):
        with mock.patch.object(MummyTitle, "save", side_effect=DatabaseError("unavailable")):
            with self.assertRaisesRegex(DatabaseError, "unavailable"):
                self.load()
        self.assertFalse(MummyTitle.objects.exists())
