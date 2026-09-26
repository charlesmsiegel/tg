from collections import defaultdict

from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

from core.create_redirects import resolve_object_type_url
from core.model_registry import get_registry
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

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        item_type = request.POST.get("item_type")
        if not item_type or action not in {"create", "index"}:
            return HttpResponseBadRequest("Invalid item selection")
        if action == "create":
            if not request.user.is_authenticated:
                return HttpResponseBadRequest("Login required")
        return redirect(
            resolve_object_type_url(
                "obj",
                item_type,
                "create" if action == "create" else "list",
                request.POST.get("gameline"),
            )
        )

    def get_context(self):
        game_items = get_registry("items").menu(self.request.user)
        context = {
            "objects": game_items,
        }

        chron_dict = {}
        for chron in list(Chronicle.objects.all()) + [None]:
            if chron:
                c = ItemModel.objects.for_chronicle(chron).order_by("name")
            else:
                c = ItemModel.objects.filter(chronicle=chron).order_by("name")
            c = c.with_polymorphic_ctype()
            chron_dict[chron] = c

        context["chron_dict"] = chron_dict
        context["form"] = ItemCreationForm(user=self.request.user)
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"

        return context


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
