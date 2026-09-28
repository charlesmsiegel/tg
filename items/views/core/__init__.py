from collections import defaultdict

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from core.utils import get_gameline_name
from core.views.generic import DictView
from core.views.public_object import PublicObjectDetailView, render_public_object_list
from core.views.registry import RegistryDetailView
from game.models import Chronicle, ObjectType
from items.forms.core.item_creation import ItemCreationForm
from items.models.core.item import ItemModel
from items.views import mage, werewolf

from .item import ItemCreateView, ItemDetailView, ItemUpdateView
from .material import (
    MaterialCreateView,
    MaterialDetailView,
    MaterialListView,
    MaterialUpdateView,
)
from .medium import MediumCreateView, MediumDetailView, MediumListView, MediumUpdateView
from .meleeweapon import (
    MeleeWeaponCreateView,
    MeleeWeaponDetailView,
    MeleeWeaponListView,
    MeleeWeaponUpdateView,
)
from .rangedweapon import (
    RangedWeaponCreateView,
    RangedWeaponDetailView,
    RangedWeaponListView,
    RangedWeaponUpdateView,
)
from .thrownweapon import (
    ThrownWeaponCreateView,
    ThrownWeaponDetailView,
    ThrownWeaponListView,
    ThrownWeaponUpdateView,
)
from .weapon import WeaponCreateView, WeaponDetailView, WeaponListView, WeaponUpdateView


class GenericItemDetailView(RegistryDetailView):
    registry_app = "items"
    model_class = ItemModel
    public_view_class = PublicObjectDetailView


class ItemIndexView(View):
    def get(self, request, *args, **kwargs):
        if not (
            request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        ):
            return render_public_object_list(
                request,
                ItemModel,
                (
                    {"item_form": ItemCreationForm(user=request.user)}
                    if request.user.is_authenticated
                    else None
                ),
            )
        context = self.get_context()
        return render(request, "items/index.html", context)

    def get_context(self):
        """Staff index (Spread M3): one chronicle at a time, items grouped into tables.

        ``?chronicle=<pk|none>`` picks the chronicle (default: the first that has
        items) and ``?line=<code>`` narrows it to one gameline.
        """
        chronicles = list(Chronicle.objects.all()) + [None]
        by_chronicle = {chron: [] for chron in chronicles}
        items = (
            ItemModel.objects.visible()
            .select_related("polymorphic_ctype", "owner", "chronicle")
            .prefetch_related("owned_by")
            .order_by("name")
        )
        for item in items:
            by_chronicle.setdefault(item.chronicle, []).append(item)

        params = self.request.GET
        keys = {str(chron.pk) if chron else "none": chron for chron in by_chronicle}
        if params.get("chronicle") in keys:
            selected = keys[params["chronicle"]]
        else:
            selected = next((chron for chron, found in by_chronicle.items() if found), None)
        chron_key = str(selected.pk) if selected else "none"
        chronicle_items = by_chronicle[selected]

        line_counts = {}
        for item in chronicle_items:
            line = item.get_gameline()
            line_counts[line] = line_counts.get(line, 0) + 1
        line = params.get("line")
        if line not in line_counts:
            line = "all"
        shown = [item for item in chronicle_items if line == "all" or item.get_gameline() == line]

        return {
            "form": ItemCreationForm(user=self.request.user),
            "selected_chronicle": selected,
            "chronicle_key": chron_key,
            "selected_line": line,
            "item_count": len(chronicle_items),
            "chronicle_switch": [
                {"chronicle": chron, "key": str(chron.pk) if chron else "none"}
                for chron in by_chronicle
                if chron != selected
            ],
            "line_tabs": [{"key": "all", "label": "All lines", "count": len(chronicle_items)}]
            + [
                {"key": code, "label": gameline_label(code), "count": line_counts[code]}
                for code in [*(c for c in settings.GAMELINES if c != "wod"), "wod"]
                if code in line_counts
            ],
            "item_groups": group_items(shown),
        }


# Index tables, in this order; every other item falls into its gameline's group.
ITEM_GROUPS = (
    ("wonders", "Wonders"),
    ("grimoires", "Grimoires"),
    ("fetishes", "Fetishes & Talens"),
)


def gameline_label(code):
    """ "Mage" for "mta", "World of Darkness" for the generic line."""
    name = settings.GAMELINES.get(code, {}).get("name", code)
    return name if code == "wod" else name.split(":")[0]


def item_group(item):
    """(key, label) of the index table an item is listed in."""
    line, kind = item.get_gameline(), item.type
    if line == "mta":
        return ITEM_GROUPS[1] if kind == "grimoire" else ITEM_GROUPS[0]
    if line == "wta":
        return ITEM_GROUPS[2]
    if line == "wod":
        return ("weapons", "Weapons") if "weapon" in kind else ("wod", "Other items")
    return (line, f"{gameline_label(line)} items")


def group_items(items):
    """[{key, label, items}] in ITEM_GROUPS order, then gameline order, then weapons and
    other generic items."""
    order = [key for key, _ in ITEM_GROUPS] + [
        code for code in settings.GAMELINES if code not in ("mta", "wta", "wod")
    ]
    order += ["weapons", "wod"]
    groups = {}
    for item in items:
        key, label = item_group(item)
        groups.setdefault(key, {"key": key, "label": label, "items": []})["items"].append(item)
    return [groups[key] for key in order if key in groups]


__all__ = [
    "defaultdict",
    "Http404",
    "redirect",
    "render",
    "View",
    "get_gameline_name",
    "DictView",
    "Chronicle",
    "ObjectType",
    "ItemCreationForm",
    "ItemModel",
    "mage",
    "werewolf",
    "ItemCreateView",
    "ItemDetailView",
    "ItemUpdateView",
    "MaterialCreateView",
    "MaterialDetailView",
    "MaterialListView",
    "MaterialUpdateView",
    "MediumCreateView",
    "MediumDetailView",
    "MediumListView",
    "MediumUpdateView",
    "MeleeWeaponCreateView",
    "MeleeWeaponDetailView",
    "MeleeWeaponListView",
    "MeleeWeaponUpdateView",
    "RangedWeaponCreateView",
    "RangedWeaponDetailView",
    "RangedWeaponListView",
    "RangedWeaponUpdateView",
    "ThrownWeaponCreateView",
    "ThrownWeaponDetailView",
    "ThrownWeaponListView",
    "ThrownWeaponUpdateView",
    "WeaponCreateView",
    "WeaponDetailView",
    "WeaponListView",
    "WeaponUpdateView",
]
