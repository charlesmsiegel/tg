from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.crud_fields import KINFOLK_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.werewolf.kinfolk import KinfolkCreationForm
from characters.models.core.merit_flaw_block import MeritFlawRating
from characters.models.werewolf.kinfolk import Kinfolk
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
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
    XPApprovalMixin,
)
from core.permissions import PermissionManager


class KinfolkDetailView(XPApprovalMixin, HumanDetailView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["merits_and_flaws"] = MeritFlawRating.objects.order_by("mf__name").filter(
            character=self.object
        )
        all_gifts = list(context["object"].gifts.all())
        row_length = 3
        all_gifts = [all_gifts[i : i + row_length] for i in range(0, len(all_gifts), row_length)]
        context["gifts"] = all_gifts
        return context


class KinfolkUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Kinfolk
    success_message = "Kinfolk updated successfully."
    error_message = "Error updating kinfolk."
    fields = KINFOLK_UPDATE_FIELDS
    template_name = "characters/werewolf/kinfolk/form.html"

    limited_form_class = LimitedHumanEditForm


class KinfolkBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = KinfolkCreationForm
    template_name = "characters/werewolf/kinfolk/basics.html"

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


class KinfolkAttributeView(HumanAttributeView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class KinfolkAbilityView(WtAHumanAbilityView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkBackgroundsView(HumanBackgroundsView):
    """Tribal background restrictions come from Kinfolk.background_violations."""

    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkExtrasView(WtAHumanExtrasView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkFreebiesView(WtAHumanFreebiesView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkLanguagesView(HumanLanguagesView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkAlliesView(GenericBackgroundView):
    primary_object_class = Kinfolk
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkSpecialtiesView(HumanSpecialtiesView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Kinfolk
    key_property = "creation_status"
    default_redirect = KinfolkDetailView
