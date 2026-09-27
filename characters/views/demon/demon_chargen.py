from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.rules.limits import (
    APOCALYPTIC_FORM_POINT_BUDGET,
    DEMON_LORES,
    FALLEN_VIRTUES,
)
from characters.views.core.allocations import AllocationStepMixin
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.demon.apocalyptic_form import ApocalypticFormSelectionForm
from characters.forms.demon.demon import DemonCreationForm
from characters.forms.demon.freebies import DemonFreebiesForm
from characters.models.demon.demon import Demon
from characters.services.demon_chargen import apply_apocalyptic_form
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
    EditPermissionMixin,
    ScopedCreationFormMixin,
    SpecialUserMixin,
)
from core.permissions import PermissionManager


class DemonBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = DemonCreationForm
    template_name = "characters/demon/demon/basics.html"

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
        self.object.faith = 3
        self.object.temporary_faith = 3
        if self.object.house:
            self.object.torment = self.object.house.starting_torment
        else:
            self.object.torment = 3
        self.object.temporary_torment = 0
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class DemonAttributeView(HumanAttributeView):
    model = Demon
    template_name = "characters/demon/demon/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DemonAbilityView(HumanAbilityView):
    model = Demon
    fields = Demon.primary_abilities
    template_name = "characters/demon/demon/chargen.html"
    primary = 13
    secondary = 9
    tertiary = 5


class DemonBackgroundsView(HumanBackgroundsView):
    model = Demon
    template_name = "characters/demon/demon/chargen.html"


class DemonLoresView(AllocationStepMixin, ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Demon
    fields = list(DEMON_LORES.fields)
    allocation_rules = (DEMON_LORES,)
    template_name = "characters/demon/demon/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Highlight house lores if house is set
        if self.object.house:
            house_lore_properties = [
                f"lore_of_{lore.property_name}" for lore in self.object.house.lores.all()
            ]
            for field_name in self.fields:
                if field_name in house_lore_properties:
                    form.fields[field_name].help_text = "House Lore (reduced cost)"

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.house:
            context["house_lores"] = self.object.house.lores.all()
        else:
            context["house_lores"] = []
        return context

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class DemonApocalypticFormView(ChargenStepMixin, EditPermissionMixin, FormView):
    template_name = "characters/demon/demon/chargen.html"
    form_class = ApocalypticFormSelectionForm

    def get_object(self):
        """Return the Demon object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Demon, pk=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["points_spent"] = context["object"].apocalyptic_form_points_spent()
        context["points_remaining"] = context["object"].apocalyptic_form_points_remaining()
        context["points_budget"] = APOCALYPTIC_FORM_POINT_BUDGET
        return context

    def form_valid(self, form):
        demon = self.get_object()
        apply_apocalyptic_form(demon, form.low_traits, form.high_traits)
        advance(demon, user=self.request.user)
        demon.save()
        return HttpResponseRedirect(demon.get_absolute_url())


class DemonVirtuesView(AllocationStepMixin, ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Demon
    fields = ["conviction", "courage", "conscience"]
    allocation_rules = (FALLEN_VIRTUES,)
    template_name = "characters/demon/demon/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["conviction"].help_text = "Demon Virtue"
        form.fields["courage"].help_text = "Demon Virtue"
        form.fields["conscience"].help_text = "Demon Virtue"
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Willpower equals Courage; set_willpower keeps temporary Willpower in range.
        self.object.set_willpower(self.object.courage)
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class DemonExtrasView(CharacterExtrasView):
    model = Demon
    fields = [
        "celestial_name",
        "age_of_fall",
        "abyss_duration",
        "age",
        "apparent_age",
        "date_of_birth",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/demon/demon/chargen.html"
    date_fields = ()
    optional_fields = ("notes", "history", "goals", "abyss_duration")
    field_widget_attrs = {
        "celestial_name": {"placeholder": "Your name before the Fall"},
        "history": {
            "placeholder": "Describe your character's history, including their role before the Fall and their experiences since escaping the Abyss.",
            "rows": 6,
        },
        "goals": {"placeholder": "What does your character hope to achieve?", "rows": 3},
        "abyss_duration": {"placeholder": "How long were you imprisoned in the Abyss?", "rows": 2},
    }


class DemonFreebiesView(HumanFreebiesView):
    """Freebie spending view for Demon characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    DemonFreebieSpendingService with Demon-specific handlers.
    """

    model = Demon
    form_class = DemonFreebiesForm
    template_name = "characters/demon/demon/chargen.html"


class DemonLanguagesView(HumanLanguagesView):
    model = Demon
    template_name = "characters/demon/demon/chargen.html"


class DemonAlliesView(GenericBackgroundView):
    primary_object_class = Demon
    background_name = "allies"
    template_name = "characters/demon/demon/chargen.html"
    form_class = LinkedNPCForm


class DemonMentorView(GenericBackgroundView):
    primary_object_class = Demon
    background_name = "mentor"
    template_name = "characters/demon/demon/chargen.html"
    form_class = LinkedNPCForm


class DemonContactsView(GenericBackgroundView):
    primary_object_class = Demon
    background_name = "contacts"
    template_name = "characters/demon/demon/chargen.html"
    form_class = LinkedNPCForm


class DemonRetainersView(GenericBackgroundView):
    primary_object_class = Demon
    background_name = "retainers"
    template_name = "characters/demon/demon/chargen.html"
    form_class = LinkedNPCForm


class DemonFollowersView(GenericBackgroundView):
    primary_object_class = Demon
    background_name = "followers"
    template_name = "characters/demon/demon/chargen.html"
    form_class = LinkedNPCForm


class DemonSpecialtiesView(HumanSpecialtiesView):
    model = Demon
    template_name = "characters/demon/demon/chargen.html"


class DemonCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Demon
    key_property = "creation_status"
    default_redirect = DetailView
