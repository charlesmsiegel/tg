from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.demon.freebies import ThrallFreebiesForm
from characters.forms.demon.thrall import ThrallCreationForm
from characters.models.demon.thrall import Thrall
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.chargen_mixins import ChargenStepMixin
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
from core.mixins import (
    ScopedCreationFormMixin,
    SpecialUserMixin,
)
from core.permissions import PermissionManager


class ThrallBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = ThrallCreationForm
    template_name = "characters/demon/thrall/basics.html"

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
        # Set initial values
        self.object.willpower = 3
        self.object.faith_potential = 1
        self.object.daily_faith_offered = 1
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ThrallAttributeView(HumanAttributeView):
    model = Thrall
    template_name = "characters/demon/thrall/chargen.html"


class ThrallAbilityView(HumanAbilityView):
    model = Thrall
    fields = Thrall.primary_abilities
    template_name = "characters/demon/thrall/chargen.html"
    primary = 13
    secondary = 9
    tertiary = 5


class ThrallBackgroundsView(HumanBackgroundsView):
    model = Thrall
    template_name = "characters/demon/thrall/chargen.html"


class ThrallVirtuesView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Thrall
    fields = ["conviction", "courage", "conscience"]
    template_name = "characters/demon/thrall/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["conviction"].help_text = "Thrall Virtue"
        form.fields["courage"].help_text = "Thrall Virtue"
        form.fields["conscience"].help_text = "Thrall Virtue"
        return form

    def form_valid(self, form):
        # Calculate total virtues (must equal 6)
        total = (
            form.cleaned_data.get("conviction", 0)
            + form.cleaned_data.get("courage", 0)
            + form.cleaned_data.get("conscience", 0)
        )

        if total != 6:
            form.add_error(None, f"Virtues must total 6 dots. Currently: {total}")
            return self.form_invalid(form)

        # Update willpower based on courage
        self.object.willpower = form.cleaned_data.get("courage", 1)

        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class ThrallExtrasView(CharacterExtrasView):
    model = Thrall
    fields = ["age", "apparent_age", "date_of_birth", "history", "goals", "notes"]
    template_name = "characters/demon/thrall/chargen.html"
    date_fields = ()
    optional_fields = ("notes", "history", "goals")
    field_widget_attrs = {
        "history": {
            "placeholder": "Describe your character's history, including how they became bound to a demon.",
            "rows": 6,
        },
        "goals": {"placeholder": "What does your character hope to achieve?", "rows": 3},
    }


class ThrallFreebiesView(HumanFreebiesView):
    """Freebie spending view for Thrall characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    ThrallFreebieSpendingService with Thrall-specific handlers.
    """

    model = Thrall
    form_class = ThrallFreebiesForm
    template_name = "characters/demon/thrall/chargen.html"


class ThrallLanguagesView(HumanLanguagesView):
    model = Thrall
    template_name = "characters/demon/thrall/chargen.html"


class ThrallAlliesView(GenericBackgroundView):
    background_name = "allies"
    primary_object_class = Thrall
    model = Thrall
    template_name = "characters/demon/thrall/chargen.html"
    form_class = LinkedNPCForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg_name"] = "allies"
        return context


class ThrallSpecialtiesView(HumanSpecialtiesView):
    model = Thrall
    template_name = "characters/demon/thrall/chargen.html"


class ThrallCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Thrall
    key_property = "creation_status"
    default_redirect = DetailView
