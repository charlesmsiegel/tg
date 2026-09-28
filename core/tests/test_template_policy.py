"""Ratchets for the template policy in the Step 8 design
(docs/superpowers/specs/2026-09-25-template-consolidation-design.md).

* Inline ``style="..."`` attributes may only go down: styles belong in
  ``core/static/core/tl/tl.css`` (Spread). Lower ``INLINE_STYLE_BUDGET`` when a
  cleanup removes some.
* ``<style>`` blocks may only live in the templates listed here.
* No template sits more than ``MAX_EXTENDS_DEPTH`` ``{% extends %}`` hops below
  its root (``core/tl_base.html`` → character → human → gameline → splat).
"""

import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

APPS = ("accounts", "characters", "core", "game", "items", "locations")
INLINE_STYLE_BUDGET = 3
STYLE_BLOCK_TEMPLATES = {
    "accounts/registration/password_reset_email.html",
}
MAX_EXTENDS_DEPTH = 5
EXTENDS = re.compile(r'{%\s*extends\s+"([^"]+)"')


def project_templates():
    """{template name: source} for every app template (generated docs excluded)."""
    templates = {}
    for app in APPS:
        root = Path(settings.BASE_DIR) / app / "templates"
        for path in root.rglob("*.html"):
            if "docs" not in path.parts:
                templates[str(path.relative_to(root))] = path.read_text(encoding="utf-8")
    return templates


class TemplatePolicyTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.templates = project_templates()

    def test_inline_styles_do_not_grow(self):
        count = sum(source.count('style="') for source in self.templates.values())
        self.assertLessEqual(
            count,
            INLINE_STYLE_BUDGET,
            "New inline styles: move them to a stylesheet under source_static/",
        )

    def test_style_blocks_only_in_known_templates(self):
        found = {name for name, source in self.templates.items() if "<style" in source}
        self.assertLessEqual(
            found, STYLE_BLOCK_TEMPLATES, "Move new <style> blocks to source_static/pages/"
        )

    def test_extends_depth(self):
        def depth(name, seen=()):
            match = EXTENDS.search(self.templates.get(name, ""))
            if not match or name in seen:
                return 0
            return 1 + depth(match.group(1), (*seen, name))

        too_deep = {name: depth(name) for name in self.templates if depth(name) > MAX_EXTENDS_DEPTH}
        self.assertEqual(too_deep, {})
