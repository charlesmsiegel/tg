from core.utils import get_gameline_name, level_name, tree_sort
from core.views.generic import DictView
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from game.models import Chronicle, ObjectType
from locations.forms.core.location_creation import LocationCreationForm
from locations.models.core.city import City
from locations.models.core.location import LocationModel
from locations.models.mage.chantry import Chantry
from locations.models.mage.library import Library
from locations.models.mage.node import Node
from locations.models.mage.reality_zone import RealityZone
from locations.models.mage.realm import HorizonRealm
from locations.models.mage.sanctum import Sanctum
from locations.models.mage.sector import Sector
from locations.models.werewolf.caern import Caern
from locations.views import mage, werewolf

from .city import CityCreateView, CityDetailView, CityUpdateView
from .location import LocationCreateView, LocationDetailView, LocationUpdateView


class GenericLocationDetailView(DictView):
    view_mapping = {
        "location": LocationDetailView,
        "city": CityDetailView,
        "node": mage.NodeDetailView,
        "sector": mage.SectorDetailView,
        "library": mage.LibraryDetailView,
        "horizon_realm": mage.RealmDetailView,
        "caern": werewolf.CaernDetailView,
        "sanctum": mage.SanctumDetailView,
        "chantry": mage.ChantryCreationView,
    }

    model_class = LocationModel
    key_property = "type"
    default_redirect = "locations:index"


class LocationIndexView(View):
    locs = {
        "location": LocationModel,
        "city": City,
        "node": Node,
        "sector": Sector,
        "library": Library,
        "horizon_realm": HorizonRealm,
        "caern": Caern,
        "chantry": Chantry,
        "sanctum": Sanctum,
        "reality_zone": RealityZone,
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, "locations/index.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context()
        action = request.POST.get("action")
        loc_type = request.POST["loc_type"]
        obj = ObjectType.objects.get(name=loc_type)
        gameline = obj.gameline
        if action == "create":
            if gameline == "wod":
                redi = f"locations:create:{loc_type}"
            elif gameline == "wta":
                redi = f"locations:werewolf:create:{loc_type}"
            elif gameline == "mta":
                redi = f"locations:mage:create:{loc_type}"
            return redirect(redi)
        elif action == "index":
            if gameline == "wod":
                redi = f"locations:list:{loc_type}"
            elif gameline == "wta":
                redi = f"locations:werewolf:list:{loc_type}"
            elif gameline == "mta":
                redi = f"locations:mage:list:{loc_type}"
            return redirect(redi)
        return render(request, "locations/index.html", context)

    def get_context(self):
        game_locations = ObjectType.objects.filter(type="loc")
        game_location_types = [x.name for x in game_locations]
        context = {
            "objects": game_locations,
        }
        chron_dict = {}
        for chron in list(Chronicle.objects.all()) + [None]:
            chron_dict[chron] = LocationModel.objects.filter(
                chronicle=chron, parent=None
            ).order_by("name")
        context["form"] = LocationCreationForm(user=self.request.user)
        context["chrondict"] = chron_dict
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"

        return context
