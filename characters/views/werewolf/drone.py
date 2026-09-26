from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.crud_fields import DRONE_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.werewolf.drone import DroneCreationForm
from characters.models.werewolf.drone import Drone
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.werewolf.wtahuman import (
    WtAHumanAbilityView,
    WtAHumanExtrasView,
    WtAHumanFreebiesView,
)
from core.mixins import (
    EditPermissionMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
)
from core.permissions import PermissionManager


class DroneDetailView(HumanDetailView):
    model = Drone
    template_name = "characters/werewolf/drone/detail.html"


class DroneUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Drone
    success_message = "Drone updated successfully."
    error_message = "Error updating drone."
    fields = DRONE_UPDATE_FIELDS
    template_name = "characters/werewolf/drone/form.html"

    limited_form_class = LimitedHumanEditForm


class DroneBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = DroneCreationForm
    template_name = "characters/werewolf/drone/basics.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["storyteller"] = PermissionManager.user_can_manage_creation(
            self.request.user, context["form"], request=self.request
        )
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


class DroneLanguagesView(HumanLanguagesView):
    model = Drone
    template_name = "characters/werewolf/drone/chargen.html"


class DroneSpecialtiesView(HumanSpecialtiesView):
    model = Drone
    template_name = "characters/werewolf/drone/chargen.html"


class DroneCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Drone
    key_property = "creation_status"
    default_redirect = DroneDetailView
