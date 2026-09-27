"""Guards for Step 4: views may not route invalid forms into form_valid."""

import ast
from pathlib import Path
from unittest import TestCase

from django.conf import settings

VIEW_DIRS = ("characters/views", "items/views", "locations/views", "game", "core/views")


def view_modules():
    root = Path(settings.BASE_DIR)
    for directory in VIEW_DIRS:
        base = root / directory
        paths = base.rglob("*.py") if base.is_dir() else []
        for path in paths:
            if "tests" in path.parts or "migrations" in path.parts:
                continue
            yield path


class ValidationBypassGuardTest(TestCase):
    def test_form_invalid_never_calls_form_valid(self):
        offenders = []
        for path in view_modules():
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "form_invalid":
                    for call in ast.walk(node):
                        if (
                            isinstance(call, ast.Call)
                            and isinstance(call.func, ast.Attribute)
                            and call.func.attr == "form_valid"
                        ):
                            offenders.append(f"{path}:{call.lineno}")
        self.assertEqual(offenders, [], "form_invalid must not call form_valid")
