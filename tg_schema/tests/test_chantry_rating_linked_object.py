"""tg_schema 0002 adds ChantryBackgroundRating's linked-object columns exactly once."""

import importlib

from django.db import connection
from django.test import TransactionTestCase

from locations.models.mage.chantry import ChantryBackgroundRating

migration = importlib.import_module("tg_schema.migrations.0002_chantry_rating_linked_object")

LINKED_COLUMNS = {"linked_location_id", "linked_character_id"}


def rating_columns():
    with connection.cursor() as cursor:
        return {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, ChantryBackgroundRating._meta.db_table
            )
        }


class ChantryRatingLinkedObjectMigrationTests(TransactionTestCase):
    def fields(self):
        return [ChantryBackgroundRating._meta.get_field(name) for name in migration.LINKED_FIELDS]

    def restore_columns(self):
        missing = [field for field in self.fields() if field.column not in rating_columns()]
        with connection.schema_editor() as editor:
            for field in missing:
                editor.add_field(ChantryBackgroundRating, field)

    def test_adds_each_missing_column(self):
        self.addCleanup(self.restore_columns)
        for field in self.fields():
            with self.subTest(column=field.column):
                # SQLite rebuilds the table from the live model, so drop one
                # column at a time.
                with connection.schema_editor() as editor:
                    editor.remove_field(ChantryBackgroundRating, field)
                self.assertNotIn(field.column, rating_columns())

                with connection.schema_editor() as editor:
                    migration.add_chantry_rating_linked_object(None, editor)

                self.assertEqual(rating_columns() & LINKED_COLUMNS, LINKED_COLUMNS)

    def test_existing_columns_are_left_alone(self):
        self.assertEqual(rating_columns() & LINKED_COLUMNS, LINKED_COLUMNS)
        with connection.schema_editor(collect_sql=True) as editor:
            migration.add_chantry_rating_linked_object(None, editor)
            self.assertEqual(editor.collected_sql, [])
