"""Tests for the populate_gamedata management command."""

import os
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


def dry_run(*args):
    out = StringIO()
    call_command("populate_gamedata", "--dry-run", *args, stdout=out)
    return out.getvalue()


class GamelineFilterTests(TestCase):
    """--gameline matches the folder and whole name words, by code or by name."""

    def test_code_selects_the_gameline_folder(self):
        output = dry_run("--gameline", "vtm")
        self.assertIn("vampire/vampire_clans.py", output)
        self.assertIn("vampire/linear_magic_path.py", output)
        self.assertIn("character_templates/vampire_templates.py", output)
        self.assertIn("abilities.py", output)
        self.assertNotIn("mage/spheres.py", output)
        self.assertNotIn("character_templates/mage_templates.py", output)

    def test_name_and_code_select_the_same_files(self):
        self.assertEqual(dry_run("--gameline", "vampire"), dry_run("--gameline", "vtm"))

    def test_mummy_is_a_gameline(self):
        output = dry_run("--gameline", "mtr")
        self.assertIn("mummy/dynasties.py", output)
        self.assertNotIn("vampire/vampire_clans.py", output)

    def test_unknown_gameline_is_an_error(self):
        with self.assertRaises(CommandError):
            dry_run("--gameline", "xyz")


class FailureExitTests(TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        scripts = Path(tmp.name) / "populate_db"
        scripts.mkdir()
        (scripts / "good.py").write_text("LOADED = True\n")
        (scripts / "broken.py").write_text("raise RuntimeError('bad data')\n")
        cwd = os.getcwd()
        os.chdir(tmp.name)
        self.addCleanup(os.chdir, cwd)

    def test_failed_script_makes_the_command_fail_after_running_the_rest(self):
        out = StringIO()
        with (
            self.assertLogs("core.management.commands.populate_gamedata", "ERROR"),
            self.assertRaises(CommandError),
        ):
            call_command("populate_gamedata", stdout=out)
        self.assertIn("✓ good.py", out.getvalue())
        self.assertIn("✗ broken.py", out.getvalue())
