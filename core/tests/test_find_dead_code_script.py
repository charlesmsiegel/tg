"""Smoke test for scripts/find_dead_code.py.

The script points the default database at in-memory SQLite when imported, so it
runs in a subprocess rather than inside the test runner's process.
"""

import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "find_dead_code.py"
SECTIONS = ("urls", "views", "templates", "tags", "symbols")


class FindDeadCodeScriptTest(SimpleTestCase):
    def test_every_section_runs_and_reports_a_summary(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *(f"--section={s}" for s in SECTIONS)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        # The script reports import or parse failures as "warning:" lines; those
        # would silently shrink the scan. Library warnings on stderr are fine.
        script_warnings = [
            line for line in result.stderr.splitlines() if line.startswith("warning:")
        ]
        self.assertEqual(script_warnings, [])
        for section in SECTIONS:
            self.assertIn(f"## {section}", result.stdout)
        self.assertIn("**Summary:**", result.stdout)

    def test_tsv_format_is_one_tab_separated_row_per_line(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--section=urls", "--format=tsv"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertTrue(lines[0].startswith("# urls\t"), lines[0])
        self.assertNotIn("**Summary:**", result.stdout)
        headers, rows = None, 0
        for line in lines[1:]:
            fields = line.split("\t")
            if fields[:2] == ["section", "table"]:
                headers = fields
                continue
            self.assertIsNotNone(headers, f"row before any header: {line!r}")
            self.assertEqual(fields[0], "urls", line)
            self.assertEqual(len(fields), len(headers), line)
            rows += 1
        self.assertGreater(rows, 0)
        self.assertIn(
            "\t".join(
                ("section", "table", "URL name", "Route", "View", "Status", "Dead-route kind")
            ),
            lines,
        )
