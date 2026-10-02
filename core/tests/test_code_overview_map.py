"""Guard for ``docs/code-overview.json``, the package map behind ``docs/code-overview.html``.

The map names the units the generated code overview is built from. A root that no longer
exists, or two units sharing a name or a docs directory, would make the next regeneration
grade nothing or overwrite one unit's pages with another's, so the map is checked here
rather than discovered to be stale at regeneration time.
"""

import json
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

MAP = Path(settings.BASE_DIR) / "docs" / "code-overview.json"
REQUIRED_KEYS = {"name", "roots", "docs", "language", "doctor"}


class CodeOverviewMapTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = json.loads(MAP.read_text(encoding="utf-8"))
        cls.packages = cls.data["packages"]

    def test_schema_and_commit(self):
        self.assertEqual(self.data["schema"], "code-overview/1")
        self.assertRegex(self.data["commit"], r"^[0-9a-f]{7,40}$")

    def test_every_package_has_the_expected_keys(self):
        for package in self.packages:
            self.assertEqual(set(package), REQUIRED_KEYS, package.get("name"))
            self.assertIsInstance(package["roots"], list, package["name"])
            self.assertTrue(package["roots"], package["name"])

    def test_names_and_docs_directories_are_unique(self):
        names = [package["name"] for package in self.packages]
        docs = [package["docs"] for package in self.packages]
        self.assertEqual(len(names), len(set(names)), names)
        self.assertEqual(len(docs), len(set(docs)), docs)

    def test_every_root_exists_and_owns_its_docs_directory(self):
        # The docs directory itself is created on regeneration (scripts/ has none in
        # the tree), so only its placement under the first root is checked.
        base = Path(settings.BASE_DIR)
        for package in self.packages:
            for root in package["roots"]:
                self.assertTrue((base / root).is_dir(), f"{package['name']}: {root}")
            self.assertEqual(package["docs"], f"{package['roots'][0]}/docs", package["name"])

    def test_paths_are_repo_relative(self):
        for package in self.packages:
            for path in [*package["roots"], package["docs"]]:
                self.assertFalse(path.startswith("/"), path)
                self.assertNotIn("..", Path(path).parts, path)
