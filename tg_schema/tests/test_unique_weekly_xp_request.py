"""tg_schema 0010 removes duplicate weekly XP requests and makes (week, character) unique."""

import importlib
from datetime import date
from unittest import mock

from django.db import IntegrityError, connection, transaction
from django.test import TransactionTestCase

from characters.models.core.human import Human
from game.models import Week, WeeklyXPRequest

migration = importlib.import_module("tg_schema.migrations.0010_unique_weekly_xp_request")

CONSTRAINT_SQL = ', CONSTRAINT "unique_weekly_xp_request" UNIQUE ("week_id", "character_id")'


def unique_week_character():
    with connection.cursor() as cursor:
        return migration.has_unique_week_character(connection, cursor)


class UniqueWeeklyXPRequestMigrationTests(TransactionTestCase):
    def setUp(self):
        self.ada = Human.objects.create(name="Ada")
        self.bo = Human.objects.create(name="Bo")
        self.week = Week.objects.create(end_date=date(2024, 1, 14))
        self.next_week = Week.objects.create(end_date=date(2024, 1, 21))

    def legacy_table(self):
        """Rebuild the table as older databases have it: no unique constraint. (Django's
        SQLite remove_constraint rebuilds from the model, which still declares it.)"""
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT type, sql FROM sqlite_master WHERE tbl_name = %s AND sql IS NOT NULL",
                [migration.TABLE],
            )
            rows = cursor.fetchall()
        table = next(sql for kind, sql in rows if kind == "table")
        indexes = [sql for kind, sql in rows if kind == "index"]
        legacy = table.replace(CONSTRAINT_SQL, "")
        self.assertNotEqual(legacy, table)
        self.rebuild(legacy, indexes)
        self.addCleanup(self.rebuild, table, indexes)
        # Cleanups run last-in first-out: empty the table before restoring the constraint.
        self.addCleanup(WeeklyXPRequest.objects.all().delete)
        self.assertFalse(unique_week_character())

    def rebuild(self, create_table, indexes):
        name = migration.TABLE
        with connection.cursor() as cursor:
            cursor.execute(f'DROP INDEX IF EXISTS "{migration.INDEX}"')
            cursor.execute(f'ALTER TABLE "{name}" RENAME TO "{name}__old"')
            cursor.execute(create_table)
            cursor.execute(f'INSERT INTO "{name}" SELECT * FROM "{name}__old"')
            cursor.execute(f'DROP TABLE "{name}__old"')
            for index in indexes:
                cursor.execute(index)

    def insert(self, week, character, approved=False):
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {migration.TABLE} (week_id, character_id, finishing, learning,"
                " rp, focus, standingout, approved) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                [week and week.pk, character and character.pk, True, False, False, False, False]
                + [approved],
            )
            return cursor.lastrowid

    def run_migration(self):
        with connection.schema_editor() as editor:
            migration.make_weekly_xp_request_unique(None, editor)

    def test_duplicates_keep_the_approved_then_oldest_row_then_the_pair_is_unique(self):
        self.legacy_table()
        self.insert(self.week, self.ada)
        approved = self.insert(self.week, self.ada, approved=True)
        self.insert(self.week, self.ada, approved=True)
        oldest = self.insert(self.week, self.bo)
        self.insert(self.week, self.bo)
        other_week = self.insert(self.next_week, self.ada)

        self.run_migration()

        self.assertEqual(
            sorted(WeeklyXPRequest.objects.values_list("pk", flat=True)),
            sorted([approved, oldest, other_week]),
        )
        self.assertTrue(unique_week_character())
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.insert(self.week, self.ada)

    def test_rows_without_a_week_or_character_are_kept(self):
        self.legacy_table()
        self.insert(None, self.ada)
        self.insert(None, self.ada)
        self.insert(self.week, None)
        self.run_migration()
        self.assertEqual(WeeklyXPRequest.objects.count(), 3)
        self.assertTrue(unique_week_character())

    def test_an_existing_unique_constraint_is_left_alone(self):
        self.assertTrue(unique_week_character())
        self.run_migration()
        with connection.cursor() as cursor:
            names = connection.introspection.get_constraints(cursor, migration.TABLE)
        self.assertEqual(
            sum(
                1
                for spec in names.values()
                if spec["unique"] and sorted(spec["columns"]) == ["character_id", "week_id"]
            ),
            1,
        )

    def test_a_second_run_changes_nothing(self):
        self.legacy_table()
        self.insert(self.week, self.ada)
        self.insert(self.week, self.ada)
        self.run_migration()
        rows = list(WeeklyXPRequest.objects.values_list("pk", flat=True))
        self.run_migration()
        self.assertEqual(list(WeeklyXPRequest.objects.values_list("pk", flat=True)), rows)

    def test_a_renamed_column_is_skipped(self):
        self.legacy_table()
        self.insert(self.week, self.ada)
        self.insert(self.week, self.ada)
        with mock.patch.object(migration, "COLUMNS", migration.COLUMNS | {"renamed_id"}):
            self.run_migration()
        self.assertEqual(WeeklyXPRequest.objects.count(), 2)
        self.assertFalse(unique_week_character())
