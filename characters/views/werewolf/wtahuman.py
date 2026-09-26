from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.forms.core.crud_fields import WT_A_HUMAN_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.template_selection import (
    CharacterTemplateSelectionForm as SharedCharacterTemplateSelectionForm,
)
from characters.forms.werewolf.wtahuman import WtAHumanCreationForm
from characters.models.werewolf.wtahuman import WtAHuman
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAbilityView,
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.core.template_selection import CharacterTemplateSelectView
from core.mixins import (
    EditPermissionMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
    XPApprovalMixin,
)
from core.permissions import PermissionManager


class WtAHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = WtAHuman
    template_name = "characters/werewolf/wtahuman/detail.html"


class WtAHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = WtAHuman
    success_message = "WtA Human updated successfully."
    error_message = "Error updating WtA Human."
    fields = WT_A_HUMAN_UPDATE_FIELDS
    template_name = "characters/werewolf/wtahuman/form.html"

    limited_form_class = LimitedHumanEditForm


class WtAHumanBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = WtAHumanCreationForm
    template_name = "characters/werewolf/wtahuman/basics.html"

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
        return reverse("characters:werewolf:wtahuman_template", kwargs={"pk": self.object.pk})


class CharacterTemplateSelectionForm(SharedCharacterTemplateSelectionForm):
    gameline = "wta"
    character_type = "werewolf"


class WtAHumanTemplateSelectView(CharacterTemplateSelectView):
    model = WtAHuman
    form_class = CharacterTemplateSelectionForm
    template_name = "characters/werewolf/wtahuman/template_select.html"
    creation_route = "characters:werewolf:wtahuman_creation"


class WtAHumanAttributeView(HumanAttributeView):
    model = WtAHuman
    template_name = "characters/werewolf/wtahuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class WtAHumanAbilityView(HumanAbilityView):
    model = WtAHuman
    fields = WtAHuman.primary_abilities
    template_name = "characters/werewolf/wtahuman/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4


class WtAHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanExtrasView(CharacterExtrasView):
    model = WtAHuman
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
    template_name = "characters/werewolf/wtahuman/chargen.html"
    field_widget_attrs = {
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        }
    }


class WtAHumanFreebiesView(HumanFreebiesView):
    model = WtAHuman
    form_class = ChainedHumanFreebiesForm
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanLanguagesView(HumanLanguagesView):
    model = WtAHuman
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanAlliesView(GenericBackgroundView):
    primary_object_class = WtAHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanSpecialtiesView(HumanSpecialtiesView):
    model = WtAHuman
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = WtAHuman
    key_property = "creation_status"
    default_redirect = WtAHumanDetailView
