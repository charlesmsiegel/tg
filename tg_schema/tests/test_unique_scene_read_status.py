"""tg_schema 0008 merges duplicate scene read statuses and makes (user, scene) unique."""

import importlib
from unittest import mock

from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection, transaction
from django.test import TransactionTestCase

from characters.models.core.human import Human
from game.models import Chronicle, Post, Scene, UserSceneReadStatus

migration = importlib.import_module("tg_schema.migrations.0008_unique_scene_read_status")


def unique_user_scene():
    with connection.cursor() as cursor:
        return migration.has_unique_user_scene(connection, cursor)


class UniqueSceneReadStatusMigrationTests(TransactionTestCase):
    def setUp(self):
        users = get_user_model().objects
        self.ada, self.bo = users.create_user("ada"), users.create_user("bo")
        chronicle = Chronicle.objects.create(name="Ashes")
        self.scene = Scene.objects.create(name="Harbour", chronicle=chronicle)
        self.other_scene = Scene.objects.create(name="Tower", chronicle=chronicle)
        speaker = Human.objects.create(name="Speaker", chronicle=chronicle)
        self.first, self.second = (
            Post.objects.create(scene=self.scene, character=speaker, message=text)
            for text in ("First", "Second")
        )

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
        legacy = table.replace(
            ', CONSTRAINT "unique_user_scene_read_status" UNIQUE ("user_id", "scene_id")', ""
        )
        self.assertNotEqual(legacy, table)
        self.rebuild(legacy, indexes)
        self.addCleanup(self.rebuild, table, indexes)
        self.assertFalse(unique_user_scene())

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

    def insert(self, user, scene, read, marker=None):
        with connection.cursor() as cursor:
            cursor.execute(
                f'INSERT INTO {migration.TABLE} (user_id, scene_id, "read", last_read_post_id)'
                " VALUES (%s, %s, %s, %s)",
                [user and user.pk, scene and scene.pk, read, marker and marker.pk],
            )

    def run_migration(self):
        with connection.schema_editor() as editor:
            migration.make_scene_read_status_unique(None, editor)

    def test_duplicates_merge_into_one_row_then_the_pair_is_unique(self):
        self.legacy_table()
        self.insert(self.ada, self.scene, True, self.second)
        self.insert(self.ada, self.scene, False, self.first)
        self.insert(self.ada, self.scene, True, None)
        self.insert(self.bo, self.scene, True, self.first)
        self.insert(self.ada, self.other_scene, False, None)

        self.run_migration()

        ada = UserSceneReadStatus.objects.get(user=self.ada, scene=self.scene)
        self.assertEqual((ada.read, ada.last_read_post), (False, self.second))
        self.assertEqual(UserSceneReadStatus.objects.count(), 3)
        self.assertTrue(unique_user_scene())
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.insert(self.ada, self.scene, True)

    def test_rows_without_a_user_or_scene_are_deleted(self):
        self.legacy_table()
        self.insert(None, self.scene, False)
        self.insert(self.ada, None, False)
        self.insert(self.bo, self.scene, True)
        self.run_migration()
        self.assertEqual(
            list(UserSceneReadStatus.objects.values_list("user", "scene")),
            [(self.bo.pk, self.scene.pk)],
        )

    def test_an_existing_unique_constraint_is_left_alone(self):
        self.assertTrue(unique_user_scene())
        self.run_migration()
        with connection.cursor() as cursor:
            names = connection.introspection.get_constraints(cursor, migration.TABLE)
        self.assertEqual(
            sum(
                1
                for spec in names.values()
                if spec["unique"] and sorted(spec["columns"]) == ["scene_id", "user_id"]
            ),
            1,
        )

    def test_a_renamed_marker_column_is_skipped(self):
        with mock.patch.object(migration, "COLUMNS", migration.COLUMNS | {"renamed_id"}):
            UserSceneReadStatus.objects.create(user=self.ada, scene=None)
            self.run_migration()
        self.assertTrue(UserSceneReadStatus.objects.filter(scene=None).exists())

    def test_rows_go_with_their_user_and_scene(self):
        UserSceneReadStatus.objects.create(user=self.ada, scene=self.scene)
        UserSceneReadStatus.objects.create(user=self.bo, scene=self.other_scene)
        self.ada.delete()
        self.other_scene.delete()
        self.assertFalse(UserSceneReadStatus.objects.exists())
