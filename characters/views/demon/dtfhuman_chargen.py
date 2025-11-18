from typing import Any

from characters.forms.core.ally import AllyForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.demon.dtfhuman import DtFHumanCreationForm
from characters.forms.demon.freebies import DtFHumanFreebiesForm
from characters.models.core.specialty import Specialty
from characters.models.demon.dtf_human import DtFHuman
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
from core.views.approved_user_mixin import SpecialUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, UpdateView


class DtFHumanBasicsView(LoginRequiredMixin, FormView):
    form_class = DtFHumanCreationForm
    template_name = "characters/demon/dtfhuman/basics.html"

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
        # Set initial willpower
        self.object.willpower = 3
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class DtFHumanAttributeView(HumanAttributeView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class DtFHumanAbilityView(SpecialUserMixin, UpdateView):
    model = DtFHuman
    fields = DtFHuman.primary_abilities
    template_name = "characters/demon/dtfhuman/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["primary"] = self.primary
        context["secondary"] = self.secondary
        context["tertiary"] = self.tertiary
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
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


class DtFHumanBackgroundsView(HumanBackgroundsView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanExtrasView(SpecialUserMixin, UpdateView):
    model = DtFHuman
    fields = [
        "age",
        "apparent_age",
        "date_of_birth",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/demon/dtfhuman/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe your character's history and background.",
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class DtFHumanFreebiesView(HumanFreebiesView):
    model = DtFHuman
    form_class = DtFHumanFreebiesForm
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanLanguagesView(HumanLanguagesView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanAlliesView(GenericBackgroundView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"
    form_class = AllyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg_name"] = "allies"
        return context


class DtFHumanSpecialtiesView(HumanSpecialtiesView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/chargen.html"


class DtFHumanFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = DtFHuman
    template_name = "characters/core/human/load_examples_dropdown_list.html"


class DtFHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: DtFHumanAttributeView,
        2: DtFHumanAbilityView,
        3: DtFHumanBackgroundsView,
        4: DtFHumanExtrasView,
        5: DtFHumanFreebiesView,
        6: DtFHumanLanguagesView,
        7: DtFHumanAlliesView,
        8: DtFHumanSpecialtiesView,
    }
    model_class = DtFHuman
    key_property = "creation_status"
    default_redirect = DetailView
