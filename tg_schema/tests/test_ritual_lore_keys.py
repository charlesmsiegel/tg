"""Legacy ritual JSON is upgraded without losing requirements."""

import importlib
from types import SimpleNamespace
from unittest.mock import patch

from django.db import connection
from django.test import TestCase

from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual


class RitualLoreKeyMigrationTests(TestCase):
    def setUp(self):
        self.migration = importlib.import_module("tg_schema.migrations.0015_ritual_lore_keys")
        self.lore = Lore.objects.create(name="Flame", property_name="flame")
        self.ritual = Ritual.objects.create(name="Legacy ritual")

    def run_migration(self):
        self.migration.convert_ritual_lore_keys(None, SimpleNamespace(connection=connection))

    def test_converts_mixed_requirements_without_changing_new_entries(self):
        old = [{"lore_id": self.lore.pk, "rating": 2}, {"lore": "flame", "rating": 1}]
        Ritual.objects.filter(pk=self.ritual.pk).update(secondary_lore_requirements=old)
        self.run_migration()
        self.ritual.refresh_from_db()
        self.assertEqual(
            self.ritual.secondary_lore_requirements,
            [{"lore": "flame", "rating": 2}, {"lore": "flame", "rating": 1}],
        )
        with self.assertNumQueries(0):
            with patch.object(self.migration, "table_names", return_value=set()):
                self.run_migration()
        self.run_migration()
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.secondary_lore_requirements[0], {"lore": "flame", "rating": 2})

    def test_unresolvable_requirements_are_retained_and_warned_about(self):
        old = [{"lore_id": 999999, "rating": 3}]
        Ritual.objects.filter(pk=self.ritual.pk).update(secondary_lore_requirements=old)
        with self.assertLogs(self.migration.__name__, level="WARNING") as logs:
            self.run_migration()
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.secondary_lore_requirements, old)
        self.assertIn(str(self.ritual.pk), logs.output[0])

    def test_removed_models_fields_tables_or_columns_skip_safely(self):
        for guard, result in (
            ("live_model", None),
            ("live_field", None),
            ("table_names", set()),
            ("table_columns", set()),
        ):
            with (
                self.subTest(guard=guard),
                patch.object(self.migration, guard, return_value=result),
            ):
                self.run_migration()
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.secondary_lore_requirements, [])
