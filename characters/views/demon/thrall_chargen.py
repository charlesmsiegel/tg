from typing import Any

from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.demon.freebies import ThrallFreebiesForm
from characters.forms.demon.thrall import ThrallCreationForm
from characters.models.core.specialty import Specialty
from characters.models.demon.thrall import Thrall
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
from core.mixins import (
    ApprovedUserContextMixin,
    EditPermissionMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from core.views.approved_user_mixin import SpecialUserMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, UpdateView


class ThrallBasicsView(LoginRequiredMixin, FormView):
    form_class = ThrallCreationForm
    template_name = "characters/demon/thrall/basics.html"

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


class ThrallAbilityView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = Thrall
    fields = Thrall.primary_abilities
    template_name = "characters/demon/thrall/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["primary"] = self.primary
        context["secondary"] = self.secondary
        context["tertiary"] = self.tertiary
        return context

    def form_valid(self, form):
        for ability in self.model.primary_abilities:
            if form.cleaned_data.get(ability) < 0 or form.cleaned_data.get(ability) > 3:
                form.add_error(None, "Abilities must range from 0-3")
                return self.form_invalid(form)

        talents = sum(
            [form.cleaned_data.get(ability) for ability in self.model.talents]
        )
        skills = sum([form.cleaned_data.get(ability) for ability in self.model.skills])
        knowledges = sum(
            [form.cleaned_data.get(ability) for ability in self.model.knowledges]
        )

        triple = [talents, skills, knowledges]
        triple.sort()
        if triple != [self.tertiary, self.secondary, self.primary]:
            form.add_error(
                None,
                f"Abilities must be distributed {self.primary}/{self.secondary}/{self.tertiary}",
            )
            return self.form_invalid(form)
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class ThrallBackgroundsView(HumanBackgroundsView):
    model = Thrall
    template_name = "characters/demon/thrall/chargen.html"


class ThrallVirtuesView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
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

        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class ThrallExtrasView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = Thrall
    fields = [
        "age",
        "apparent_age",
        "date_of_birth",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/demon/thrall/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe your character's history, including how they became bound to a demon.",
                "rows": 6,
            }
        )
        form.fields["goals"].widget.attrs.update(
            {"placeholder": "What does your character hope to achieve?", "rows": 3}
        )
        form.fields["notes"].required = False
        form.fields["history"].required = False
        form.fields["goals"].required = False
        return form

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class ThrallFreebiesView(HumanFreebiesView):
    model = Thrall
    form_class = ThrallFreebiesForm
    template_name = "characters/demon/thrall/chargen.html"

    def get_category_functions(self):
        d = super().get_category_functions()
        d.update(
            {
                "faith_potential": self.object.faith_potential_freebies,
                "virtue": self.object.virtue_freebies,
            }
        )
        return d


class ThrallLanguagesView(HumanLanguagesView):
    model = Thrall
    template_name = "characters/demon/thrall/chargen.html"


class ThrallAlliesView(GenericBackgroundView):
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


class ThrallFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Thrall
    template_name = "characters/core/human/load_examples_dropdown_list.html"


class ThrallCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: ThrallAttributeView,
        2: ThrallAbilityView,
        3: ThrallBackgroundsView,
        4: ThrallVirtuesView,
        5: ThrallExtrasView,
        6: ThrallFreebiesView,
        7: ThrallLanguagesView,
        8: ThrallAlliesView,
        9: ThrallSpecialtiesView,
    }
    model_class = Thrall
    key_property = "creation_status"
    default_redirect = DetailView
