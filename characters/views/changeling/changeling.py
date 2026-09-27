from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.changeling.chained_freebies import ChainedChangelingFreebiesForm
from characters.forms.changeling.changeling import ChangelingCreationForm
from characters.forms.core.crud_fields import CHANGELING_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.models.changeling.changeling import Changeling
from characters.models.core.merit_flaw_block import MeritFlawRating
from characters.rules.limits import CHANGELING_ARTS, CHANGELING_REALMS
from characters.views.changeling.ctdhuman import CtDHumanAbilityView
from characters.views.core.allocations import AllocationStepMixin
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.chargen_mixins import ChargenStepMixin
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from core.mixins import (
    EditPermissionMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
    SpecialUserMixin,
)
from core.permissions import PermissionManager


class ChangelingDetailView(HumanDetailView):
    model = Changeling
    template_name = "characters/changeling/changeling/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["merits_and_flaws"] = MeritFlawRating.objects.order_by("mf__name").filter(
            character=self.object
        )
        return context


class ChangelingUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Changeling
    fields = CHANGELING_UPDATE_FIELDS
    template_name = "characters/changeling/changeling/form.html"
    success_message = "Changeling '{name}' updated successfully!"
    error_message = "Failed to update changeling. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChangelingBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = ChangelingCreationForm
    template_name = "characters/changeling/changeling/basics.html"

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
        messages.success(
            self.request,
            f"Changeling '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ChangelingAttributeView(HumanAttributeView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChangelingAbilityView(CtDHumanAbilityView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class ChangelingBackgroundsView(HumanBackgroundsView):
    template_name = "characters/changeling/changeling/chargen.html"


class ChangelingArtsRealmsView(AllocationStepMixin, ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Changeling
    fields = [*CHANGELING_ARTS.fields, *CHANGELING_REALMS.fields]
    allocation_rules = (CHANGELING_ARTS, CHANGELING_REALMS)
    template_name = "characters/changeling/changeling/chargen.html"

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        self.object.save()
        messages.success(self.request, "Arts and Realms allocated successfully!")
        return super().form_valid(form)


class ChangelingExtrasView(CharacterExtrasView):
    model = Changeling
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
        "true_name",
        "crysalis",
        "date_of_crysalis",
        "fae_mien",
        "antithesis",
        "musing_threshold",
        "ravaging_threshold",
    ]
    template_name = "characters/changeling/changeling/chargen.html"
    success_message = "Character details saved successfully!"
    date_fields = ("date_of_birth", "date_of_crysalis")
    optional_fields = ("date_of_birth", "date_of_crysalis")
    field_widget_attrs = {
        "history": {
            "placeholder": "Describe character history/backstory. Include information about their mortal life and their Chrysalis."
        },
        "true_name": {"placeholder": "Your character's fae true name"},
        "crysalis": {
            "placeholder": "Describe your character's Chrysalis - how they awakened to their fae nature."
        },
        "fae_mien": {"placeholder": "Describe your character's fae appearance."},
        "antithesis": {
            "placeholder": "What is your character's Antithesis? What causes them to gain Banality?"
        },
    }


class ChangelingFreebiesView(HumanFreebiesView):
    """Freebie spending view for Changeling characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    ChangelingFreebieSpendingService with Changeling-specific handlers.
    """

    model = Changeling
    form_class = ChainedChangelingFreebiesForm
    template_name = "characters/changeling/changeling/chargen.html"


class ChangelingLanguagesView(HumanLanguagesView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"
    success_message = "Languages added successfully!"


class ChangelingAlliesView(GenericBackgroundView):
    primary_object_class = Changeling
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/changeling/changeling/chargen.html"


class ChangelingSpecialtiesView(HumanSpecialtiesView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"
    success_message = "Changeling '{name}' submitted for approval!"


class ChangelingCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Changeling
    key_property = "creation_status"
    default_redirect = ChangelingDetailView
