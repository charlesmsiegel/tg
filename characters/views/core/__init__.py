from characters.forms.core.character_creation import CharacterCreationForm
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
from characters.views.changeling.changeling import ChangelingCharacterCreationView
from characters.views.changeling.ctdhuman import CtDHumanCharacterCreationView
from characters.views.changeling.motley import MotleyDetailView
from core.views.generic import DictView
from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect, render
from django.views.generic import ListView
from game.models import Chronicle, ObjectType

from .group import GroupDetailView


class GenericCharacterDetailView(DictView):
    from characters.views import changeling, mage, vampire, werewolf, wraith

    view_mapping = {
        "spirit_character": werewolf.SpiritDetailView,
        "mta_human": mage.MtAHumanCharacterCreationView,
        "mage": mage.MageCharacterCreationView,
        "vtm_human": vampire.VtMHumanCharacterCreationView,
        "wto_human": wraith.WtOHumanCharacterCreationView,
        "wta_human": werewolf.WtAHumanCharacterCreationView,
        "kinfolk": werewolf.KinfolkCharacterCreationView,
        "werewolf": werewolf.WerewolfCharacterCreationView,
        "fomor": werewolf.FomorCharacterCreationView,
        "changeling": ChangelingCharacterCreationView,
        "ctd_human": CtDHumanCharacterCreationView,
        "companion": mage.CopanionCharacterCreationView,
        "sorcerer": mage.SorcererCharacterCreationView,
    }
    model_class = Character
    key_property = "type"
    default_redirect = "characters:index wod"


class GenericGroupDetailView(DictView):
    from characters.views import changeling, mage, vampire, werewolf, wraith

    view_mapping = {
        "group": GroupDetailView,
        "cabal": mage.CabalDetailView,
        "pack": werewolf.PackDetailView,
        "motley": MotleyDetailView,
    }
    model_class = Group
    key_property = "type"
    default_redirect = "characters:index wod"


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
        CharacterGroup = Character.group_set.through

        # Subquery to get the first group id for each character
        first_group_id = Subquery(
            CharacterGroup.objects.filter(character_id=OuterRef("pk"))
            .order_by(
                "group_id"
            )  # Assuming ordering by 'group_id', adjust if different
            .values("group_id")[:1]
        )

        # Annotating the queryset with the first group id
        characters = (
            Character.objects.annotate(first_group_id=first_group_id)
            .select_related("chronicle")
            .order_by("chronicle__id", "-first_group_id", "name")
        )

        return characters

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        char_type = request.POST["char_type"]
        obj = ObjectType.objects.get(name=char_type)
        gameline = obj.gameline
        if action == "create":
            if gameline == "wod":
                redi = f"characters:create:{char_type}"
            elif gameline == "vtm":
                redi = f"characters:vampire:create:{char_type}"
            elif gameline == "wta":
                redi = f"characters:werewolf:create:{char_type}"
            elif gameline == "mta":
                redi = f"characters:mage:create:{char_type}"
            elif gameline == "wto":
                redi = f"characters:wraith:create:{char_type}"
            elif gameline == "ctd":
                redi = f"characters:changeling:create:{char_type}"
            return redirect(redi)
        context = self.get_context_data()
        return render(request, "characters/charlist.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Characters"
        context["button_include"] = True
        context["form"] = CharacterCreationForm(user=self.request.user)
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"

        # Create chron_dict similar to items and locations
        chron_dict = {}
        for chron in list(Chronicle.objects.all()) + [None]:
            chron_dict[chron] = {
                "active": [
                    char
                    for char in self.get_queryset().filter(
                        chronicle=chron, status__in=["Un", "Sub", "App"], npc=False
                    )
                    if char.display
                ],
                "retired": [
                    char
                    for char in self.get_queryset().filter(
                        chronicle=chron, status="Ret"
                    )
                    if char.display
                ],
                "deceased": [
                    char
                    for char in self.get_queryset().filter(
                        chronicle=chron, status="Dec"
                    )
                    if char.display
                ],
                "npc": [
                    char
                    for char in self.get_queryset().filter(chronicle=chron, npc=True)
                    if char.display
                ],
            }

        context["chron_dict"] = chron_dict
        return context


class RetiredCharacterIndex(ListView):
    model = Character
    template_name = "characters/charlist.html"

    def get_queryset(self):
        CharacterGroup = Character.group_set.through

        # Subquery to get the first group id for each character
        first_group_id = Subquery(
            CharacterGroup.objects.filter(character_id=OuterRef("pk"))
            .order_by(
                "group_id"
            )  # Assuming ordering by 'group_id', adjust if different
            .values("group_id")[:1]
        )

        # Annotating the queryset with the first group id
        characters = (
            Human.objects.filter(status="Ret")
            .annotate(first_group_id=first_group_id)
            .select_related("chronicle")
            .order_by("chronicle__id", "-first_group_id", "name")
        )

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
        CharacterGroup = Character.group_set.through

        # Subquery to get the first group id for each character
        first_group_id = Subquery(
            CharacterGroup.objects.filter(character_id=OuterRef("pk"))
            .order_by(
                "group_id"
            )  # Assuming ordering by 'group_id', adjust if different
            .values("group_id")[:1]
        )

        # Annotating the queryset with the first group id
        characters = (
            Human.objects.filter(status="Dec")
            .annotate(first_group_id=first_group_id)
            .select_related("chronicle")
            .order_by("chronicle__id", "-first_group_id", "name")
        )

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
        CharacterGroup = Character.group_set.through

        # Subquery to get the first group id for each character
        first_group_id = Subquery(
            CharacterGroup.objects.filter(character_id=OuterRef("pk"))
            .order_by(
                "group_id"
            )  # Assuming ordering by 'group_id', adjust if different
            .values("group_id")[:1]
        )

        # Annotating the queryset with the first group id
        characters = (
            Human.objects.filter(npc=True)
            .annotate(first_group_id=first_group_id)
            .select_related("chronicle")
            .order_by("chronicle__id", "-first_group_id", "name")
        )

        chron_pk = self.kwargs.get("pk")
        if chron_pk is not None:
            characters = characters.filter(chronicle__id=chron_pk)

        return characters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "NPCs"
        context["header"] = "wod_heading"
        return context
