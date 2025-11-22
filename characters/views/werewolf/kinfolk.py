from characters.forms.werewolf.kinfolk import KinfolkCreationForm
from characters.models.core.merit_flaw_block import MeritFlawRating
from characters.models.werewolf.kinfolk import Kinfolk
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
)
from characters.views.werewolf.wtahuman import (
    WtAHumanAbilityView,
    WtAHumanAlliesView,
    WtAHumanExtrasView,
    WtAHumanFreebieFormPopulationView,
    WtAHumanFreebiesView,
    WtAHumanLanguagesView,
    WtAHumanSpecialtiesView,
)
from core.mixins import ViewPermissionMixin, EditPermissionMixin, SpendFreebiesPermissionMixin, SpendXPPermissionMixin
from core.views.message_mixin import MessageMixin
from core.mixins import ViewPermissionMixin, EditPermissionMixin, SpendFreebiesPermissionMixin, SpendXPPermissionMixin, ApprovedUserContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, FormView, UpdateView
from game.models import ObjectType


class KinfolkDetailView(ApprovedUserContextMixin, ViewPermissionMixin, DetailView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialties = {}
        for attribute in self.object.get_attributes():
            specialties[attribute] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=attribute)]
            )
        for ability in self.object.get_abilities():
            specialties[ability] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=ability)]
            )
        for key, value in specialties.items():
            context[f"{key}_spec"] = value

        context["merits_and_flaws"] = MeritFlawRating.objects.order_by(
            "mf__name"
        ).filter(character=self.object)
        all_gifts = list(context["object"].gifts.all())
        row_length = 3
        all_gifts = [
            all_gifts[i : i + row_length] for i in range(0, len(all_gifts), row_length)
        ]
        context["gifts"] = all_gifts
        return context


class KinfolkCreateView(MessageMixin, CreateView):
    model = Kinfolk
    success_message = "Kinfolk created successfully."
    error_message = "Error creating kinfolk."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "leadership",
        "primal_urge",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "law",
        "occult",
        "rituals",
        "technology",
        "breed",
        "tribe",
        "relation",
        "gifts",
        "gnosis",
        "fetishes_owned",
        "glory",
        "temporary_glory",
        "wisdom",
        "temporary_wisdom",
        "honor",
        "temporary_honor",
    ]
    template_name = "characters/werewolf/kinfolk/form.html"


class KinfolkUpdateView(ApprovedUserContextMixin, EditPermissionMixin, UpdateView):
    model = Kinfolk
    success_message = "Kinfolk updated successfully."
    error_message = "Error updating kinfolk."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "leadership",
        "primal_urge",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "law",
        "occult",
        "rituals",
        "technology",
        "breed",
        "tribe",
        "relation",
        "gifts",
        "gnosis",
        "fetishes_owned",
        "glory",
        "temporary_glory",
        "wisdom",
        "temporary_wisdom",
        "honor",
        "temporary_honor",
    ]
    template_name = "characters/werewolf/kinfolk/form.html"


class KinfolkBasicsView(LoginRequiredMixin, FormView):
    form_class = KinfolkCreationForm
    template_name = "characters/werewolf/kinfolk/basics.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = False
        if self.request.user.profile.is_st():
            context["storyteller"] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class KinfolkAttributeView(ApprovedUserContextMixin, HumanAttributeView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class KinfolkAbilityView(WtAHumanAbilityView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkBackgroundsView(HumanBackgroundsView):
    # TODO: Tribal Restrictions?
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkExtrasView(WtAHumanExtrasView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkFreebiesView(WtAHumanFreebiesView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Kinfolk


class KinfolkLanguagesView(WtAHumanLanguagesView):
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkAlliesView(GenericBackgroundView):
    primary_object_class = Kinfolk
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkSpecialtiesView(WtAHumanSpecialtiesView):
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: KinfolkAttributeView,
        2: KinfolkAbilityView,
        3: KinfolkBackgroundsView,
        4: KinfolkExtrasView,
        5: KinfolkFreebiesView,
        6: KinfolkLanguagesView,
        7: KinfolkAlliesView,
        8: KinfolkSpecialtiesView,
    }
    model_class = Kinfolk
    key_property = "creation_status"
    default_redirect = KinfolkDetailView
