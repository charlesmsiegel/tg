"""Guard: views do not choose an action from POST keys, and detail views do
not handle POST (Step 5). Each action has its own endpoint instead."""

import ast
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import get_resolver
from django.views.generic import DetailView

from core.views.generic import DictView

APPS = ("accounts", "characters", "core", "game", "items", "locations", "widgets")


def _view_modules():
    root = Path(settings.BASE_DIR)
    for app in APPS:
        base = root / app
        yield from base.glob("views.py")
        yield from base.glob("views/**/*.py")
        yield from base.glob("actions.py")


def _is_post_data(node):
    """``request.POST``, ``self.request.POST``, ``form.data`` and the like."""
    return isinstance(node, ast.Attribute) and node.attr in {"POST", "data"}


def _button_dispatch(tree):
    """Yield line numbers that test which button or key was posted.

    ``"close_scene" in request.POST`` and ``"Approve" in request.POST.values()``
    are dispatch; a computed formset key (``f"{prefix}-{i}-x" in form.data``)
    is parsing and is allowed.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare) and any(
            isinstance(op, ast.In | ast.NotIn) for op in node.ops
        ):
            literal = isinstance(node.left, ast.Constant) and isinstance(node.left.value, str)
            for target in node.comparators:
                if literal and _is_post_data(target):
                    yield node.lineno
                if (
                    isinstance(target, ast.Call)
                    and isinstance(target.func, ast.Attribute)
                    and target.func.attr in {"keys", "values", "items"}
                    and _is_post_data(target.func.value)
                ):
                    yield node.lineno


class ActionGuardTests(SimpleTestCase):
    def test_no_view_dispatches_on_posted_button_names(self):
        offenders = []
        for path in _view_modules():
            tree = ast.parse(path.read_text(), filename=str(path))
            offenders += [f"{path}:{line}" for line in _button_dispatch(tree)]
        self.assertEqual(offenders, [], "Give each action its own endpoint (core.actions)")

    def test_routed_detail_views_do_not_handle_post(self):
        seen, offenders = set(), []

        def visit(view):
            if not isinstance(view, type) or view in seen:
                return
            seen.add(view)
            if issubclass(view, DictView):
                mapping = view.view_mapping
                if isinstance(mapping, property):
                    mapping = view().view_mapping
                for target in dict(mapping).values():
                    visit(target)
                visit(view.default_redirect)
                return
            if (
                issubclass(view, DetailView)
                and view.__module__.startswith(tuple(f"{app}." for app in APPS))
                and hasattr(view, "post")
            ):
                offenders.append(f"{view.__module__}.{view.__qualname__}")

        def walk(patterns):
            for pattern in patterns:
                if hasattr(pattern, "url_patterns"):
                    walk(pattern.url_patterns)
                else:
                    visit(getattr(pattern.callback, "view_class", None))

        walk(get_resolver().url_patterns)
        self.assertGreater(len(seen), 100)
        self.assertEqual(sorted(offenders), [])
