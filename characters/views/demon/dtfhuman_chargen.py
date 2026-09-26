from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, FormView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.template_selection import (
    CharacterTemplateSelectionForm as SharedCharacterTemplateSelectionForm,
)
from characters.forms.demon.dtfhuman import DtFHumanCreationForm
from characters.forms.demon.freebies import DtFHumanFreebiesForm
from characters.models.demon.dtf_human import DtFHuman
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAbilityView,
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.core.template_selection import CharacterTemplateSelectView
from core.mixins import (
    ScopedCreationFormMixin,
)
from core.permissions import PermissionManager


class DtFHumanBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = DtFHumanCreationForm
    template_name = "characters/demon/dtfhuman/basics.html"

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
        # Set initial willpower
        self.object.willpower = 3
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("characters:demon:dtfhuman_template", kwargs={"pk": self.object.pk})


class CharacterTemplateSelectionForm(SharedCharacterTemplateSelectionForm):
    gameline = "dtf"
    character_type = "demon"


class DtFHumanTemplateSelectView(CharacterTemplateSelectView):
    model = DtFHuman
    form_class = CharacterTemplateSelectionForm
    template_name = "characters/demon/dtfhuman/template_select.html"
    creation_route = "characters:demon:dtfhuman_creation"


class DtFHumanAttributeView(HumanAttributeView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DtFHumanAbilityView(HumanAbilityView):
    model = DtFHuman
    fields = DtFHuman.primary_abilities
    template_name = "characters/demon/dtfhuman/chargen.html"
    primary = 13
    secondary = 9
    tertiary = 5


class DtFHumanBackgroundsView(HumanBackgroundsView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanExtrasView(CharacterExtrasView):
    model = DtFHuman
    fields = ["age", "apparent_age", "date_of_birth", "history", "goals", "notes"]
    template_name = "characters/demon/dtfhuman/chargen.html"
    date_fields = ()
    optional_fields = ("notes", "history", "goals")
    field_widget_attrs = {
        "history": {"placeholder": "Describe your character's history and background.", "rows": 6},
        "goals": {"placeholder": "What does your character hope to achieve?", "rows": 3},
    }


class DtFHumanFreebiesView(HumanFreebiesView):
    model = DtFHuman
    form_class = DtFHumanFreebiesForm
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanLanguagesView(HumanLanguagesView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanAlliesView(GenericBackgroundView):
    background_name = "allies"
    primary_object_class = DtFHuman
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"
    form_class = LinkedNPCForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg_name"] = "allies"
        return context


class DtFHumanSpecialtiesView(HumanSpecialtiesView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = DtFHuman
    key_property = "creation_status"
    default_redirect = DetailView
