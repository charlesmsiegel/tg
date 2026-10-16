"""Structured input rejects ambiguous instructions before touching the database."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

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
                with self.assertRaisesRegex(seed_data.SeedDataError, str(self.path)):
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
                with self.assertRaisesRegex(seed_data.SeedDataError, str(self.path)):
                    self.read(fields=fields, legacy=legacy)
        with self.assertRaises(seed_data.SeedDataError):
            self.read(model=Mummy, fields=frozenset({"titles"}))

    def test_duplicate_json_properties_are_not_silently_overwritten(self):
        raw = json.dumps([RECORD]).replace('"name": "Pharaoh"', '"name":"Other", "name":"Pharaoh"')
        self.path.write_text(raw, encoding="utf-8")
        with self.assertRaisesRegex(seed_data.SeedDataError, "duplicate"):
            self.read()

    def test_missing_and_malformed_files_report_the_path(self):
        with self.assertRaisesRegex(seed_data.SeedDataError, str(self.path)):
            self.read()
        for text in ["[broken", "\ud800"]:
            self.path.write_bytes(text.encode("utf-8", errors="surrogatepass"))
            with self.assertRaisesRegex(seed_data.SeedDataError, str(self.path)):
                self.read()
