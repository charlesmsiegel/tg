from typing import Any

from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.demon.demon import DemonCreationForm
from characters.forms.demon.freebies import DemonFreebiesForm
from characters.models.core.specialty import Specialty
from characters.models.core.statistic import Statistic
from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from characters.models.demon.demon import Demon
from characters.models.demon.lore import Lore
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


class DemonBasicsView(LoginRequiredMixin, FormView):
    form_class = DemonCreationForm
    template_name = "characters/demon/demon/basics.html"

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


class DemonAbilityView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = Demon
    fields = Demon.primary_abilities
    template_name = "characters/demon/demon/chargen.html"

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


class DemonBackgroundsView(HumanBackgroundsView):
    model = Demon
    template_name = "characters/demon/demon/chargen.html"


class DemonLoresView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = Demon
    fields = [
        "lore_of_the_celestials",
        "lore_of_the_earth",
        "lore_of_the_firmament",
        "lore_of_humanity",
        "lore_of_the_wild",
        "lore_of_light",
        "lore_of_radiance",
        "lore_of_awakening",
        "lore_of_the_fundament",
        "lore_of_patterns",
        "lore_of_portals",
        "lore_of_forging",
        "lore_of_longing",
        "lore_of_storms",
        "lore_of_transfiguration",
        "lore_of_the_flesh",
        "lore_of_death",
        "lore_of_the_spirit",
        "lore_of_the_winds",
        "lore_of_flame",
        "lore_of_paths",
    ]
    template_name = "characters/demon/demon/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Highlight house lores if house is set
        if self.object.house:
            house_lore_properties = [
                f"lore_of_{lore.property_name}"
                for lore in self.object.house.lores.all()
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
        # Calculate total lores (must equal 3)
        total_lores = 0
        for field in self.fields:
            total_lores += form.cleaned_data.get(field, 0)

        if total_lores != 3:
            form.add_error(
                None,
                f"You must spend exactly 3 dots on Lores. Currently: {total_lores}",
            )
            return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class DemonApocalypticFormView(EditPermissionMixin, FormView):
    template_name = "characters/demon/demon/chargen.html"
    form_class = forms.Form

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        demon = get_object_or_404(Demon, pk=self.kwargs["pk"])

        # Get available traits from visage
        if demon.visage:
            available_traits = demon.get_available_apocalyptic_traits()
            if available_traits:
                for trait in available_traits:
                    form.fields[f"trait_{trait.id}"] = forms.BooleanField(
                        required=False,
                        label=f"{trait.name} ({trait.cost} points)",
                        help_text=trait.description,
                    )

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Demon, pk=self.kwargs["pk"])
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        context["points_spent"] = context["object"].apocalyptic_form_points_spent()
        context["points_remaining"] = context[
            "object"
        ].apocalyptic_form_points_remaining()
        context["points_budget"] = context["object"].apocalyptic_form_points
        return context

    def form_valid(self, form):
        demon = get_object_or_404(Demon, pk=self.kwargs["pk"])

        # Clear existing selections
        demon.apocalyptic_form.clear()

        # Add selected traits
        total_cost = 0
        traits_selected = 0

        for field_name, value in form.cleaned_data.items():
            if field_name.startswith("trait_") and value:
                trait_id = int(field_name.split("_")[1])
                trait = ApocalypticFormTrait.objects.get(id=trait_id)
                total_cost += trait.cost
                traits_selected += 1

                if traits_selected > 8:
                    form.add_error(None, "You can select a maximum of 8 traits")
                    return self.form_invalid(form)

                if total_cost > demon.apocalyptic_form_points:
                    form.add_error(
                        None,
                        f"Point budget exceeded. You have {demon.apocalyptic_form_points} points available.",
                    )
                    return self.form_invalid(form)

                demon.apocalyptic_form.add(trait)

        # Must spend at least 8 points
        if total_cost < 8:
            form.add_error(
                None,
                f"You must spend at least 8 points on Apocalyptic Form traits. Currently: {total_cost}",
            )
            return self.form_invalid(form)

        demon.creation_status += 1
        demon.save()
        return HttpResponseRedirect(demon.get_absolute_url())


class DemonVirtuesView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = Demon
    fields = ["conviction", "courage", "conscience"]
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


class DemonExtrasView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = Demon
    fields = [
        "celestial_name",
        "true_name",
        "host_name",
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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["celestial_name"].widget.attrs.update(
            {"placeholder": "Your name before the Fall"}
        )
        form.fields["true_name"].widget.attrs.update(
            {"placeholder": "Your true angelic name"}
        )
        form.fields["host_name"].widget.attrs.update(
            {"placeholder": "Name of the mortal body you inhabit"}
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe your character's history, including their role before the Fall and their experiences since escaping the Abyss.",
                "rows": 6,
            }
        )
        form.fields["goals"].widget.attrs.update(
            {"placeholder": "What does your character hope to achieve?", "rows": 3}
        )
        form.fields["abyss_duration"].widget.attrs.update(
            {"placeholder": "How long were you imprisoned in the Abyss?", "rows": 2}
        )
        form.fields["notes"].required = False
        form.fields["history"].required = False
        form.fields["goals"].required = False
        form.fields["abyss_duration"].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class DemonFreebiesView(HumanFreebiesView):
    model = Demon
    form_class = DemonFreebiesForm
    template_name = "characters/demon/demon/chargen.html"

    def get_category_functions(self):
        d = super().get_category_functions()
        d.update(
            {
                "lore": self.object.lore_freebies,
                "faith": self.object.faith_freebies,
                "virtue": self.object.virtue_freebies,
                "temporary_faith": self.object.temporary_faith_freebies,
            }
        )
        return d


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


class DemonFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Demon
    template_name = "characters/core/human/load_examples_dropdown_list.html"

    def category_method_map(self):
        d = super().category_method_map()
        d.update(
            {
                "Lore": self.lore_options,
            }
        )
        return d

    def lore_options(self):
        return Lore.objects.all().order_by("name")


class DemonCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: DemonAttributeView,
        2: DemonAbilityView,
        3: DemonBackgroundsView,
        4: DemonLoresView,
        5: DemonApocalypticFormView,
        6: DemonVirtuesView,
        7: DemonExtrasView,
        8: DemonFreebiesView,
        9: DemonLanguagesView,
        10: DemonAlliesView,
        11: DemonMentorView,
        12: DemonContactsView,
        13: DemonRetainersView,
        14: DemonFollowersView,
        15: DemonSpecialtiesView,
    }
    model_class = Demon
    key_property = "creation_status"
    default_redirect = DetailView
