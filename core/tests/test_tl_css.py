"""tl.css is appended to by area by area; a merge that drops a closing brace swallows
every rule after it into the preceding @media block (desktop pages then lose them)."""

import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase


class TlCssBalanceTest(SimpleTestCase):
    def test_every_block_is_closed(self):
        source = (Path(settings.BASE_DIR) / "core/static/core/tl/tl.css").read_text(
            encoding="utf-8"
        )
        source = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), source, flags=re.S)
        open_lines = []
        for number, line in enumerate(source.split("\n"), 1):
            for char in line:
                if char == "{":
                    open_lines.append(number)
                elif char == "}":
                    self.assertTrue(open_lines, f"unmatched '}}' on line {number}")
                    open_lines.pop()
        self.assertEqual(open_lines, [], "blocks opened on these lines are never closed")
