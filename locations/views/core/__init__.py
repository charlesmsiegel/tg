from core.utils import get_gameline_name, level_name, tree_sort
from core.views.generic import DictView
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from game.models import Chronicle, ObjectType
from locations.forms.core.location_creation import LocationCreationForm

# Changeling models
from locations.models.changeling.dream_realm import DreamRealm
from locations.models.changeling.freehold import Freehold
from locations.models.changeling.holding import Holding
from locations.models.changeling.trod import Trod

# Core models
from locations.models.core.city import City
from locations.models.core.location import LocationModel

# Demon models
from locations.models.demon.bastion import Bastion
from locations.models.demon.reliquary import Reliquary

# Hunter models
from locations.models.hunter.huntingground import HuntingGround
from locations.models.hunter.safehouse import Safehouse

# Mage models
from locations.models.mage.chantry import Chantry
from locations.models.mage.demesne import Demesne
from locations.models.mage.library import Library
from locations.models.mage.node import Node
from locations.models.mage.paradox_realm import ParadoxRealm
from locations.models.mage.reality_zone import RealityZone
from locations.models.mage.realm import HorizonRealm
from locations.models.mage.sanctum import Sanctum
from locations.models.mage.sector import Sector

# Mummy models
from locations.models.mummy.cult_temple import CultTemple
from locations.models.mummy.sanctuary import UndergroundSanctuary
from locations.models.mummy.tomb import Tomb

# Vampire models
from locations.models.vampire.barrens import Barrens
from locations.models.vampire.chantry import TremereChantry
from locations.models.vampire.domain import Domain
from locations.models.vampire.elysium import Elysium
from locations.models.vampire.haven import Haven
from locations.models.vampire.rack import Rack

# Werewolf models
from locations.models.werewolf.caern import Caern

# Wraith models
from locations.models.wraith.byway import Byway
from locations.models.wraith.citadel import Citadel
from locations.models.wraith.freehold import WraithFreehold
from locations.models.wraith.haunt import Haunt
from locations.models.wraith.necropolis import Necropolis
from locations.models.wraith.nihil import Nihil
from locations.views import mage, werewolf

from .city import CityCreateView, CityDetailView, CityListView, CityUpdateView
from .location import LocationCreateView, LocationDetailView, LocationUpdateView


class GenericLocationDetailView(DictView):
    model_class = LocationModel
    key_property = "type"
    default_redirect = "locations:index"

    @property
    def view_mapping(self):
        from locations.views import changeling, demon, hunter, mummy, vampire, wraith

        return {
            # Core
            "location": LocationDetailView,
            "city": CityDetailView,
            # Mage
            "node": mage.NodeDetailView,
            "sector": mage.SectorDetailView,
            "library": mage.LibraryDetailView,
            "horizon_realm": mage.RealmDetailView,
            "paradox_realm": mage.ParadoxRealmDetailView,
            "sanctum": mage.SanctumDetailView,
            "chantry": mage.ChantryDetailView,
            "reality_zone": mage.RealityZoneDetailView,
            "demesne": mage.DemesneDetailView,
            # Werewolf
            "caern": werewolf.CaernDetailView,
            # Vampire
            "haven": vampire.HavenDetailView,
            "domain": vampire.DomainDetailView,
            "elysium": vampire.ElysiumDetailView,
            "rack": vampire.RackDetailView,
            "tremere_chantry": vampire.TremereChantryDetailView,
            "barrens": vampire.BarrensDetailView,
            # Wraith
            "haunt": wraith.HauntDetailView,
            "necropolis": wraith.NecropolisDetailView,
            "citadel": wraith.CitadelDetailView,
            "nihil": wraith.NihilDetailView,
            "byway": wraith.BywayDetailView,
            "wraith_freehold": wraith.WraithFreeholdDetailView,
            # Changeling
            "freehold": changeling.FreeholdDetailView,
            "dream_realm": changeling.DreamRealmDetailView,
            "trod": changeling.TrodDetailView,
            "holding": changeling.HoldingDetailView,
            # Demon
            "bastion": demon.BastionDetailView,
            "reliquary": demon.ReliquaryDetailView,
            # Hunter
            "hunting_ground": hunter.HuntingGroundDetailView,
            "safehouse": hunter.SafehouseDetailView,
            # Mummy
            "tomb": mummy.TombDetailView,
            "cult_temple": mummy.CultTempleDetailView,
            "underground_sanctuary": mummy.UndergroundSanctuaryDetailView,
        }


class LocationIndexView(View):
    locs = {
        # Core
        "location": LocationModel,
        "city": City,
        # Changeling
        "freehold": Freehold,
        "dream_realm": DreamRealm,
        "trod": Trod,
        "holding": Holding,
        # Demon
        "bastion": Bastion,
        "reliquary": Reliquary,
        # Hunter
        "hunting_ground": HuntingGround,
        "safehouse": Safehouse,
        # Mage
        "node": Node,
        "sector": Sector,
        "library": Library,
        "horizon_realm": HorizonRealm,
        "paradox_realm": ParadoxRealm,
        "chantry": Chantry,
        "sanctum": Sanctum,
        "reality_zone": RealityZone,
        "demesne": Demesne,
        # Mummy
        "tomb": Tomb,
        "cult_temple": CultTemple,
        "underground_sanctuary": UndergroundSanctuary,
        # Vampire
        "haven": Haven,
        "domain": Domain,
        "elysium": Elysium,
        "rack": Rack,
        "tremere_chantry": TremereChantry,
        "barrens": Barrens,
        # Werewolf
        "caern": Caern,
        # Wraith
        "haunt": Haunt,
        "necropolis": Necropolis,
        "citadel": Citadel,
        "nihil": Nihil,
        "byway": Byway,
        "wraith_freehold": WraithFreehold,
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, "locations/index.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context()
        action = request.POST.get("action")
        loc_type = request.POST["loc_type"]
        obj, _ = ObjectType.objects.get_or_create(
            name=loc_type, defaults={"type": "loc", "gameline": "wod"}
        )
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
