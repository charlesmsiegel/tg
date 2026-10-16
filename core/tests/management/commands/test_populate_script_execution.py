"""Populate scripts retain their source identity and transaction error boundary."""

import json
import tempfile
import traceback
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.test import SimpleTestCase

from core.management.commands.populate_gamedata import Command


class PopulateScriptExecutionTests(SimpleTestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        self.script = self.directory / "example.py"
        self.output = StringIO()
        self.command = Command(stdout=self.output, no_color=True)

    def test_script_receives_file_and_main_name(self):
        self.script.write_text(
            "import json\n"
            "from pathlib import Path\n"
            "Path(__file__).with_suffix('.json').write_text(\n"
            "    json.dumps({'file': __file__, 'name': __name__}))\n"
        )
        with patch("core.management.commands.populate_gamedata.transaction.atomic"):
            self.command.load_file(self.script, self.directory)
        identity = json.loads(self.script.with_suffix(".json").read_text())
        self.assertEqual(Path(identity["file"]), self.script)
        self.assertEqual(identity["name"], "__main__")
        self.assertEqual(self.output.getvalue(), "✓ example.py\n")

    def test_failure_retains_script_filename_and_reaches_transaction_boundary(self):
        self.script.write_text("raise RuntimeError('bad fixture')\n")
        with patch("core.management.commands.populate_gamedata.transaction.atomic") as atomic:
            try:
                self.command.load_file(self.script, self.directory, verbose=True)
            except RuntimeError as error:
                frames = traceback.extract_tb(error.__traceback__)
                self.assertEqual(str(error), "bad fixture")
                self.assertIn((str(self.script), 1), [(f.filename, f.lineno) for f in frames])
                exit_args = atomic.return_value.__exit__.call_args.args
                self.assertIs(exit_args[0], RuntimeError)
                self.assertIs(exit_args[1], error)
            else:
                self.fail("script error did not propagate")
        self.assertEqual(self.output.getvalue(), "Loading example.py...")

    def test_script_executes_inside_atomic_block_and_preserves_verbose_output(self):
        marker = self.directory / "transaction-active"
        self.script.write_text(f"from pathlib import Path\nassert Path({str(marker)!r}).exists()\n")
        with patch("core.management.commands.populate_gamedata.transaction.atomic") as atomic:
            atomic.return_value.__enter__.side_effect = lambda: marker.touch()
            self.command.load_file(self.script, self.directory, verbose=True)
            atomic.assert_called_once_with()
        self.assertEqual(self.output.getvalue(), "Loading example.py... ✓\n")
