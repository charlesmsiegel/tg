from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.werewolf.drone import DroneCreationForm
from characters.models.werewolf.drone import Drone
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import HumanAttributeView, HumanCharacterCreationView
from characters.views.werewolf.wtahuman import (
    WtAHumanAbilityView,
    WtAHumanExtrasView,
    WtAHumanFreebieFormPopulationView,
    WtAHumanFreebiesView,
    WtAHumanLanguagesView,
    WtAHumanSpecialtiesView,
)
from core.mixins import EditPermissionMixin, ViewPermissionMixin
from core.permissions import Permission, PermissionManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView


class DroneDetailView(ViewPermissionMixin, DetailView):
    model = Drone
    template_name = "characters/werewolf/drone/detail.html"


class DroneUpdateView(EditPermissionMixin, UpdateView):
    model = Drone
    success_message = "Drone updated successfully."
    error_message = "Error updating drone."
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
        "bane_name",
        "bane_type",
        "rage",
        "gnosis",
        "willpower_per_turn",
    ]
    template_name = "characters/werewolf/drone/form.html"

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedHumanEditForm.
        STs and admins get full access via the default form.
        """
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )
        if has_full_edit:
            return super().get_form_class()
        else:
            return LimitedHumanEditForm


class DroneBasicsView(LoginRequiredMixin, FormView):
    form_class = DroneCreationForm
    template_name = "characters/werewolf/drone/basics.html"

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


class DroneAttributeView(HumanAttributeView):
    model = Drone
    template_name = "characters/werewolf/drone/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class DroneAbilityView(WtAHumanAbilityView):
    model = Drone
    template_name = "characters/werewolf/drone/chargen.html"


class DroneBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/drone/chargen.html"


class DroneExtrasView(WtAHumanExtrasView):
    model = Drone
    template_name = "characters/werewolf/drone/chargen.html"


class DroneFreebiesView(WtAHumanFreebiesView):
    model = Drone
    template_name = "characters/werewolf/drone/chargen.html"


class DroneFreebieFormPopulationView(WtAHumanFreebieFormPopulationView):
    primary_class = Drone


class DroneLanguagesView(WtAHumanLanguagesView):
    template_name = "characters/werewolf/drone/chargen.html"


class DroneSpecialtiesView(WtAHumanSpecialtiesView):
    template_name = "characters/werewolf/drone/chargen.html"


class DroneCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: DroneAttributeView,
        2: DroneAbilityView,
        3: DroneBackgroundsView,
        4: DroneExtrasView,
        5: DroneFreebiesView,
        6: DroneLanguagesView,
        7: DroneSpecialtiesView,
    }
    model_class = Drone
    key_property = "creation_status"
    default_redirect = DroneDetailView
