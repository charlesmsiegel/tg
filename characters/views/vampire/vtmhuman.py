from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.template_selection import (
    CharacterTemplateSelectionForm as SharedCharacterTemplateSelectionForm,
)
from characters.forms.vampire.vtmhuman import VtMHumanCreationForm
from characters.models.vampire.vtmhuman import VtMHuman
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


class VtMHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/detail.html"


VTMHUMAN_FORM_FIELDS = [
    "name",
    "owner",
    "description",
    "nature",
    "demeanor",
    "willpower",
    "derangements",
    "age",
    "apparent_age",
    "date_of_birth",
    "merits_and_flaws",
    "history",
    "goals",
    "notes",
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
    "xp",
    "awareness",
    "leadership",
    "animal_ken",
    "larceny",
    "performance",
    "survival",
    "finance",
    "law",
    "occult",
    "politics",
    "technology",
]


class VtMHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = VtMHuman
    success_message = "VtM Human updated successfully."
    error_message = "Error updating VtM Human."
    fields = VTMHUMAN_FORM_FIELDS
    template_name = "characters/vampire/vtmhuman/form.html"

    limited_form_class = LimitedHumanEditForm


class VtMHumanBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = VtMHumanCreationForm
    template_name = "characters/vampire/vtmhuman/basics.html"

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
        self.object.creation_status = 1
        self.object.save()
        return reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.object.pk})


class CharacterTemplateSelectionForm(SharedCharacterTemplateSelectionForm):
    gameline = "vtm"
    character_type = "vampire"


class VtMHumanTemplateSelectView(CharacterTemplateSelectView):
    model = VtMHuman
    form_class = CharacterTemplateSelectionForm
    template_name = "characters/vampire/vtmhuman/template_select.html"
    creation_route = "characters:vampire:vtmhuman_creation"


class VtMHumanAttributeView(HumanAttributeView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class VtMHumanAbilityView(HumanAbilityView):
    model = VtMHuman
    fields = VtMHuman.primary_abilities
    template_name = "characters/vampire/vtmhuman/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4


class VtMHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanExtrasView(CharacterExtrasView):
    model = VtMHuman
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
    template_name = "characters/vampire/vtmhuman/chargen.html"
    field_widget_attrs = {
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        }
    }


class VtMHumanFreebiesView(HumanFreebiesView):
    model = VtMHuman
    form_class = ChainedHumanFreebiesForm
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanLanguagesView(HumanLanguagesView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanAlliesView(GenericBackgroundView):
    primary_object_class = VtMHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanSpecialtiesView(HumanSpecialtiesView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = VtMHuman
    key_property = "creation_status"
    default_redirect = VtMHumanDetailView
