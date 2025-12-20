from characters.forms.core.character_creation import CharacterCreationForm
from characters.forms.core.group_creation import GroupCreationForm

# Changeling models
from characters.models.changeling.autumn_person import AutumnPerson
from characters.models.changeling.cantrip import Cantrip
from characters.models.changeling.changeling import Changeling
from characters.models.changeling.chimera import Chimera
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.changeling.house import House as ChangelingHouse
from characters.models.changeling.house_faction import HouseFaction
from characters.models.changeling.inanimae import Inanimae
from characters.models.changeling.kith import Kith
from characters.models.changeling.legacy import Legacy
from characters.models.changeling.motley import Motley
from characters.models.changeling.nunnehi import Nunnehi

# Core models
from characters.models.core import Character, Derangement, Group, Human
from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from characters.models.core.statistic import Statistic

# Demon models
from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from characters.models.demon.conclave import Conclave
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.earthbound import Earthbound
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.pact import Pact
from characters.models.demon.ritual import Ritual as DemonRitual
from characters.models.demon.thrall import Thrall
from characters.models.demon.visage import Visage

# Hunter models
from characters.models.hunter.creed import Creed
from characters.models.hunter.edge import Edge
from characters.models.hunter.htrhuman import HtRHuman
from characters.models.hunter.hunter import Hunter
from characters.models.hunter.organization import HunterOrganization

# Mage models
from characters.models.mage.cabal import Cabal
from characters.models.mage.companion import Advantage, Companion
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.focus import (
    CorruptedPractice,
    Instrument,
    Paradigm,
    Practice,
    SpecializedPractice,
    Tenet,
)
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual, Sorcerer
from characters.models.mage.sphere import Sphere

# Mummy models
from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mtr_human import MtRHuman
from characters.models.mummy.mummy import Mummy
from characters.models.mummy.mummy_title import MummyTitle

# Vampire models
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.coterie import Coterie
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.path import Path as VampirePath
from characters.models.vampire.revenant import Revenant, RevenantFamily
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.title import VampireTitle
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman

# Werewolf models
from characters.models.werewolf.ajaba import Ajaba
from characters.models.werewolf.ananasi import Ananasi
from characters.models.werewolf.bastet import Bastet
from characters.models.werewolf.battlescar import BattleScar
from characters.models.werewolf.camp import Camp
from characters.models.werewolf.charm import SpiritCharm
from characters.models.werewolf.corax import Corax
from characters.models.werewolf.drone import Drone
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.fomoripower import FomoriPower
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift
from characters.models.werewolf.grondr import Grondr
from characters.models.werewolf.gurahl import Gurahl
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.kitsune import Kitsune
from characters.models.werewolf.mokole import Mokole
from characters.models.werewolf.nagah import Nagah
from characters.models.werewolf.nuwisha import Nuwisha
from characters.models.werewolf.pack import Pack
from characters.models.werewolf.ratkin import Ratkin
from characters.models.werewolf.renownincident import RenownIncident
from characters.models.werewolf.rite import Rite
from characters.models.werewolf.rokea import Rokea
from characters.models.werewolf.septposition import SeptPosition
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.totem import Totem
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman

# Wraith models
from characters.models.wraith.arcanos import Arcanos
from characters.models.wraith.circle import Circle
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.guild import Guild
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import Wraith
from characters.models.wraith.wtohuman import WtOHuman
from core.views.generic import DictView
from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect, render
from django.views.generic import ListView
from game.models import Chronicle, ObjectType

from .group import GroupDetailView


class GenericCharacterDetailView(DictView):
    model_class = Character
    key_property = "type"
    default_redirect = "characters:index"

    @property
    def view_mapping(self):
        from characters.views import (
            changeling,
            demon,
            hunter,
            mage,
            mummy,
            vampire,
            werewolf,
            wraith,
        )

        return {
            # Vampire
            "vtm_human": vampire.VtMHumanCharacterCreationView,
            "vampire": vampire.VampireCharacterCreationView,
            "ghoul": vampire.GhoulCharacterCreationView,
            "revenant": vampire.RevenantDetailView,
            # Werewolf
            "wta_human": werewolf.WtAHumanCharacterCreationView,
            "werewolf": werewolf.WerewolfCharacterCreationView,
            "spirit_character": werewolf.SpiritDetailView,
            "kinfolk": werewolf.KinfolkCharacterCreationView,
            "fomor": werewolf.FomorCharacterCreationView,
            "drone": werewolf.DroneCharacterCreationView,
            # Fera (all shifter types use the same view)
            "fera": werewolf.FeraCharacterCreationView,
            "ajaba": werewolf.FeraCharacterCreationView,
            "ananasi": werewolf.FeraCharacterCreationView,
            "bastet": werewolf.FeraCharacterCreationView,
            "corax": werewolf.FeraCharacterCreationView,
            "grondr": werewolf.FeraCharacterCreationView,
            "gurahl": werewolf.FeraCharacterCreationView,
            "kitsune": werewolf.FeraCharacterCreationView,
            "mokole": werewolf.FeraCharacterCreationView,
            "nagah": werewolf.FeraCharacterCreationView,
            "nuwisha": werewolf.FeraCharacterCreationView,
            "ratkin": werewolf.FeraCharacterCreationView,
            "rokea": werewolf.FeraCharacterCreationView,
            # Mage
            "mta_human": mage.MtAHumanCharacterCreationView,
            "mage": mage.MageCharacterCreationView,
            "companion": mage.CopanionCharacterCreationView,
            "sorcerer": mage.SorcererCharacterCreationView,
            # Changeling
            "ctd_human": changeling.CtDHumanCharacterCreationView,
            "changeling": changeling.ChangelingCharacterCreationView,
            "autumn_person": changeling.AutumnPersonDetailView,
            "inanimae": changeling.InanimaeDetailView,
            "nunnehi": changeling.NunnehiDetailView,
            # Wraith
            "wto_human": wraith.WtOHumanCharacterCreationView,
            "wraith": wraith.WraithCharacterCreationView,
            # Demon
            "dtf_human": demon.DtFHumanCharacterCreationView,
            "demon": demon.DemonCharacterCreationView,
            "thrall": demon.ThrallCharacterCreationView,
            "earthbound": demon.EarthboundDetailView,
            # Hunter
            "htr_human": hunter.HtRHumanDetailView,
            "hunter": hunter.HunterDetailView,
            # Mummy
            "mtr_human": mummy.MtRHumanDetailView,
            "mummy": mummy.MummyDetailView,
        }


class GenericGroupDetailView(DictView):
    model_class = Group
    key_property = "type"
    default_redirect = "characters:index"

    @property
    def view_mapping(self):
        from characters.views import changeling, demon, mage, vampire, werewolf, wraith

        return {
            "group": GroupDetailView,
            "pack": werewolf.PackDetailView,
            "cabal": mage.CabalDetailView,
            "motley": changeling.MotleyDetailView,
            "coterie": vampire.CoterieDetailView,
            "circle": wraith.CircleDetailView,
            "conclave": demon.ConclaveDetailView,
        }


class CharacterIndexView(ListView):
    model = Character
    template_name = "characters/index.html"

    chars = {
        # Core
        "human": Human,
        "character": Character,
        "group": Group,
        "statistic": Statistic,
        "attribute": Attribute,
        "ability": Ability,
        "background": Background,
        "specialty": Specialty,
        "meritflaw": MeritFlaw,
        "derangement": Derangement,
        "archetype": Archetype,
        # Changeling
        "ctd_human": CtDHuman,
        "changeling": Changeling,
        "autumn_person": AutumnPerson,
        "inanimae": Inanimae,
        "nunnehi": Nunnehi,
        "motley": Motley,
        "kith": Kith,
        "house": ChangelingHouse,
        "house_faction": HouseFaction,
        "legacy": Legacy,
        "cantrip": Cantrip,
        "chimera": Chimera,
        # Demon
        "dtf_human": DtFHuman,
        "demon": Demon,
        "earthbound": Earthbound,
        "thrall": Thrall,
        "conclave": Conclave,
        "demon_faction": DemonFaction,
        "demon_house": DemonHouse,
        "lore": Lore,
        "visage": Visage,
        "pact": Pact,
        "demon_ritual": DemonRitual,
        "apocalyptic_form_trait": ApocalypticFormTrait,
        # Hunter
        "htr_human": HtRHuman,
        "hunter": Hunter,
        "creed": Creed,
        "edge": Edge,
        "hunter_organization": HunterOrganization,
        # Mage
        "mta_human": MtAHuman,
        "mage": Mage,
        "sorcerer": Sorcerer,
        "companion": Companion,
        "cabal": Cabal,
        "mage_faction": MageFaction,
        "sorcerer_fellowship": SorcererFellowship,
        "sphere": Sphere,
        "rote": Rote,
        "effect": Effect,
        "resonance": Resonance,
        "paradigm": Paradigm,
        "practice": Practice,
        "specialized_practice": SpecializedPractice,
        "corrupted_practice": CorruptedPractice,
        "instrument": Instrument,
        "tenet": Tenet,
        "advantage": Advantage,
        "linear_magic_path": LinearMagicPath,
        "linear_magic_ritual": LinearMagicRitual,
        # Mummy
        "mtr_human": MtRHuman,
        "mummy": Mummy,
        "dynasty": Dynasty,
        "mummy_title": MummyTitle,
        # Vampire
        "vtm_human": VtMHuman,
        "vampire": Vampire,
        "ghoul": Ghoul,
        "revenant": Revenant,
        "coterie": Coterie,
        "vampire_clan": VampireClan,
        "vampire_sect": VampireSect,
        "vampire_title": VampireTitle,
        "vampire_path": VampirePath,
        "discipline": Discipline,
        "revenant_family": RevenantFamily,
        # Werewolf
        "wta_human": WtAHuman,
        "werewolf": Werewolf,
        "kinfolk": Kinfolk,
        "fomor": Fomor,
        "drone": Drone,
        "spirit_character": SpiritCharacter,
        "pack": Pack,
        # Fera
        "fera": Fera,
        "ajaba": Ajaba,
        "ananasi": Ananasi,
        "bastet": Bastet,
        "corax": Corax,
        "grondr": Grondr,
        "gurahl": Gurahl,
        "kitsune": Kitsune,
        "mokole": Mokole,
        "nagah": Nagah,
        "nuwisha": Nuwisha,
        "ratkin": Ratkin,
        "rokea": Rokea,
        # Werewolf mechanics
        "tribe": Tribe,
        "camp": Camp,
        "gift": Gift,
        "rite": Rite,
        "totem": Totem,
        "spirit_charm": SpiritCharm,
        "fomori_power": FomoriPower,
        "battle_scar": BattleScar,
        "renown_incident": RenownIncident,
        "sept_position": SeptPosition,
        # Wraith
        "wto_human": WtOHuman,
        "wraith": Wraith,
        "circle": Circle,
        "wraith_faction": WraithFaction,
        "guild": Guild,
        "arcanos": Arcanos,
        "thorn": Thorn,
        "shadow_archetype": ShadowArchetype,
    }

    def get_queryset(self):
        return Character.objects.with_group_ordering()

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        # Determine if this is a character or group creation
        if "char_type" in request.POST:
            type_name = request.POST["char_type"]
        elif "group_type" in request.POST:
            type_name = request.POST["group_type"]
        else:
            context = self.get_context_data()
            return render(request, "characters/index.html", context)

        obj, _ = ObjectType.objects.get_or_create(
            name=type_name, defaults={"type": "char", "gameline": "wod"}
        )
        gameline = obj.gameline

        if action == "create" or action == "create_group":
            if gameline == "wod":
                redi = f"characters:create:{type_name}"
            elif gameline == "vtm":
                redi = f"characters:vampire:create:{type_name}"
            elif gameline == "wta":
                redi = f"characters:werewolf:create:{type_name}"
            elif gameline == "mta":
                redi = f"characters:mage:create:{type_name}"
            elif gameline == "wto":
                redi = f"characters:wraith:create:{type_name}"
            elif gameline == "ctd":
                redi = f"characters:changeling:create:{type_name}"
            return redirect(redi)

        context = self.get_context_data()
        return render(request, "characters/index.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Characters"
        context["button_include"] = True
        context["form"] = CharacterCreationForm(user=self.request.user)
        context["group_form"] = GroupCreationForm(user=self.request.user)
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"

        # Create chron_dict similar to items and locations
        chron_dict = {}
        for chron in list(Chronicle.objects.all()) + [None]:
            chron_dict[chron] = {
                "active": list(
                    self.get_queryset()
                    .filter(chronicle=chron, status__in=["Un", "Sub", "App"], npc=False)
                    .visible()
                ),
                "retired": list(
                    self.get_queryset().filter(chronicle=chron, status="Ret").visible()
                ),
                "deceased": list(
                    self.get_queryset().filter(chronicle=chron, status="Dec").visible()
                ),
                "npc": list(self.get_queryset().filter(chronicle=chron, npc=True).visible()),
            }

        context["chron_dict"] = chron_dict
        return context


class RetiredCharacterIndex(ListView):
    model = Character
    template_name = "characters/charlist.html"

    def get_queryset(self):
        characters = Human.objects.retired().with_group_ordering()

        chron_pk = self.kwargs.get("pk")
        if chron_pk is not None:
            characters = characters.filter(chronicle__id=chron_pk)

        return characters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Retired Characters"
        context["header"] = "wod_heading"
        return context


class DeceasedCharacterIndex(ListView):
    model = Character
    template_name = "characters/charlist.html"

    def get_queryset(self):
        characters = Human.objects.deceased().with_group_ordering()

        chron_pk = self.kwargs.get("pk")
        if chron_pk is not None:
            characters = characters.filter(chronicle__id=chron_pk)

        return characters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Deceased Characters"
        context["header"] = "wod_heading"
        return context


class NPCCharacterIndex(ListView):
    model = Character
    template_name = "characters/charlist.html"

    def get_queryset(self):
        characters = Human.objects.npcs().with_group_ordering()

        chron_pk = self.kwargs.get("pk")
        if chron_pk is not None:
            characters = characters.filter(chronicle__id=chron_pk)

        return characters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "NPCs"
        context["header"] = "wod_heading"
        return context
