from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.changeling.ctdhuman import CtDHumanCreationForm
from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.template_selection import (
    CharacterTemplateSelectionForm as SharedCharacterTemplateSelectionForm,
)
from characters.models.changeling.ctdhuman import CtDHuman
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


class CtDHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = CtDHuman
    template_name = "characters/changeling/ctdhuman/detail.html"


CTDHUMAN_FORM_FIELDS = [
    "name",
    "description",
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
    "willpower",
    "age",
    "apparent_age",
    "history",
    "goals",
    "notes",
    "kenning",
    "leadership",
    "animal_ken",
    "larceny",
    "performance",
    "survival",
    "enigmas",
    "gremayre",
    "law",
    "politics",
    "technology",
]


class CtDHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = CtDHuman
    success_message = "CtD Human updated successfully."
    error_message = "Error updating CtD Human."
    fields = CTDHUMAN_FORM_FIELDS
    template_name = "characters/changeling/ctdhuman/form.html"

    limited_form_class = LimitedHumanEditForm


class CtDHumanBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = CtDHumanCreationForm
    template_name = "characters/changeling/ctdhuman/basics.html"

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
        return reverse("characters:changeling:ctdhuman_template", kwargs={"pk": self.object.pk})


class CharacterTemplateSelectionForm(SharedCharacterTemplateSelectionForm):
    gameline = "ctd"
    character_type = "changeling"


class CtDHumanTemplateSelectView(CharacterTemplateSelectView):
    model = CtDHuman
    form_class = CharacterTemplateSelectionForm
    template_name = "characters/changeling/ctdhuman/template_select.html"
    creation_route = "characters:changeling:ctdhuman_creation"


class CtDHumanAttributeView(HumanAttributeView):
    model = CtDHuman
    template_name = "characters/changeling/ctdhuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class CtDHumanAbilityView(HumanAbilityView):
    model = CtDHuman
    fields = CtDHuman.primary_abilities
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanExtrasView(CharacterExtrasView):
    model = CtDHuman
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
    template_name = "characters/changeling/ctdhuman/chargen.html"
    field_widget_attrs = {
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        }
    }


class CtDHumanFreebiesView(HumanFreebiesView):
    model = CtDHuman
    form_class = ChainedHumanFreebiesForm
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanLanguagesView(HumanLanguagesView):
    model = CtDHuman
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanAlliesView(GenericBackgroundView):
    primary_object_class = CtDHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanSpecialtiesView(HumanSpecialtiesView):
    model = CtDHuman
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = CtDHuman
    key_property = "creation_status"
    default_redirect = CtDHumanDetailView
