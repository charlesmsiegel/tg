"""Print the effective Django URL/view authorization inventory as Markdown.

Run: python scripts/inventory_authorization_routes.py > route-inventory.md
The script is read-only; no database connection is required.
"""

import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")

import django  # noqa: E402

django.setup()

from django.contrib.auth.mixins import (  # noqa: E402
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import URLPattern, URLResolver, get_resolver  # noqa: E402
from django.views import View  # noqa: E402

from core.mixins import (  # noqa: E402
    AjaxLoginRequiredMixin,
    CharacterOwnerOrSTMixin,
    OwnerRequiredMixin,
    PermissionRequiredMixin,
    StorytellerRequiredMixin,
)
from core.views.generic import DictView  # noqa: E402


def descendants(view_class, trail=()):
    """Include every nested DictView branch and class-valued fallback."""
    if not issubclass(view_class, DictView) or view_class in trail:
        return
    instance = view_class()
    try:
        mapping = instance.view_mapping
    except Exception as exc:  # Keep a broken router visible.
        yield ("<mapping error>", None, str(exc))
        return
    for key, target in mapping.items():
        if not isinstance(target, type):
            yield (str(key), None, repr(target))
            continue
        yield (str(key), target, "")
        for suffix, child, error in descendants(target, (*trail, view_class)):
            yield (f"{key}/{suffix}", child, error)
    fallback = instance.default_redirect
    if isinstance(fallback, type) and issubclass(fallback, View):
        yield ("<default>", fallback, "")
        for suffix, child, error in descendants(fallback, (*trail, view_class)):
            yield (f"<default>/{suffix}", child, error)
    public_target = getattr(instance, "public_view_class", None)
    if isinstance(public_target, type) and issubclass(public_target, View):
        yield ("<public>", public_target, "")
        for suffix, child, error in descendants(public_target, (*trail, view_class)):
            yield (f"<public>/{suffix}", child, error)


def gate(view_class):
    if view_class is None:
        return "mapping error", "no"
    mro = view_class.__mro__
    if PermissionRequiredMixin in mro:
        permission = getattr(view_class, "required_permission", None)
        return (f"Permission.{permission.name}" if permission else "permission unset"), "yes"
    if StorytellerRequiredMixin in mro:
        return "scoped StorytellerRequiredMixin", "yes"
    if CharacterOwnerOrSTMixin in mro:
        return "CharacterOwnerOrSTMixin", "yes"
    if OwnerRequiredMixin in mro:
        return "OwnerRequiredMixin", "yes"
    if AjaxLoginRequiredMixin in mro:
        return "AjaxLoginRequiredMixin", "yes"
    if LoginRequiredMixin in mro:
        return "LoginRequiredMixin", "yes"
    if UserPassesTestMixin in mro:
        return "UserPassesTestMixin", "unknown"
    return "none", "no"


def methods(view_class):
    if view_class is None:
        return "unknown"
    accepted = [
        method.upper()
        for method in view_class.http_method_names
        if hasattr(view_class, method)
    ]
    if "GET" in accepted and "HEAD" not in accepted:
        accepted.append("HEAD")
    return ",".join(accepted)


def intended(view_class, route, branch):
    """Policy family for review; the spec supplies each family's exact rules."""
    module = view_class.__module__ if view_class else ""
    if route.startswith("__chained_select__/"):
        return "login-only: allowlisted GET"
    if module.startswith(("django.", "debug_toolbar.")) or not module.startswith(
        ("core.", "characters.", "items.", "locations.", "game.", "accounts.", "widgets.")
    ):
        return "framework-owned: explicit exclusion"
    if module.startswith("accounts."):
        return "login-only: own profile or scoped object"
    if module.startswith("game."):
        if "ListView" in view_class.__name__:
            return "object-permission: filtered chronicle collection"
        return "object-permission: chronicle scoped"
    if module.startswith("widgets."):
        return "login-only: allowlisted GET"
    if module.startswith("core."):
        if view_class.__name__ == "PublicObjectDetailView":
            return "object-permission: public projection GET"
        if "CharacterTemplate" in view_class.__name__:
            if "DetailView" in view_class.__name__:
                return "object-permission: public GET / full VIEW_FULL"
            if "ListView" in view_class.__name__:
                return "object-permission: filtered public/full collection"
            return "object-permission: template action scoped to owner/ST/staff"
        if "CreateView" in view_class.__name__ or "UpdateView" in view_class.__name__:
            return "object-permission: reference write ADMIN"
        return "public-reference: GET/HEAD only"
    if issubclass(view_class, DictView):
        return "object-permission: public GET / full target"
    if route.startswith("characters/") and branch and branch.rsplit("/", 1)[-1].isdigit():
        return "object-permission: chargen SPEND_FREEBIES or VIEW_FULL"
    model = getattr(view_class, "model", None)
    if model is not None and not hasattr(model, "owner"):
        if "CreateView" in view_class.__name__ or "UpdateView" in view_class.__name__:
            return "object-permission: reference write ADMIN"
        return "public-reference: GET/HEAD only"
    if "IndexView" in view_class.__name__ or "ListView" in view_class.__name__:
        return "login-only: filtered collection"
    if "CreateView" in view_class.__name__ or "BasicsView" in view_class.__name__:
        return "object-permission: create policy"
    if "DetailView" in view_class.__name__:
        return "object-permission: public GET / full VIEW_FULL"
    return "object-permission: object/action policy"


def walk(patterns, prefix=""):
    for pattern in patterns:
        route = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            yield from walk(pattern.url_patterns, route)
        elif isinstance(pattern, URLPattern):
            callback = pattern.callback
            view_class = getattr(callback, "view_class", None)
            if view_class is None:
                name = f"{callback.__module__}.{callback.__name__}"
                yield route, "", name, "function/unknown", "unknown", "ANY*", intended(None, route, "")
                continue
            branch = f"{view_class.__module__}.{view_class.__name__}"
            current_gate, login = gate(view_class)
            yield route, "", branch, current_gate, login, methods(view_class), intended(view_class, route, "")
            for key, target, error in descendants(view_class):
                name = (
                    f"{target.__module__}.{target.__name__}" if target else error
                )
                child_gate, child_login = gate(target)
                yield route, key, name, child_gate, child_login, methods(target), intended(target, route, key)


def main():
    from core.route_policy_manifest import VIEW_POLICIES

    def effective_login(policy):
        if policy in {
            "ACCOUNT", "CHARGEN_STEP", "LOGIN", "OBJECT_ACTION",
            "OBJECT_AJAX", "OBJECT_CREATE", "OBJECT_WRITE", "STAFF_WRITE",
            "WIDGET",
        }:
            return "yes"
        if policy in {"PUBLIC_CARD", "PUBLIC_READ"}:
            return "no"
        if policy in {
            "GAME", "OBJECT_DETAIL", "OBJECT_LIST", "PUBLIC_INDEX", "ROUTER",
        }:
            return "mixed: public read / protected full or write"
        return "framework-owned"

    rows = list(walk(get_resolver().url_patterns))
    counts = Counter(row[3] for row in rows)
    print(f"Rows: {len(rows)}; direct routes: {sum(not r[1] for r in rows)}")
    for key, count in sorted(counts.items()):
        print(f"- {key}: {count}")
    print("\n| Route | Router branch | View class | Current MRO gate | Login enforced by MRO | Methods | Declared policy | Effective login policy | Intended policy family |")
    print("|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        policy = VIEW_POLICIES.get(row[2], "framework/undeclared")
        displayed = (*row[:-1], policy, effective_login(policy), row[-1])
        print("| " + " | ".join(str(value).replace("|", "\\|") for value in displayed) + " |")


if __name__ == "__main__":
    main()
