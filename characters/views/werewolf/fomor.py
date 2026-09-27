from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.forms.core.crud_fields import FOMOR_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.werewolf.fomor import FomorCreationForm
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.fomoripower import FomoriPower
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
from characters.views.werewolf.wtahuman import WtAHumanAbilityView
from core.mixins import (
    EditPermissionMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
    SpecialUserMixin,
)
from core.permissions import PermissionManager


class FomorDetailView(HumanDetailView):
    model = Fomor
    template_name = "characters/werewolf/fomor/detail.html"


class FomorUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Fomor
    success_message = "Fomor updated successfully."
    error_message = "Error updating fomor."
    fields = FOMOR_UPDATE_FIELDS
    template_name = "characters/werewolf/fomor/form.html"

    limited_form_class = LimitedHumanEditForm


class FomorBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = FomorCreationForm
    template_name = "characters/werewolf/fomor/basics.html"

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


class FomorAttributeView(HumanAttributeView):
    model = Fomor
    template_name = "characters/werewolf/fomor/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class FomorAbilityView(WtAHumanAbilityView):
    model = Fomor
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorPowersView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Fomor
    fields = ["powers", "rage", "gnosis"]
    template_name = "characters/werewolf/fomor/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["powers"].queryset = FomoriPower.objects.all()
        form.fields["powers"].required = False
        form.fields["powers"].help_text = (
            "Select the powers your Fomor possesses. Fomori typically have 1-3 powers."
        )
        form.fields["rage"].help_text = "Fomori typically have 1-5 Rage"
        form.fields["gnosis"].help_text = "Fomori typically have 1-5 Gnosis"
        return form

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class FomorExtrasView(CharacterExtrasView):
    model = Fomor
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/werewolf/fomor/chargen.html"
    field_widget_attrs = {
        "history": {
            "placeholder": "Describe character history/backstory. Include information about their transformation into a Fomor, how they gained their powers, and their relationship with the Wyrm."
        },
        "goals": {"placeholder": "Describe your character's goals and motivations."},
    }


class FomorFreebiesView(HumanFreebiesView):
    model = Fomor
    form_class = ChainedHumanFreebiesForm
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorLanguagesView(HumanLanguagesView):
    model = Fomor
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorAlliesView(GenericBackgroundView):
    primary_object_class = Fomor
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorContactsView(GenericBackgroundView):
    primary_object_class = Fomor
    background_name = "contacts"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorSpecialtiesView(HumanSpecialtiesView):
    model = Fomor
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Fomor
    key_property = "creation_status"
    default_redirect = FomorDetailView
