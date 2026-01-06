from typing import Any

from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.demon.demon import DemonCreationForm
from characters.forms.demon.freebies import DemonFreebiesForm
from characters.models.core.specialty import Specialty
from characters.models.core.statistic import Statistic
from characters.models.demon.apocalyptic_form import (
    ApocalypticForm,
    ApocalypticFormTrait,
)
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
    EditPermissionMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    ViewPermissionMixin,
)
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


class DemonAbilityView(SpecialUserMixin, UpdateView):
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

        talents = sum([form.cleaned_data.get(ability) for ability in self.model.talents])
        skills = sum([form.cleaned_data.get(ability) for ability in self.model.skills])
        knowledges = sum([form.cleaned_data.get(ability) for ability in self.model.knowledges])

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


class DemonLoresView(SpecialUserMixin, UpdateView):
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

    def get_object(self):
        """Return the Demon object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Demon, pk=self.kwargs["pk"])
        return self.object

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        demon = get_object_or_404(Demon, pk=self.kwargs["pk"])

        # Get all available traits, separated by type
        # Low torment traits (exclude high_torment_only traits)
        low_torment_traits = ApocalypticFormTrait.objects.filter(high_torment_only=False)
        # High torment traits (all traits can be high torment)
        high_torment_traits = ApocalypticFormTrait.objects.all()

        # Add low torment trait fields
        for trait in low_torment_traits:
            form.fields[f"low_trait_{trait.id}"] = forms.BooleanField(
                required=False,
                label=f"{trait.name} ({trait.cost} points)",
                help_text=trait.description,
            )

        # Add high torment trait fields
        for trait in high_torment_traits:
            form.fields[f"high_trait_{trait.id}"] = forms.BooleanField(
                required=False,
                label=f"{trait.name} ({trait.cost} points)",
                help_text=trait.description,
            )

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["points_spent"] = context["object"].apocalyptic_form_points_spent()
        context["points_remaining"] = context["object"].apocalyptic_form_points_remaining()
        context["points_budget"] = 16
        return context

    def form_valid(self, form):
        demon = get_object_or_404(Demon, pk=self.kwargs["pk"])

        # Create or get an ApocalypticForm for this demon
        form_name = f"{demon.name}'s Apocalyptic Form"
        apoc_form, _ = ApocalypticForm.objects.get_or_create(
            name=form_name,
            defaults={"description": f"Apocalyptic form for {demon.name}"},
        )

        # Clear existing selections
        apoc_form.low_torment_traits.clear()
        apoc_form.high_torment_traits.clear()

        # Collect selected traits
        low_traits = []
        high_traits = []
        total_cost = 0

        for field_name, value in form.cleaned_data.items():
            if value:
                if field_name.startswith("low_trait_"):
                    trait_id = int(field_name.split("_")[2])
                    trait = ApocalypticFormTrait.objects.get(id=trait_id)
                    low_traits.append(trait)
                    total_cost += trait.cost
                elif field_name.startswith("high_trait_"):
                    trait_id = int(field_name.split("_")[2])
                    trait = ApocalypticFormTrait.objects.get(id=trait_id)
                    high_traits.append(trait)
                    total_cost += trait.cost

        # Validate selections
        if len(low_traits) != 4:
            form.add_error(
                None, f"You must select exactly 4 low torment traits. Currently: {len(low_traits)}"
            )
            return self.form_invalid(form)

        if len(high_traits) != 4:
            form.add_error(
                None,
                f"You must select exactly 4 high torment traits. Currently: {len(high_traits)}",
            )
            return self.form_invalid(form)

        if total_cost > 16:
            form.add_error(
                None, f"Point budget exceeded. Maximum is 16 points. Currently: {total_cost}"
            )
            return self.form_invalid(form)

        # Check for duplicate traits between low and high
        low_ids = {t.id for t in low_traits}
        high_ids = {t.id for t in high_traits}
        if low_ids & high_ids:
            form.add_error(None, "A trait cannot be selected as both low and high torment.")
            return self.form_invalid(form)

        # Add traits to the form
        for trait in low_traits:
            apoc_form.low_torment_traits.add(trait)
        for trait in high_traits:
            apoc_form.high_torment_traits.add(trait)

        demon.apocalyptic_form = apoc_form
        demon.creation_status += 1
        demon.save()
        return HttpResponseRedirect(demon.get_absolute_url())


class DemonVirtuesView(SpecialUserMixin, UpdateView):
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


class DemonExtrasView(SpecialUserMixin, UpdateView):
    model = Demon
    fields = [
        "celestial_name",
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


class DemonFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Demon

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
