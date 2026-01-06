from typing import Any

from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.vampire.freebies import GhoulFreebiesForm
from characters.forms.vampire.ghoul import GhoulCreationForm
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.vampire.vtmhuman import VtMHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.mixins import (
    EditPermissionMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    ViewPermissionMixin,
)
from core.models import Language
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, UpdateView


class GhoulBasicsView(LoginRequiredMixin, FormView):
    form_class = GhoulCreationForm
    template_name = "characters/vampire/ghoul/basics.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = self.request.user.profile.is_st()
        return context

    def form_valid(self, form):
        self.object = form.save()
        # Ghouls start with Potence 1 (already set as default in model)
        # Set initial willpower to courage (default 1)
        # Use set_willpower() to properly adjust temporary_willpower and avoid constraint violations
        self.object.set_willpower(self.object.courage)
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class GhoulAttributeView(HumanAttributeView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/chargen.html"

    # Ghouls get 6/4/3 instead of 7/5/3
    primary = 6
    secondary = 4
    tertiary = 3


class GhoulAbilityView(VtMHumanAbilityView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/chargen.html"

    # Ghouls get 11/7/4 instead of 13/9/5
    primary = 11
    secondary = 7
    tertiary = 4


class GhoulBackgroundsView(HumanBackgroundsView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/chargen.html"


class GhoulDisciplinesView(SpecialUserMixin, UpdateView):
    model = Ghoul
    fields = [
        "potence",
        "celerity",
        "fortitude",
        "auspex",
        "dominate",
        "obfuscate",
        "presence",
    ]
    template_name = "characters/vampire/ghoul/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Potence is always 1 and can't be changed during chargen
        form.fields["potence"].widget = forms.HiddenInput()
        form.fields["potence"].help_text = "All ghouls have Potence 1"

        # Get available disciplines based on domitor or independence
        available_disciplines = self.object.get_available_disciplines()
        available_property_names = [d.property_name for d in available_disciplines]

        # Hide disciplines that aren't available
        for field_name in self.fields:
            if field_name == "potence":
                continue  # Already handled
            if field_name not in available_property_names:
                form.fields[field_name].widget = forms.HiddenInput()
            else:
                if self.object.domitor:
                    form.fields[field_name].help_text = "Domitor's Clan Discipline"
                else:
                    form.fields[field_name].help_text = "Physical Discipline"

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_disciplines"] = self.object.get_available_disciplines()
        context["has_domitor"] = bool(self.object.domitor)
        return context

    def form_valid(self, form):
        # Calculate total disciplines (excluding Potence which is automatic)
        total_disciplines = 0
        for field in self.fields:
            if field != "potence":
                total_disciplines += form.cleaned_data.get(field, 0)

        # Ghouls can spend up to 2 dots on additional disciplines during chargen
        if total_disciplines > 2:
            form.add_error(
                None,
                f"You can spend up to 2 dots on additional Disciplines. Currently: {total_disciplines}",
            )
            return self.form_invalid(form)

        # Verify all disciplines are available
        available_disciplines = self.object.get_available_disciplines()
        available_property_names = [d.property_name for d in available_disciplines]

        for field in self.fields:
            if field == "potence":
                continue
            rating = form.cleaned_data.get(field, 0)
            if rating > 0 and field not in available_property_names:
                form.add_error(
                    field,
                    "You can only learn disciplines available from your domitor or physical disciplines if independent.",
                )
                return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class GhoulExtrasView(SpecialUserMixin, UpdateView):
    model = Ghoul
    fields = [
        "age",
        "apparent_age",
        "date_of_birth",
        "years_as_ghoul",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/vampire/ghoul/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe your character's history, including life before and after becoming a ghoul.",
                "rows": 6,
            }
        )
        form.fields["goals"].widget.attrs.update(
            {"placeholder": "What does your character hope to achieve?", "rows": 3}
        )
        form.fields["notes"].required = False
        form.fields["history"].required = False
        form.fields["goals"].required = False
        form.fields["years_as_ghoul"].help_text = "How many years has your character been a ghoul?"
        return form

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class GhoulFreebiesView(HumanFreebiesView):
    """Freebie spending view for Ghoul characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    GhoulFreebieSpendingService with Ghoul-specific handlers.
    """

    model = Ghoul
    form_class = GhoulFreebiesForm
    template_name = "characters/vampire/ghoul/chargen.html"


class GhoulLanguagesView(HumanLanguagesView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/chargen.html"


class GhoulAlliesView(GenericBackgroundView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/chargen.html"
    form_class = LinkedNPCForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg_name"] = "allies"
        return context


class GhoulSpecialtiesView(HumanSpecialtiesView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/chargen.html"


class GhoulFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Ghoul

    def category_method_map(self):
        d = super().category_method_map()
        d.update(
            {
                "Discipline": self.discipline_options,
            }
        )
        return d

    def discipline_options(self):
        return Discipline.objects.all().order_by("name")


class GhoulCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: GhoulAttributeView,
        2: GhoulAbilityView,
        3: GhoulBackgroundsView,
        4: GhoulDisciplinesView,
        5: GhoulExtrasView,
        6: GhoulFreebiesView,
        7: GhoulLanguagesView,
        8: GhoulAlliesView,
        9: GhoulSpecialtiesView,
    }
    model_class = Ghoul
    key_property = "creation_status"
    default_redirect = DetailView
