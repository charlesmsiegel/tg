"""Tests for the reset_db management command."""

import os
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings


class ResetDbTests(SimpleTestCase):
    """reset_db works on the current directory, so each test runs in a scratch one."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        cwd = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)
        for app, name in [("core", "0001_initial.py"), ("tg_schema", "0001_scene_visibility.py")]:
            migrations = self.root / app / "migrations"
            migrations.mkdir(parents=True)
            (migrations / "__init__.py").write_text("")
            (migrations / name).write_text("")
        (self.root / "db.sqlite3").write_text("")

    @override_settings(DEBUG=True)
    def test_keeps_committed_tg_schema_migrations(self):
        call_command("reset_db", "--yes", stdout=StringIO())
        self.assertFalse((self.root / "db.sqlite3").exists())
        self.assertFalse((self.root / "core/migrations/0001_initial.py").exists())
        self.assertTrue((self.root / "core/migrations/__init__.py").exists())
        self.assertTrue((self.root / "tg_schema/migrations/0001_scene_visibility.py").exists())

    @override_settings(DEBUG=False)
    def test_refuses_without_debug(self):
        with self.assertRaises(CommandError):
            call_command("reset_db", "--yes", stdout=StringIO())
        self.assertTrue((self.root / "db.sqlite3").exists())
