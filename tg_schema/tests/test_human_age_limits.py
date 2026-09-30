"""tg_schema 0009 replaces the Human age checks with the wider 0-65535 range."""

import importlib
from unittest import mock

from django.db import IntegrityError, connection, transaction
from django.test import TransactionTestCase

from characters.models.core.human import Human

migration = importlib.import_module("tg_schema.migrations.0009_human_age_limits")


def run_migration():
    with connection.schema_editor() as schema_editor:
        migration.widen_age_limits(None, schema_editor)


def constraint_names():
    with connection.cursor() as cursor:
        return set(connection.introspection.get_constraints(cursor, Human._meta.db_table))


class HumanAgeLimitsMigrationTests(TransactionTestCase):
    def test_checks_are_kept_and_allow_long_lived_ages(self):
        run_migration()
        run_migration()

        self.assertLessEqual({name for _, name in migration.CHECKS}, constraint_names())
        Human.objects.create(name="Elder", age=2000, apparent_age=40)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Human.objects.filter(name="Elder").update(age=-1)

    def test_skips_when_model_is_gone(self):
        with (
            mock.patch.object(migration, "live_model", return_value=None),
            connection.schema_editor() as schema_editor,
            mock.patch.object(schema_editor, "add_constraint") as add_constraint,
        ):
            migration.widen_age_limits(None, schema_editor)
        add_constraint.assert_not_called()

    def test_skips_renamed_fields(self):
        with (
            mock.patch.object(migration, "live_field", return_value=None),
            connection.schema_editor() as schema_editor,
            mock.patch.object(schema_editor, "add_constraint") as add_constraint,
        ):
            migration.widen_age_limits(None, schema_editor)
        add_constraint.assert_not_called()
