"""Generate a reviewable starting manifest from the current URL inventory.

Run only when deliberately classifying newly routed views. The runtime never
generates policies; an unlisted callback is denied and fails the route test.
"""

# Django must initialize before model imports in this standalone script.
# ruff: noqa: E402

import importlib
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")

import django

django.setup()

from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from characters.models.changeling.chimera import Chimera
from characters.models.core import CharacterModel, Group
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from core.models import CharacterTemplate
from core.views.generic import DictView
from items.models.core import ItemModel
from locations.models.core import LocationModel
from scripts.inventory_authorization_routes import get_resolver, walk

PROJECT_PREFIXES = ("accounts.", "characters.", "core.", "game.", "items.", "locations.", "widgets.")
PLAYER_MODELS = (CharacterModel, Group, Chimera, Effect, Rote, ItemModel, LocationModel, CharacterTemplate)


def classify(name, view, step_names):
    if name in {
        "characters.views.core.human.LoadExamplesView",
        "characters.views.core.human.LoadValuesView",
        "characters.views.mage.companion.LoadExamplesView",
        "characters.views.mage.mage.GetAbilitiesView",
        "characters.views.mage.mage.LoadXPExamplesView",
        "characters.views.mage.sorcerer.LoadExamplesView",
    }:
        return "OBJECT_AJAX"
    if name == "core.views.public_object.PublicObjectDetailView":
        return "PUBLIC_CARD"
    if name == "characters.views.core.CharacterIndexView":
        return "PUBLIC_INDEX"
    if name.startswith("widgets."):
        return "WIDGET"
    if name.startswith("accounts."):
        return "PUBLIC_READ" if name.rsplit(".", 1)[-1] in {
            "SignUp", "CustomLoginView", "CustomPasswordResetView"
        } else "ACCOUNT"
    if name.startswith("game."):
        return "GAME"
    if issubclass(view, DictView):
        return "ROUTER"
    if name in step_names:
        return "CHARGEN_STEP"
    model = getattr(view, "model", None)
    player_object = isinstance(model, type) and issubclass(model, PLAYER_MODELS)
    if player_object:
        if issubclass(view, CreateView):
            return "OBJECT_CREATE"
        if issubclass(view, UpdateView | DeleteView):
            return "OBJECT_WRITE"
        if issubclass(view, DetailView):
            return "OBJECT_DETAIL"
        if issubclass(view, ListView):
            return "OBJECT_LIST"
        return "OBJECT_ACTION"
    if isinstance(model, type):
        if issubclass(view, CreateView | UpdateView | DeleteView):
            return "STAFF_WRITE"
        if issubclass(view, DetailView | ListView):
            return "PUBLIC_READ"
    if "IndexView" in name or name == "core.views.home.HomeListView":
        return "PUBLIC_INDEX"
    return "LOGIN"


def main():
    rows = list(walk(get_resolver().url_patterns))
    names = {row[2] for row in rows if row[2].startswith(PROJECT_PREFIXES)}
    step_names = {
        row[2] for row in rows
        if row[1] and row[1].rsplit("/", 1)[-1].isdigit()
        and row[0].startswith(("characters/", "locations/"))
    }
    groups = defaultdict(list)
    for name in sorted(names):
        module, class_name = name.rsplit(".", 1)
        view = getattr(importlib.import_module(module), class_name)
        groups[classify(name, view, step_names)].append(name)

    lines = [
        '"""Explicit, reviewed route policies. Missing entries deny in production."""',
        "",
        "POLICIES = {",
    ]
    for policy, members in sorted(groups.items()):
        lines.append(f"    {policy!r}: frozenset(\"\"\"")
        lines.extend(members)
        lines.append('    """.split()),')
    lines.extend(["}", "", "VIEW_POLICIES = {name: policy for policy, names in POLICIES.items() for name in names}", ""])
    output = Path(__file__).resolve().parent.parent / "core" / "route_policy_manifest.py"
    output.write_text("\n".join(lines), encoding="utf-8")
    for policy, members in sorted(groups.items()):
        print(f"{policy}: {len(members)}")


if __name__ == "__main__":
    main()
