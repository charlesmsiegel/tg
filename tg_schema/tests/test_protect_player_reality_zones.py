"""tg_schema 0012 classifies linked zones without changing independent names."""

import importlib
from types import SimpleNamespace
from unittest import mock

from django.db import connection
from django.test import TestCase, TransactionTestCase

from locations.models.mage.reality_zone import RealityZone
from locations.registry import registry
from tg_schema.schema import table_columns

migration = importlib.import_module("tg_schema.migrations.0012_protect_player_reality_zones")


class ProtectPlayerRealityZonesTests(TestCase):
    def run_migration(self):
        migration.protect_player_reality_zones(None, SimpleNamespace(connection=connection))

    def test_backfills_every_link_type_and_preserves_independent_staff_names(self):
        standalone = RealityZone.objects.create(name="Staff standalone", description="Public")
        linked = []
        for entry in registry:
            if any(field.name == "reality_zone" for field in entry.model._meta.fields):
                zone = RealityZone.objects.create(name=f"Staff's {entry.slug} zone")
                entry.model.objects.create(name=entry.slug, reality_zone=zone)
                linked.append(zone)
        # Simulate the new column's default on databases with pre-existing links.
        RealityZone.objects.filter(pk__in=[zone.pk for zone in linked]).update(is_player_zone=False)
        self.run_migration()
        for zone in linked:
            original_name = zone.name
            zone.refresh_from_db()
            self.assertTrue(zone.is_player_zone)
            self.assertEqual(zone.name, original_name)
        standalone.refresh_from_db()
        self.assertFalse(standalone.is_player_zone)

    def test_rerun_never_declassifies_an_orphan(self):
        orphan = RealityZone.objects.create(name="Old private zone", is_player_zone=True)
        self.run_migration()
        self.run_migration()
        orphan.refresh_from_db()
        self.assertTrue(orphan.is_player_zone)

    def test_missing_zone_model_or_marker_is_skipped_without_queries(self):
        with mock.patch.object(migration, "live_model", return_value=None):
            with self.assertNumQueries(0):
                self.run_migration()
        with mock.patch.object(migration, "live_field", return_value=None):
            with self.assertNumQueries(0):
                self.run_migration()

    def test_missing_zone_table_is_skipped(self):
        with mock.patch.object(migration, "table_names", return_value=set()):
            with self.assertNumQueries(0):
                self.run_migration()

    def test_missing_link_column_is_skipped(self):
        zone = RealityZone.objects.create(name="Legacy reference")
        node_model = registry.entry("locations.Node").model
        node_model.objects.create(name="Legacy node", reality_zone=zone)
        RealityZone.objects.filter(pk=zone.pk).update(is_player_zone=False)
        original_columns = migration.table_columns

        def columns_without_node_link(db, table):
            columns = original_columns(db, table)
            return columns - {"reality_zone_id"} if table == node_model._meta.db_table else columns

        with mock.patch.object(migration, "table_columns", side_effect=columns_without_node_link):
            self.run_migration()
        zone.refresh_from_db()
        self.assertFalse(zone.is_player_zone)


class ProtectPlayerRealityZonesSchemaTests(TransactionTestCase):
    def test_legacy_database_gets_column_and_backfill_without_rewriting_names(self):
        zone = RealityZone.objects.create(name="Original private name")
        node_model = registry.entry("locations.Node").model
        node_model.objects.create(name=zone.name, reality_zone=zone)
        standalone = RealityZone.objects.create(name="Independent staff reference")
        field = RealityZone._meta.get_field("is_player_zone")

        def restore_column():
            with connection.schema_editor() as editor:
                migration.protect_player_reality_zones(None, editor)

        self.addCleanup(restore_column)
        with connection.schema_editor() as editor:
            editor.remove_field(RealityZone, field)
        self.assertNotIn("is_player_zone", table_columns(connection, RealityZone._meta.db_table))
        restore_column()
        self.assertIn("is_player_zone", table_columns(connection, RealityZone._meta.db_table))
        zone.refresh_from_db()
        standalone.refresh_from_db()
        self.assertTrue(zone.is_player_zone)
        self.assertFalse(standalone.is_player_zone)
        self.assertEqual(zone.name, "Original private name")
        with connection.schema_editor(collect_sql=True) as editor:
            migration.protect_player_reality_zones(None, editor)
            self.assertEqual(editor.collected_sql, [])
