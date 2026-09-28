"""tg_schema 0004 adds Post.roll and the scene read marker exactly once, with a backfill."""

import importlib

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TransactionTestCase

from characters.models.core.human import Human
from game.models import Post, Scene, UserSceneReadStatus

migration = importlib.import_module("tg_schema.migrations.0004_scene_rolls_and_read_marker")


def columns(model):
    with connection.cursor() as cursor:
        return {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, model._meta.db_table
            )
        }


class SceneRollsAndReadMarkerMigrationTests(TransactionTestCase):
    def fields(self):
        return [(model, model._meta.get_field(name)) for model, name in migration.NEW_FIELDS]

    def restore_columns(self):
        with connection.schema_editor() as editor:
            for model, field in self.fields():
                if field.column not in columns(model):
                    editor.add_field(model, field)

    def drop(self, model, field):
        # SQLite rebuilds the table from the live model, so drop one column at a time.
        with connection.schema_editor() as editor:
            editor.remove_field(model, field)
        self.assertNotIn(field.column, columns(model))

    def migrate(self):
        with connection.schema_editor() as editor:
            migration.add_scene_rolls_and_read_marker(None, editor)

    def test_adds_each_missing_column(self):
        self.addCleanup(self.restore_columns)
        for model, field in self.fields():
            with self.subTest(column=field.column):
                self.drop(model, field)
                self.migrate()
                self.assertIn(field.column, columns(model))

    def test_existing_columns_are_left_alone(self):
        for model, field in self.fields():
            self.assertIn(field.column, columns(model))
        with connection.schema_editor(collect_sql=True) as editor:
            migration.add_scene_rolls_and_read_marker(None, editor)
            self.assertEqual(editor.collected_sql, [])

    def test_new_marker_column_is_backfilled(self):
        self.addCleanup(self.restore_columns)
        users = get_user_model().objects
        writer, reader, lurker = (users.create_user(name) for name in ("w", "r", "l"))
        scene = Scene.objects.create(name="Legacy")
        mine = Human.objects.create(name="Mine", owner=writer)
        theirs = Human.objects.create(name="Theirs", owner=reader)
        own_post = Post.objects.create(scene=scene, character=mine, message="Mine")
        Post.objects.create(scene=scene, character=theirs, message="Theirs")
        latest = Post.objects.create(scene=scene, character=theirs, message="Latest")
        UserSceneReadStatus.objects.create(user=writer, scene=scene, read=False)
        UserSceneReadStatus.objects.create(user=reader, scene=scene, read=True)
        UserSceneReadStatus.objects.create(user=lurker, scene=scene, read=False)

        self.drop(UserSceneReadStatus, UserSceneReadStatus._meta.get_field("last_read_post"))
        self.migrate()

        markers = dict(
            UserSceneReadStatus.objects.values_list("user__username", "last_read_post_id")
        )
        # Unread: read through their own latest post. Read: through the latest post.
        self.assertEqual(markers, {"w": own_post.pk, "r": latest.pk, "l": None})
