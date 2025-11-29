from collections import defaultdict

from core.utils import get_gameline_name
from core.views.generic import DictView
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from game.models import Chronicle, ObjectType
from items.forms.core.item_creation import ItemCreationForm
# Core models
from items.models.core.item import ItemModel
from items.models.core.material import Material
from items.models.core.medium import Medium
from items.models.core.meleeweapon import MeleeWeapon
from items.models.core.rangedweapon import RangedWeapon
from items.models.core.thrownweapon import ThrownWeapon
from items.models.core.weapon import Weapon
# Changeling models
from items.models.changeling.dross import Dross
from items.models.changeling.treasure import Treasure
# Demon models
from items.models.demon.relic import Relic as DemonRelic
# Hunter models
from items.models.hunter.gear import HunterGear
from items.models.hunter.relic import HunterRelic
# Mage models
from items.models.mage.artifact import Artifact
from items.models.mage.charm import Charm
from items.models.mage.grimoire import Grimoire
from items.models.mage.periapt import Periapt
from items.models.mage.sorcerer_artifact import SorcererArtifact
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder
# Mummy models
from items.models.mummy.relic import MummyRelic
from items.models.mummy.ushabti import Ushabti
from items.models.mummy.vessel import Vessel
# Vampire models
from items.models.vampire.artifact import VampireArtifact
from items.models.vampire.bloodstone import Bloodstone
# Werewolf models
from items.models.werewolf.fetish import Fetish
from items.models.werewolf.talen import Talen
# Wraith models
from items.models.wraith.artifact import WraithArtifact
from items.models.wraith.relic import WraithRelic

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


class GenericItemDetailView(DictView):
    model_class = ItemModel
    key_property = "type"
    default_redirect = "items:index"

    @property
    def view_mapping(self):
        from items.views import changeling, demon, hunter, mummy, vampire, wraith

        return {
            # Core
            "item": ItemDetailView,
            "weapon": WeaponDetailView,
            "melee_weapon": MeleeWeaponDetailView,
            "thrown_weapon": ThrownWeaponDetailView,
            "ranged_weapon": RangedWeaponDetailView,
            # Mage
            "wonder": mage.WonderDetailView,
            "charm": mage.CharmDetailView,
            "artifact": mage.ArtifactDetailView,
            "talisman": mage.TalismanDetailView,
            "grimoire": mage.GrimoireDetailView,
            "sorcerer_artifact": mage.SorcererArtifactDetailView,
            "periapt": mage.PeriaptDetailView,
            # Werewolf
            "fetish": werewolf.FetishDetailView,
            "talen": werewolf.TalenDetailView,
            # Vampire
            "vampire_artifact": vampire.VampireArtifactDetailView,
            "bloodstone": vampire.BloodstoneDetailView,
            # Wraith
            "relic": wraith.WraithRelicDetailView,
            "wraith_artifact": wraith.WraithArtifactDetailView,
            # Changeling
            "treasure": changeling.TreasureDetailView,
            "dross": changeling.DrossDetailView,
            # Demon
            "demon_relic": demon.RelicDetailView,
            # Hunter
            "hunter_relic": hunter.HunterRelicDetailView,
            "hunter_gear": hunter.HunterGearDetailView,
            # Mummy
            "mummy_relic": mummy.MummyRelicDetailView,
            "vessel": mummy.VesselDetailView,
            "ushabti": mummy.UshabtiDetailView,
        }


class ItemIndexView(View):
    items = {
        # Core
        "item": ItemModel,
        "weapon": Weapon,
        "melee_weapon": MeleeWeapon,
        "thrown_weapon": ThrownWeapon,
        "ranged_weapon": RangedWeapon,
        "material": Material,
        "medium": Medium,
        # Changeling
        "treasure": Treasure,
        "dross": Dross,
        # Demon
        "demon_relic": DemonRelic,
        # Hunter
        "hunter_relic": HunterRelic,
        "hunter_gear": HunterGear,
        # Mage
        "wonder": Wonder,
        "charm": Charm,
        "artifact": Artifact,
        "talisman": Talisman,
        "grimoire": Grimoire,
        "sorcerer_artifact": SorcererArtifact,
        "periapt": Periapt,
        # Mummy
        "mummy_relic": MummyRelic,
        "vessel": Vessel,
        "ushabti": Ushabti,
        # Vampire
        "vampire_artifact": VampireArtifact,
        "bloodstone": Bloodstone,
        # Werewolf
        "fetish": Fetish,
        "talen": Talen,
        # Wraith
        "wraith_relic": WraithRelic,
        "wraith_artifact": WraithArtifact,
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, "items/index.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context()
        action = request.POST.get("action")
        item_type = request.POST["item_type"]
        obj = ObjectType.objects.get(name=item_type)
        gameline = obj.gameline
        if action == "create":
            if gameline == "wod":
                redi = f"items:create:{item_type}"
            elif gameline == "wta":
                redi = f"items:werewolf:create:{item_type}"
            elif gameline == "mta":
                redi = f"items:mage:create:{item_type}"
            return redirect(redi)
        elif action == "index":
            if gameline == "wod":
                redi = f"items:list:{item_type}"
            elif gameline == "wta":
                redi = f"items:werewolf:list:{item_type}"
            elif gameline == "mta":
                redi = f"items:mage:list:{item_type}"
            return redirect(redi)
        return render(request, "items/index.html", context)

    def get_context(self):
        game_items = ObjectType.objects.filter(type="obj")
        game_items_types = [x.name for x in game_items]
        context = {
            "objects": game_items,
        }

        chron_dict = {}
        for chron in list(Chronicle.objects.all()) + [None]:
            if chron:
                c = ItemModel.objects.for_chronicle(chron).order_by("name")
            else:
                c = ItemModel.objects.filter(chronicle=chron).order_by("name")
            items = [x for x in c if x.type in game_items_types]

            c = ItemModel.objects.filter(
                id__in=[x.id for x in items], chronicle=chron
            ).order_by("name")
            chron_dict[chron] = c

        context["chron_dict"] = chron_dict
        context["form"] = ItemCreationForm(user=self.request.user)
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"

        return context
