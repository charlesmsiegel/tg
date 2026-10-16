"""Exercise the seed identity patch against real legacy-schema tables."""

import importlib
from unittest import mock

from django.db import IntegrityError, connection, models, transaction
from django.test import TransactionTestCase
from django.test.utils import isolate_apps


class MummyTitleSeedMigrationTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.patch = importlib.import_module("tg_schema.migrations.0013_mummy_title_seed_key")

    @isolate_apps()
    def setUp(self):
        class Title(models.Model):
            name = models.CharField(max_length=100, unique=True)
            seed_key = models.CharField(max_length=150, null=True, blank=True, editable=False)

            class Meta:
                app_label = "tg_schema"
                db_table = "seed_identity_migration_test"
                constraints = [
                    models.UniqueConstraint(fields=["seed_key"], name="test_unique_title_seed_key")
                ]

        self.model = Title
        self.lookup = mock.patch.object(self.patch, "live_model", return_value=Title)
        self.lookup.start()
        self.addCleanup(self.lookup.stop)
        self.addCleanup(self.drop_table)

    def drop_table(self):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS "seed_identity_migration_test"')

    def legacy_table(self, *, with_column=False):
        column = ", seed_key varchar(150) NULL" if with_column else ""
        with connection.cursor() as cursor:
            cursor.execute(
                'CREATE TABLE "seed_identity_migration_test" '
                f"(id integer PRIMARY KEY, name varchar(100) UNIQUE NOT NULL{column})"
            )
            cursor.execute(
                'INSERT INTO "seed_identity_migration_test" (id, name) VALUES (7, %s)',
                ["Pharaoh"],
            )

    def run_patch(self):
        with connection.schema_editor() as editor:
            self.patch.add_mummy_title_seed_key(None, editor)

    def assert_identity_contract(self):
        title = self.model.objects.get(pk=7)
        self.assertEqual(title.name, "Pharaoh")
        self.assertIsNone(title.seed_key)
        self.model.objects.create(name="Unseeded")
        self.model.objects.create(name="Seeded", seed_key="mummy.title.pharaoh")
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.model.objects.create(name="Duplicate", seed_key="mummy.title.pharaoh")

    def test_adds_missing_column_and_unique_identity_without_rewriting_rows(self):
        self.legacy_table()
        self.run_patch()
        self.run_patch()
        self.assert_identity_contract()

    def test_adds_constraint_when_column_already_exists(self):
        self.legacy_table(with_column=True)
        self.run_patch()
        self.assert_identity_contract()

    def test_existing_schema_has_no_ddl_on_repeat(self):
        with connection.schema_editor() as editor:
            editor.create_model(self.model)
        with connection.schema_editor(collect_sql=True) as editor:
            self.patch.add_mummy_title_seed_key(None, editor)
            self.assertEqual(editor.collected_sql, [])

    def test_missing_model_field_or_table_is_skipped(self):
        self.run_patch()  # No table.
        with mock.patch.object(self.patch, "live_model", return_value=None):
            self.run_patch()
        self.legacy_table()
        with mock.patch.object(self.patch, "live_field", return_value=None):
            self.run_patch()
        with connection.cursor() as cursor:
            columns = connection.introspection.get_table_description(
                cursor, self.model._meta.db_table
            )
        self.assertNotIn("seed_key", [column.name for column in columns])

    def test_later_model_constraint_removal_does_not_break_historical_patch(self):
        self.legacy_table(with_column=True)
        with mock.patch.object(self.model._meta, "constraints", []):
            self.run_patch()
        self.assert_identity_contract()
