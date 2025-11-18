from typing import Any

from characters.forms.core.ally import AllyForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.vampire.freebies import VampireFreebiesForm
from characters.forms.vampire.vampire import VampireCreationForm
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.vampire import Vampire
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
from core.models import Language
from core.views.approved_user_mixin import SpecialUserMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, UpdateView


class VampireBasicsView(LoginRequiredMixin, FormView):
    form_class = VampireCreationForm
    template_name = "characters/vampire/vampire/basics.html"

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
        self.object.willpower = self.object.courage
        if self.object.path:
            # Following a Path of Enlightenment
            self.object.path_rating = self.object.conviction + self.object.instinct
            self.object.humanity = 0
        else:
            # Default Humanity path
            self.object.humanity = self.object.conscience + self.object.self_control
            self.object.path_rating = 0
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class VampireAttributeView(HumanAttributeView):
    model = Vampire
    template_name = "characters/vampire/vampire/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class VampireAbilityView(VtMHumanAbilityView):
    model = Vampire
    template_name = "characters/vampire/vampire/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class VampireBackgroundsView(HumanBackgroundsView):
    model = Vampire
    template_name = "characters/vampire/vampire/chargen.html"


class VampireDisciplinesView(SpecialUserMixin, UpdateView):
    model = Vampire
    fields = [
        "celerity",
        "fortitude",
        "potence",
        "auspex",
        "dominate",
        "dementation",
        "presence",
        "animalism",
        "protean",
        "obfuscate",
        "chimerstry",
        "necromancy",
        "obtenebration",
        "quietus",
        "serpentis",
        "thaumaturgy",
        "vicissitude",
        "daimoinon",
        "melpominee",
        "mytherceria",
        "obeah",
        "temporis",
        "thanatosis",
        "valeren",
        "visceratika",
    ]
    template_name = "characters/vampire/vampire/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Only show clan disciplines if clan is set
        if self.object.clan:
            clan_discipline_properties = [
                d.property_name for d in self.object.clan.disciplines.all()
            ]
            # Hide non-clan disciplines by setting widget to HiddenInput
            for field_name in self.fields:
                if field_name not in clan_discipline_properties:
                    form.fields[field_name].widget = forms.HiddenInput()
                else:
                    form.fields[field_name].help_text = "Clan Discipline"

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        if self.object.clan:
            context["clan_disciplines"] = self.object.get_clan_disciplines()
        else:
            context["clan_disciplines"] = []
        return context

    def form_valid(self, form):
        # Calculate total disciplines
        total_disciplines = 0
        for field in self.fields:
            total_disciplines += form.cleaned_data.get(field, 0)

        if total_disciplines != 3:
            form.add_error(
                None, f"You must spend exactly 3 dots on Disciplines. Currently: {total_disciplines}"
            )
            return self.form_invalid(form)

        # Verify all disciplines are in-clan
        if self.object.clan:
            clan_discipline_properties = [
                d.property_name for d in self.object.clan.disciplines.all()
            ]
            for field in self.fields:
                rating = form.cleaned_data.get(field, 0)
                if rating > 0 and field not in clan_discipline_properties:
                    form.add_error(
                        field,
                        f"You can only spend starting dots on clan Disciplines."
                    )
                    return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class VampireVirtuesView(SpecialUserMixin, UpdateView):
    model = Vampire
    fields = ["conscience", "self_control", "courage", "conviction", "instinct"]
    template_name = "characters/vampire/vampire/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Hide unused virtues based on path
        if self.object.path:
            # Sabbat/Path: use Conviction and Instinct
            form.fields["conscience"].widget = forms.HiddenInput()
            form.fields["self_control"].widget = forms.HiddenInput()
            form.fields["conviction"].help_text = "Sabbat Virtue"
            form.fields["instinct"].help_text = "Sabbat Virtue"
        else:
            # Camarilla: use Conscience and Self-Control
            form.fields["conviction"].widget = forms.HiddenInput()
            form.fields["instinct"].widget = forms.HiddenInput()
            form.fields["conscience"].help_text = "Camarilla Virtue"
            form.fields["self_control"].help_text = "Camarilla Virtue"

        form.fields["courage"].help_text = "Universal Virtue"

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        context["uses_path"] = bool(self.object.path)
        return context

    def form_valid(self, form):
        # Calculate total virtues
        if self.object.path:
            # Sabbat: Conviction + Instinct + Courage = 7
            total = (
                form.cleaned_data.get("conviction", 0)
                + form.cleaned_data.get("instinct", 0)
                + form.cleaned_data.get("courage", 0)
            )
        else:
            # Camarilla: Conscience + Self-Control + Courage = 7
            total = (
                form.cleaned_data.get("conscience", 0)
                + form.cleaned_data.get("self_control", 0)
                + form.cleaned_data.get("courage", 0)
            )

        if total != 7:
            form.add_error(None, f"Virtues must total 7 dots. Currently: {total}")
            return self.form_invalid(form)

        # Update dependent values
        self.object.willpower = form.cleaned_data.get("courage", 1)

        if self.object.path:
            self.object.path_rating = (
                form.cleaned_data.get("conviction", 0)
                + form.cleaned_data.get("instinct", 0)
            )
            self.object.humanity = 0
        else:
            self.object.humanity = (
                form.cleaned_data.get("conscience", 0)
                + form.cleaned_data.get("self_control", 0)
            )
            self.object.path_rating = 0

        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class VampireExtrasView(SpecialUserMixin, UpdateView):
    model = Vampire
    fields = [
        "age",
        "apparent_age",
        "date_of_birth",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/vampire/vampire/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe your character's history, including mortal life and the circumstances of the Embrace.",
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


class VampireFreebiesView(HumanFreebiesView):
    model = Vampire
    form_class = VampireFreebiesForm
    template_name = "characters/vampire/vampire/chargen.html"

    def get_category_functions(self):
        d = super().get_category_functions()
        d.update({
            "discipline": self.object.discipline_freebies,
            "virtue": self.object.virtue_freebies,
            "humanity": self.object.humanity_freebies,
            "path_rating": self.object.path_rating_freebies,
        })
        return d


class VampireLanguagesView(HumanLanguagesView):
    model = Vampire
    template_name = "characters/vampire/vampire/chargen.html"


class VampireAlliesView(GenericBackgroundView):
    model = Vampire
    template_name = "characters/vampire/vampire/chargen.html"
    form_class = AllyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg_name"] = "allies"
        return context


class VampireSpecialtiesView(HumanSpecialtiesView):
    model = Vampire
    template_name = "characters/vampire/vampire/chargen.html"


class VampireFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Vampire
    template_name = "characters/core/human/load_examples_dropdown_list.html"

    def category_method_map(self):
        d = super().category_method_map()
        d.update({
            "Discipline": self.discipline_options,
        })
        return d

    def discipline_options(self):
        return Discipline.objects.all().order_by("name")


class VampireCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: VampireAttributeView,
        2: VampireAbilityView,
        3: VampireBackgroundsView,
        4: VampireDisciplinesView,
        5: VampireVirtuesView,
        6: VampireExtrasView,
        7: VampireFreebiesView,
        8: VampireLanguagesView,
        9: VampireAlliesView,
        10: VampireSpecialtiesView,
    }
    model_class = Vampire
    key_property = "creation_status"
    default_redirect = DetailView
