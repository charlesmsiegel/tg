"""Guards for code deleted by the Step 1 dead-code removal.

Design: docs/superpowers/specs/2026-09-25-dead-code-removal-design.md. Each rollout PR adds
one ``SimpleTestCase`` subclass named after its PR ID (``D2DependencyRemovedTest``, ...) that
mixes in ``RemovalAssertions``. A guard fails while the dead code exists and keeps it from
coming back. Guards need no database, so every class is a ``SimpleTestCase``.
"""

import importlib
import importlib.util
import re
from pathlib import Path

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.urls import NoReverseMatch, get_resolver, reverse

REPO_ROOT = Path(settings.BASE_DIR)


class RemovalAssertions:
    """Assertions shared by every removal guard in this module."""

    def assertRequirementRemoved(self, distribution):
        names = set()
        for line in (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                names.add(re.split(r"[\s<>=!~;\[]", line, maxsplit=1)[0].lower())
        self.assertNotIn(distribution.lower(), names)

    def assertModuleRemoved(self, dotted_path):
        try:
            spec = importlib.util.find_spec(dotted_path)
        except ModuleNotFoundError:  # a parent package is gone too
            spec = None
        self.assertIsNone(spec, f"{dotted_path} still exists")

    def assertAttributesRemoved(self, module_path, *names):
        module = importlib.import_module(module_path)
        for name in names:
            with self.subTest(name=f"{module_path}.{name}"):
                self.assertFalse(hasattr(module, name), f"{module_path}.{name} still exists")
                self.assertNotIn(name, getattr(module, "__all__", ()))

    def assertUrlNamesRemoved(self, *names):
        for name in names:
            with self.subTest(name=name), self.assertRaises(NoReverseMatch):
                reverse(name)

    def assertUrlNamespaceRemoved(self, namespace):
        *parents, leaf = namespace.split(":")
        resolver = get_resolver()
        for parent in parents:
            resolver = resolver.namespace_dict[parent][1]
        self.assertNotIn(leaf, resolver.namespace_dict, f"{namespace} is still mounted")

    def assertTemplatesRemoved(self, *names):
        for name in names:
            with self.subTest(name=name), self.assertRaises(TemplateDoesNotExist):
                get_template(name)


class D2DependencyRemovedTest(RemovalAssertions, SimpleTestCase):
    """D2: django-smart-selects is not a dependency."""

    def test_django_smart_selects_not_in_requirements(self):
        self.assertRequirementRemoved("django-smart-selects")
