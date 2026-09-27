from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.forms.core.crud_fields import MT_A_HUMAN_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.template_selection import (
    CharacterTemplateSelectionForm as SharedCharacterTemplateSelectionForm,
)
from characters.forms.mage.mtahuman import MtAHumanCreationForm
from characters.models.mage.faction import MageFaction
from characters.models.mage.mtahuman import MtAHuman
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
from characters.views.mage.background_views import (
    CharacterChantryBackgroundView,
    MtAEnhancementView,
)
from core.mixins import (
    EditPermissionMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
    XPApprovalMixin,
)
from core.permissions import PermissionManager
from items.forms.mage.wonder import WonderForm
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


class MtAHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = MtAHuman
    template_name = "characters/mage/mtahuman/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MtAHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = MtAHuman
    success_message = "MtA Human updated successfully."
    error_message = "Error updating MtA Human."
    fields = MT_A_HUMAN_UPDATE_FIELDS
    template_name = "characters/mage/mtahuman/form.html"

    limited_form_class = LimitedHumanEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MtAHumanAbilityView(HumanAbilityView):
    model = MtAHuman
    fields = MtAHuman.primary_abilities
    template_name = "characters/mage/mtahuman/chargen.html"
    primary = 11
    secondary = 7
    tertiary = 4


class MtAHumanBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = MtAHumanCreationForm
    template_name = "characters/mage/mtahuman/basics.html"

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
        return reverse("characters:mage:mtahuman_template", kwargs={"pk": self.object.pk})


class CharacterTemplateSelectionForm(SharedCharacterTemplateSelectionForm):
    gameline = "mta"
    character_type = "mage"


class MtAHumanTemplateSelectView(CharacterTemplateSelectView):
    model = MtAHuman
    form_class = CharacterTemplateSelectionForm
    template_name = "characters/mage/mtahuman/template_select.html"
    creation_route = "characters:mage:mtahuman_creation"


class MtAHumanAttributeView(HumanAttributeView):
    model = MtAHuman
    template_name = "characters/mage/mtahuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MtAHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanExtrasView(CharacterExtrasView):
    model = MtAHuman
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
    template_name = "characters/mage/mtahuman/chargen.html"
    field_widget_attrs = {
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        }
    }


class MtAHumanFreebiesView(HumanFreebiesView):
    model = MtAHuman
    form_class = ChainedHumanFreebiesForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanLanguagesView(HumanLanguagesView):
    model = MtAHuman
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanAlliesView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanEnhancementView(MtAEnhancementView):
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanLibraryView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "library"
    form_class = LibraryForm
    template_name = "characters/mage/mtahuman/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        form.fields["name"].initial = self.current_background.note or f"{obj.name}'s Library"
        form.fields["faction"].queryset = MageFaction.objects.all()
        return form


class MtAHumanNodeView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "node"
    form_class = NodeForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanSpecialtiesView(HumanSpecialtiesView):
    model = MtAHuman
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanWonderView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "wonder"
    form_class = WonderForm
    template_name = "characters/mage/mtahuman/chargen.html"
    multiple_ownership = True


class MtAHumanSanctumView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "sanctum"
    form_class = SanctumForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanChantryView(CharacterChantryBackgroundView):
    primary_object_class = MtAHuman
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = MtAHuman
    key_property = "creation_status"
    default_redirect = MtAHumanDetailView
