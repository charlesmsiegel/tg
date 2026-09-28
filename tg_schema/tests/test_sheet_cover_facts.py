"""tg_schema 0006 adds the Garou deed-name column exactly once."""

import importlib

from django.db import connection
from django.test import TransactionTestCase

migration = importlib.import_module("tg_schema.migrations.0006_sheet_cover_facts")


def table_columns(model):
    with connection.cursor() as cursor:
        return {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, model._meta.db_table
            )
        }


class SheetCoverFactsMigrationTests(TransactionTestCase):
    def fields(self):
        return [
            (model, model._meta.get_field(name))
            for model, names in migration.SHEET_FIELDS
            for name in names
        ]

    def restore_columns(self):
        for model, field in self.fields():
            if field.column not in table_columns(model):
                with connection.schema_editor() as editor:
                    editor.add_field(model, field)

    def test_adds_each_missing_column(self):
        self.addCleanup(self.restore_columns)
        for model, field in self.fields():
            with self.subTest(table=model._meta.db_table, column=field.column):
                # SQLite rebuilds the table from the live model, so drop one
                # column at a time.
                with connection.schema_editor() as editor:
                    editor.remove_field(model, field)
                self.assertNotIn(field.column, table_columns(model))

                with connection.schema_editor() as editor:
                    migration.add_sheet_cover_facts(None, editor)

                self.assertIn(field.column, table_columns(model))

    def test_existing_columns_are_left_alone(self):
        for model, field in self.fields():
            self.assertIn(field.column, table_columns(model))
        with connection.schema_editor(collect_sql=True) as editor:
            migration.add_sheet_cover_facts(None, editor)
            self.assertEqual(editor.collected_sql, [])
