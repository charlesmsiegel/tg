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
from locations.forms.core.location_creation import LocationCreationForm
from locations.models.core.location import LocationModel
from locations.views import mage, werewolf

from .city import CityCreateView, CityDetailView, CityListView, CityUpdateView
from .location import LocationCreateView, LocationDetailView, LocationUpdateView


class GenericLocationDetailView(RegistryDetailView):
    registry_app = "locations"
    model_class = LocationModel
    public_view_class = PublicObjectDetailView


class LocationIndexView(View):
    def get(self, request, *args, **kwargs):
        if not (
            request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        ):
            return render_public_object_list(
                request,
                LocationModel,
                (
                    {"location_form": LocationCreationForm(user=request.user)}
                    if request.user.is_authenticated
                    else None
                ),
            )
        context = self.get_context()
        return render(request, "locations/index.html", context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        loc_type = request.POST.get("loc_type")
        if not loc_type or action not in {"create", "index"}:
            return HttpResponseBadRequest("Invalid location selection")
        if action == "create":
            if not request.user.is_authenticated:
                return HttpResponseBadRequest("Login required")
        return redirect(
            resolve_object_type_url(
                "loc",
                loc_type,
                "create" if action == "create" else "list",
                request.POST.get("gameline"),
            )
        )

    def get_context(self):
        game_locations = get_registry("locations").menu(self.request.user)
        context = {
            "objects": game_locations,
        }
        chron_dict = {}
        for chron in list(Chronicle.objects.all()) + [None]:
            # Include polymorphic_ctype for subclass-specific method calls in templates
            chron_dict[chron] = (
                LocationModel.objects.top_level()
                .filter(chronicle=chron)
                .with_polymorphic_ctype()
                .order_by("name")
            )
        context["form"] = LocationCreationForm(user=self.request.user)
        context["chrondict"] = chron_dict
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"

        return context


__all__ = [
    "Http404",
    "redirect",
    "render",
    "View",
    "get_gameline_name",
    "DictView",
    "Chronicle",
    "ObjectType",
    "LocationCreationForm",
    "LocationModel",
    "mage",
    "werewolf",
    "CityCreateView",
    "CityDetailView",
    "CityListView",
    "CityUpdateView",
    "LocationCreateView",
    "LocationDetailView",
    "LocationUpdateView",
]
