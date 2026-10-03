"""Retired CUS visibility becomes PRI on every table that stores PermissionMixin data."""

import importlib
import importlib.util
from types import SimpleNamespace
from unittest import mock

from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import connection, connections
from django.db.utils import ConnectionHandler
from django.test import SimpleTestCase, TestCase

from characters.models.core.human import Human
from core.models import CharacterTemplate, Observer, PermissionMixin
from core.permissions import Permission, PermissionManager
from items.models.core import ItemModel
from locations.models.core import LocationModel
from tg_schema.schema import live_field, live_model

MIGRATION_NAME = "tg_schema.migrations.0011_retire_custom_visibility"


class RetireCustomVisibilityMigrationTests(SimpleTestCase):
    def setUp(self):
        self.assertIsNotNone(
            importlib.util.find_spec(MIGRATION_NAME), "Ship the guarded CUS backfill"
        )
        self.migration = importlib.import_module(MIGRATION_NAME)
        # Independent, in-memory legacy tables keep schema tests away from the shared
        # test database. The migration must use the supplied non-default connection.
        databases = ConnectionHandler(
            {
                "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
                "visibility_migration": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                },
            }
        )
        self.connection = databases["visibility_migration"]
        self.addCleanup(self.connection.close)
        # SQLite's introspection probes JSON support through transaction.atomic(),
        # which resolves its alias in Django's global connection handler.
        connections[self.connection.alias] = self.connection
        self.addCleanup(connections.__delitem__, self.connection.alias)

    def create_table(self, table, column="visibility"):
        q = self.connection.ops.quote_name
        with self.connection.cursor() as cursor:
            cursor.execute(f"CREATE TABLE {q(table)} (id INTEGER PRIMARY KEY, {q(column)} TEXT)")
            cursor.executemany(
                f"INSERT INTO {q(table)} ({q(column)}) VALUES (%s)",
                [(value,) for value in ("CUS", "PRI", "PUB", "CHR", None, "", "XYZ")],
            )

    def values(self, table, column="visibility"):
        q = self.connection.ops.quote_name
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT {q(column)} FROM {q(table)} ORDER BY id")
            return [row[0] for row in cursor.fetchall()]

    def run_migration(self):
        operation = self.migration.Migration.operations[0]
        operation.code(None, SimpleNamespace(connection=self.connection))

    def test_backfill_covers_every_concrete_permission_visibility_table(self):
        actual = {
            (model._meta.label, model._meta.db_table)
            for model in apps.get_models()
            if issubclass(model, PermissionMixin)
            and live_field(model, "visibility") in model._meta.local_fields
        }
        self.assertEqual(set(self.migration.VISIBILITY_TABLES), actual)
        self.assertEqual(len(self.migration.VISIBILITY_TABLES), len(actual))
        for _label, table in self.migration.VISIBILITY_TABLES:
            self.create_table(table)
        self.run_migration()
        for label, table in self.migration.VISIBILITY_TABLES:
            with self.subTest(model=label):
                self.assertEqual(self.values(table), ["PRI", "PRI", "PUB", "CHR", None, "", "XYZ"])

    def test_second_run_changes_nothing(self):
        table = "items_itemmodel"
        self.create_table(table)
        self.run_migration()
        first = self.values(table)
        self.run_migration()
        self.assertEqual(self.values(table), first)

    def test_missing_models_are_skipped(self):
        table = "items_itemmodel"
        self.create_table(table)
        with mock.patch.object(self.migration, "live_model", return_value=None):
            self.run_migration()
        self.assertEqual(self.values(table)[0], "CUS")

    def test_a_missing_field_is_skipped_without_blocking_other_tables(self):
        self.create_table("items_itemmodel")
        self.create_table("locations_locationmodel")
        target = live_model("items.ItemModel")
        with mock.patch.object(
            self.migration,
            "live_field",
            side_effect=lambda model, name: None if model is target else live_field(model, name),
        ):
            self.run_migration()
        self.assertEqual(self.values("items_itemmodel")[0], "CUS")
        self.assertEqual(self.values("locations_locationmodel")[0], "PRI")

    def test_missing_tables_are_skipped(self):
        self.create_table("items_itemmodel")
        self.run_migration()
        self.assertEqual(self.values("items_itemmodel")[0], "PRI")

    def test_missing_columns_are_skipped_without_blocking_other_tables(self):
        self.create_table("items_itemmodel", column="renamed_visibility")
        self.create_table("locations_locationmodel")
        self.run_migration()
        self.assertEqual(self.values("items_itemmodel", column="renamed_visibility")[0], "CUS")
        self.assertEqual(self.values("locations_locationmodel")[0], "PRI")

    def test_a_live_renamed_field_column_is_skipped(self):
        self.create_table("items_itemmodel")
        field = live_field(live_model("items.ItemModel"), "visibility")
        with mock.patch.object(field, "column", "renamed_visibility"):
            self.run_migration()
        self.assertEqual(self.values("items_itemmodel")[0], "CUS")

    def test_a_live_renamed_table_is_skipped(self):
        self.create_table("items_itemmodel")
        self.create_table("renamed_items")
        model = live_model("items.ItemModel")
        with mock.patch.object(model._meta, "db_table", "renamed_items"):
            self.run_migration()
        self.assertEqual(self.values("items_itemmodel")[0], "CUS")
        self.assertEqual(self.values("renamed_items")[0], "CUS")

    def test_a_field_moved_to_another_owning_table_is_skipped(self):
        self.create_table("items_itemmodel")
        model = live_model("items.ItemModel")
        field = live_field(model, "visibility")
        with mock.patch.object(
            model._meta,
            "local_fields",
            [local for local in model._meta.local_fields if local is not field],
        ):
            self.run_migration()
        self.assertEqual(self.values("items_itemmodel")[0], "CUS")

    def test_reverse_does_not_restore_custom_visibility(self):
        self.create_table("items_itemmodel")
        self.run_migration()
        self.migration.Migration.operations[0].reverse_code(
            None, SimpleNamespace(connection=self.connection)
        )
        self.assertEqual(self.values("items_itemmodel")[0], "PRI")

    def test_unrelated_visibility_columns_are_untouched(self):
        self.create_table("game_scene")
        self.run_migration()
        self.assertEqual(self.values("game_scene")[0], "CUS")


class MigratedCustomVisibilityModelTests(TestCase):
    def test_legacy_custom_objects_can_be_edited_after_backfill_without_losing_grants(self):
        migration = importlib.import_module(MIGRATION_NAME)
        owner = User.objects.create_user("legacy_visibility_owner")
        reader = User.objects.create_user("legacy_visibility_observer")
        objects = []
        for model, extra in (
            (Human, {}),
            (ItemModel, {}),
            (LocationModel, {}),
            (CharacterTemplate, {"character_type": "human"}),
        ):
            obj = model.objects.create(name=model.__name__, owner=owner, **extra)
            grant = Observer.objects.create(content_object=obj, user=reader, granted_by=owner)
            # Reproduce rows written when CUS was still a supported choice.
            model.objects.filter(pk=obj.pk).update(visibility="CUS")
            obj.refresh_from_db()
            with self.subTest(model=model.__name__, before_backfill=True):
                with self.assertRaises(ValidationError):
                    obj.save()
                self.assertTrue(
                    PermissionManager.user_has_permission(owner, obj, Permission.VIEW_FULL)
                )
            objects.append((obj, grant))

        migration.retire_custom_visibility(None, SimpleNamespace(connection=connection))

        for obj, grant in objects:
            with self.subTest(model=type(obj).__name__, after_backfill=True):
                obj.refresh_from_db()
                self.assertEqual(obj.visibility, "PRI")
                obj.name += " edited"
                obj.save()
                obj.refresh_from_db()
                self.assertTrue(obj.name.endswith(" edited"))
                self.assertTrue(
                    PermissionManager.user_has_permission(owner, obj, Permission.VIEW_FULL)
                )
                self.assertTrue(Observer.objects.filter(pk=grant.pk, user=reader).exists())
