"""tg_schema 0005 adds Story.chronicle exactly once, leaving existing stories unassigned."""

import importlib

from django.db import connection
from django.test import TransactionTestCase

from game.models import Story

migration = importlib.import_module("tg_schema.migrations.0005_story_chronicle")


def story_columns():
    with connection.cursor() as cursor:
        return {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, Story._meta.db_table
            )
        }


class StoryChronicleMigrationTests(TransactionTestCase):
    def field(self):
        return Story._meta.get_field("chronicle")

    def restore_column(self):
        if self.field().column not in story_columns():
            with connection.schema_editor() as editor:
                editor.add_field(Story, self.field())

    def test_adds_the_missing_column_and_keeps_stories(self):
        self.addCleanup(self.restore_column)
        with connection.schema_editor() as editor:
            editor.remove_field(Story, self.field())
        self.assertNotIn("chronicle_id", story_columns())
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {Story._meta.db_table} (name, xp_given) VALUES (%s, %s)",
                ["Legacy", False],
            )

        with connection.schema_editor() as editor:
            migration.add_story_chronicle(None, editor)

        self.assertIn("chronicle_id", story_columns())
        legacy = Story.objects.get(name="Legacy")
        self.assertIsNone(legacy.chronicle)

    def test_existing_column_is_left_alone(self):
        self.assertIn("chronicle_id", story_columns())
        with connection.schema_editor(collect_sql=True) as editor:
            migration.add_story_chronicle(None, editor)
            self.assertEqual(editor.collected_sql, [])
