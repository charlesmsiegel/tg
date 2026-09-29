"""tg_schema migrations survive later renames: models and fields are looked up when
they run, never imported, and a missing one is skipped."""

import ast
import importlib
from pathlib import Path
from unittest import mock

from django.db import connection
from django.test import TestCase, TransactionTestCase

from tg_schema import schema

MIGRATIONS = Path(schema.__file__).resolve().parent / "migrations"
LOCAL_APPS = {"accounts", "characters", "core", "game", "items", "locations", "widgets"}


class LiveLookupTests(TransactionTestCase):
    def test_missing_models_and_fields_are_none(self):
        self.assertIsNone(schema.live_model("game.NoSuchModel"))
        self.assertIsNone(schema.live_model("nosuchapp.Story"))
        story = schema.live_model("game.Story")
        self.assertIsNone(schema.live_field(story, "no_such_field"))
        self.assertIsNone(schema.live_field(None, "chronicle"))
        self.assertEqual(schema.live_field(story, "chronicle").name, "chronicle")

    def test_a_renamed_field_or_model_is_skipped(self):
        with connection.schema_editor(collect_sql=True) as editor:
            self.assertEqual(schema.add_missing_columns(editor, "game.Story", ("gone",)), set())
            self.assertEqual(schema.add_missing_columns(editor, "game.Gone", ("name",)), set())
            self.assertEqual(editor.collected_sql, [])

    def test_every_migration_runs_when_its_models_are_gone(self):
        with mock.patch.object(schema.apps, "get_model", side_effect=LookupError):
            for path in sorted(MIGRATIONS.glob("[0-9]*.py")):
                module = importlib.import_module(f"tg_schema.migrations.{path.stem}")
                operation = module.Migration.operations[0]
                with self.subTest(migration=path.stem):
                    with connection.schema_editor(collect_sql=True) as editor:
                        operation.code(None, editor)


class NoModelImportsTests(TestCase):
    def test_migrations_import_no_app_models(self):
        for path in sorted(MIGRATIONS.glob("[0-9]*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imported = {
                node.module.split(".")[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            } | {
                alias.name.split(".")[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            with self.subTest(migration=path.stem):
                self.assertFalse(imported & LOCAL_APPS, "look models up with tg_schema.schema")
