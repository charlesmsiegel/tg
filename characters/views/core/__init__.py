from characters.forms.core.character_creation import CharacterCreationForm
from characters.forms.core.group_creation import GroupCreationForm
from characters.models.core import Character, Derangement, Group, Human
from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from characters.models.core.statistic import Statistic
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
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
from characters.models.mage.sphere import Sphere
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.charm import SpiritCharm
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.totem import Totem
# from characters.views.changeling.changeling import ChangelingCharacterCreationView
# from characters.views.changeling.ctdhuman import CtDHumanCharacterCreationView
# from characters.views.changeling.motley import MotleyDetailView
from core.views.generic import DictView
from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect, render
from django.views.generic import ListView
from game.models import Chronicle, ObjectType

from .group import GroupDetailView


class GenericCharacterDetailView(DictView):
    from characters.views import changeling, mage, vampire, werewolf, wraith, demon

    view_mapping = {
        "vtm_human": vampire.VtMHumanCharacterCreationView,
        "vampire": vampire.VampireCharacterCreationView,
        "wta_human": werewolf.WtAHumanCharacterCreationView,
        "werewolf": werewolf.WerewolfCharacterCreationView,
        "spirit_character": werewolf.SpiritDetailView,
        "kinfolk": werewolf.KinfolkCharacterCreationView,
        "fomor": werewolf.FomorCharacterCreationView,
        "fera": werewolf.FeraCharacterCreationView,
        "mta_human": mage.MtAHumanCharacterCreationView,
        "mage": mage.MageCharacterCreationView,
        "companion": mage.CopanionCharacterCreationView,
        "sorcerer": mage.SorcererCharacterCreationView,
        "ctd_human": changeling.CtDHumanCharacterCreationView,
        "changeling": changeling.ChangelingCharacterCreationView,
        "wto_human": wraith.WtOHumanCharacterCreationView,
        "wraith": wraith.WraithCharacterCreationView,
        "dtf_human": demon.DtFHumanCharacterCreationView,
        "demon": demon.DemonCharacterCreationView,
        "thrall": demon.ThrallCharacterCreationView,
        
    }
    model_class = Character
    key_property = "type"
    default_redirect = "characters:index"


class GenericGroupDetailView(DictView):
    from characters.views import changeling, mage, vampire, werewolf, wraith, demon

    view_mapping = {
        "group": GroupDetailView,
        "pack": werewolf.PackDetailView,
        "cabal": mage.CabalDetailView,
        "motley": changeling.MotleyDetailView,
        "coterie": vampire.CoterieDetailView,
        "circle": wraith.CircleDetailView,
        "conclave": demon.ConclaveDetailView,
    }
    model_class = Group
    key_property = "type"
    default_redirect = "characters:index"


class CharacterIndexView(ListView):
    model = Character
    template_name = "characters/index.html"

    chars = {
        "human": Human,
        "statistic": Statistic,
        "specialty": Specialty,
        "meritflaw": MeritFlaw,
        "group": Group,
        "derangement": Derangement,
        "character": Character,
        "archetype": Archetype,
        "ability": Ability,
        "vtm_human": VtMHuman,
        "totem": Totem,
        "spirit": SpiritCharacter,
        "spirit_charm": SpiritCharm,
        "sphere": Sphere,
        "rote": Rote,
        "resonance": Resonance,
        "instrument": Instrument,
        "practice": Practice,
        "specialized_practice": SpecializedPractice,
        "corrupted_practice": CorruptedPractice,
        "tenet": Tenet,
        "paradigm": Paradigm,
        "mage_faction": MageFaction,
        "effect": Effect,
        "mage": Mage,
        "mta_human": MtAHuman,
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

        obj = ObjectType.objects.get(name=type_name)
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
                    self.get_queryset().filter(
                        chronicle=chron, status__in=["Un", "Sub", "App"], npc=False
                    ).visible()
                ),
                "retired": list(
                    self.get_queryset().filter(
                        chronicle=chron, status="Ret"
                    ).visible()
                ),
                "deceased": list(
                    self.get_queryset().filter(
                        chronicle=chron, status="Dec"
                    ).visible()
                ),
                "npc": list(
                    self.get_queryset().filter(chronicle=chron, npc=True).visible()
                ),
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
