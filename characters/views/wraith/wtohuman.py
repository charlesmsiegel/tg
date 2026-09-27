from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.forms.core.crud_fields import WT_O_HUMAN_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.template_selection import (
    CharacterTemplateSelectionForm as SharedCharacterTemplateSelectionForm,
)
from characters.forms.wraith.wtohuman import WtOHumanCreationForm
from characters.models.wraith.wtohuman import WtOHuman
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


class WtOHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = WtOHuman
    template_name = "characters/wraith/wtohuman/detail.html"


class WtOHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = WtOHuman
    fields = WT_O_HUMAN_UPDATE_FIELDS
    template_name = "characters/wraith/wtohuman/form.html"
    success_message = "Wraith Human '{name}' updated successfully!"
    error_message = "Failed to update wraith human. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm


class WtOHumanBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = WtOHumanCreationForm
    template_name = "characters/wraith/wtohuman/basics.html"

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
            f"Wraith Human '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("characters:wraith:wtohuman_template", kwargs={"pk": self.object.pk})


class CharacterTemplateSelectionForm(SharedCharacterTemplateSelectionForm):
    gameline = "wto"
    character_type = "wraith"


class WtOHumanTemplateSelectView(CharacterTemplateSelectView):
    model = WtOHuman
    form_class = CharacterTemplateSelectionForm
    template_name = "characters/wraith/wtohuman/template_select.html"
    creation_route = "characters:wraith:wtohuman_creation"


class WtOHumanAttributeView(HumanAttributeView):
    model = WtOHuman
    template_name = "characters/wraith/wtohuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class WtOHumanAbilityView(HumanAbilityView):
    model = WtOHuman
    fields = WtOHuman.primary_abilities
    template_name = "characters/wraith/wtohuman/chargen.html"
    primary = 11
    secondary = 7
    tertiary = 4
    success_message = "Abilities allocated successfully!"
    rating_error_message = "All abilities must be between 0 and 3 dots."
    allocation_error_message = (
        "{allocation}. Current: {talents} talents, {skills} skills, {knowledges} knowledges."
    )

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WtOHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/wraith/wtohuman/chargen.html"


class WtOHumanExtrasView(CharacterExtrasView):
    model = WtOHuman
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
    template_name = "characters/wraith/wtohuman/chargen.html"
    success_message = "Character details saved successfully!"
    field_widget_attrs = {
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        }
    }

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WtOHumanFreebiesView(HumanFreebiesView):
    model = WtOHuman
    form_class = ChainedHumanFreebiesForm
    template_name = "characters/wraith/wtohuman/chargen.html"


class WtOHumanLanguagesView(HumanLanguagesView):
    model = WtOHuman
    template_name = "characters/wraith/wtohuman/chargen.html"
    success_message = "Languages added successfully!"


class WtOHumanAlliesView(GenericBackgroundView):
    primary_object_class = WtOHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wtohuman/chargen.html"


class WtOHumanSpecialtiesView(HumanSpecialtiesView):
    model = WtOHuman
    template_name = "characters/wraith/wtohuman/chargen.html"
    success_message = "Wraith Human '{name}' submitted for approval!"


class WtOHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = WtOHuman
    key_property = "creation_status"
    default_redirect = WtOHumanDetailView
