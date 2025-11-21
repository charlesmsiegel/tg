from typing import Any

from characters.forms.changeling.changeling import ChangelingCreationForm
from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.models.changeling.changeling import Changeling
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlawRating
from characters.models.core.specialty import Specialty
from characters.models.core.statistic import Statistic
from characters.views.changeling.ctdhuman import CtDHumanAbilityView
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
)
from characters.views.mage.mtahuman import MtAHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.models import Language
from core.mixins import ViewPermissionMixin, EditPermissionMixin, SpendFreebiesPermissionMixin, SpendXPPermissionMixin
from core.views.message_mixin import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, FormView, UpdateView, View


class ChangelingDetailView(ViewPermissionMixin, DetailView):
    model = Changeling
    template_name = "characters/changeling/changeling/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialties = {}
        for attribute in self.object.get_attributes():
            specialties[attribute] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=attribute)]
            )
        for ability in self.object.get_abilities():
            specialties[ability] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=ability)]
            )
        for key, value in specialties.items():
            context[f"{key}_spec"] = value

        context["merits_and_flaws"] = MeritFlawRating.objects.order_by(
            "mf__name"
        ).filter(character=self.object)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context


class ChangelingCreateView(MessageMixin, CreateView):
    model = Changeling
    fields = [
        "name",
        "description",
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
        "willpower",
        "age",
        "apparent_age",
        "history",
        "goals",
        "notes",
        "kenning",
        "leadership",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "gremayre",
        "law",
        "politics",
        "technology",
        "court",
        "seeming",
        "autumn",
        "chicanery",
        "chronos",
        "contract",
        "dragons_ire",
        "legerdemain",
        "metamorphosis",
        "naming",
        "oneiromancy",
        "primal",
        "pyretics",
        "skycraft",
        "soothsay",
        "sovereign",
        "spring",
        "summer",
        "wayfare",
        "winter",
        "actor",
        "fae",
        "nature_realm",
        "prop",
        "scene",
        "time",
        "banality",
        "glamour",
        "musing_threshold",
        "ravaging_threshold",
        "antithesis",
        "true_name",
        "date_ennobled",
        "crysalis",
        "date_of_crysalis",
        "fae_mien",
    ]
    template_name = "characters/changeling/changeling/form.html"
    success_message = "Changeling '{name}' created successfully!"
    error_message = "Failed to create changeling. Please correct the errors below."


class ChangelingUpdateView(EditPermissionMixin, UpdateView):
    model = Changeling
    fields = [
        "name",
        "description",
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
        "willpower",
        "age",
        "apparent_age",
        "history",
        "goals",
        "notes",
        "kenning",
        "leadership",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "gremayre",
        "law",
        "politics",
        "technology",
        "court",
        "seeming",
        "autumn",
        "chicanery",
        "chronos",
        "contract",
        "dragons_ire",
        "legerdemain",
        "metamorphosis",
        "naming",
        "oneiromancy",
        "primal",
        "pyretics",
        "skycraft",
        "soothsay",
        "sovereign",
        "spring",
        "summer",
        "wayfare",
        "winter",
        "actor",
        "fae",
        "nature_realm",
        "prop",
        "scene",
        "time",
        "banality",
        "glamour",
        "musing_threshold",
        "ravaging_threshold",
        "antithesis",
        "true_name",
        "date_ennobled",
        "crysalis",
        "date_of_crysalis",
        "fae_mien",
    ]
    template_name = "characters/changeling/changeling/form.html"
    success_message = "Changeling '{name}' updated successfully!"
    error_message = "Failed to update changeling. Please correct the errors below."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context


class ChangelingBasicsView(LoginRequiredMixin, FormView):
    form_class = ChangelingCreationForm
    template_name = "characters/changeling/changeling/basics.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = False
        if self.request.user.profile.is_st():
            context["storyteller"] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            f"Changeling '{self.object.name}' created successfully! Continue with character creation."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors in the form below."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ChangelingAttributeView(HumanAttributeView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context


class ChangelingAbilityView(CtDHumanAbilityView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class ChangelingBackgroundsView(HumanBackgroundsView):
    template_name = "characters/changeling/changeling/chargen.html"


class ChangelingArtsRealmsView(SpecialUserMixin, UpdateView):
    model = Changeling
    fields = [
        "autumn",
        "chicanery",
        "chronos",
        "contract",
        "dragons_ire",
        "legerdemain",
        "metamorphosis",
        "naming",
        "oneiromancy",
        "primal",
        "pyretics",
        "skycraft",
        "soothsay",
        "sovereign",
        "spring",
        "summer",
        "wayfare",
        "winter",
        "actor",
        "fae",
        "nature_realm",
        "prop",
        "scene",
        "time",
    ]
    template_name = "characters/changeling/changeling/chargen.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context

    def form_valid(self, form):
        # Get all arts values
        arts = {
            "autumn": form.cleaned_data.get("autumn", 0),
            "chicanery": form.cleaned_data.get("chicanery", 0),
            "chronos": form.cleaned_data.get("chronos", 0),
            "contract": form.cleaned_data.get("contract", 0),
            "dragons_ire": form.cleaned_data.get("dragons_ire", 0),
            "legerdemain": form.cleaned_data.get("legerdemain", 0),
            "metamorphosis": form.cleaned_data.get("metamorphosis", 0),
            "naming": form.cleaned_data.get("naming", 0),
            "oneiromancy": form.cleaned_data.get("oneiromancy", 0),
            "primal": form.cleaned_data.get("primal", 0),
            "pyretics": form.cleaned_data.get("pyretics", 0),
            "skycraft": form.cleaned_data.get("skycraft", 0),
            "soothsay": form.cleaned_data.get("soothsay", 0),
            "sovereign": form.cleaned_data.get("sovereign", 0),
            "spring": form.cleaned_data.get("spring", 0),
            "summer": form.cleaned_data.get("summer", 0),
            "wayfare": form.cleaned_data.get("wayfare", 0),
            "winter": form.cleaned_data.get("winter", 0),
        }

        # Get all realms values
        realms = {
            "actor": form.cleaned_data.get("actor", 0),
            "fae": form.cleaned_data.get("fae", 0),
            "nature_realm": form.cleaned_data.get("nature_realm", 0),
            "prop": form.cleaned_data.get("prop", 0),
            "scene": form.cleaned_data.get("scene", 0),
            "time": form.cleaned_data.get("time", 0),
        }

        # Validate arts total is 3
        total_arts = sum(arts.values())
        if total_arts != 3:
            form.add_error(None, f"Arts must total 3 dots (currently {total_arts})")
            messages.error(self.request, f"Arts allocation error: You must spend exactly 3 dots. You have {total_arts}.")
            return self.form_invalid(form)

        # Validate realms total is 5
        total_realms = sum(realms.values())
        if total_realms != 5:
            form.add_error(None, f"Realms must total 5 dots (currently {total_realms})")
            messages.error(self.request, f"Realms allocation error: You must spend exactly 5 dots. You have {total_realms}.")
            return self.form_invalid(form)

        # Validate individual values don't exceed 5
        for art_name, value in arts.items():
            if value > 5:
                form.add_error(art_name, "Cannot exceed 5 dots")
                messages.error(self.request, f"{art_name.replace('_', ' ').title()} cannot exceed 5 dots.")
                return self.form_invalid(form)

        for realm_name, value in realms.items():
            if value > 5:
                form.add_error(realm_name, "Cannot exceed 5 dots")
                messages.error(self.request, f"{realm_name.replace('_', ' ').title()} cannot exceed 5 dots.")
                return self.form_invalid(form)

        # All validations passed, increment creation_status and save
        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Arts and Realms allocated successfully!")
        return super().form_valid(form)


class ChangelingExtrasView(SpecialUserMixin, UpdateView):
    model = Changeling
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
        "true_name",
        "crysalis",
        "date_of_crysalis",
        "fae_mien",
        "antithesis",
        "musing_threshold",
        "ravaging_threshold",
    ]
    template_name = "characters/changeling/changeling/chargen.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Character details saved successfully!")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["date_of_birth"].required = False
        form.fields["date_of_crysalis"].widget = forms.DateInput(
            attrs={"type": "date"}
        )
        form.fields["date_of_crysalis"].required = False
        form.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's physical appearance. Be detailed, this will be visible to other players."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory. Include information about their mortal life and their Chrysalis."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {
                "placeholder": "Describe your character's long and short term goals."
            }
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "This will be displayed to all players who look at your character."
            }
        )
        form.fields["true_name"].widget.attrs.update(
            {"placeholder": "Your character's fae true name"}
        )
        form.fields["crysalis"].widget.attrs.update(
            {
                "placeholder": "Describe your character's Chrysalis - how they awakened to their fae nature."
            }
        )
        form.fields["fae_mien"].widget.attrs.update(
            {"placeholder": "Describe your character's fae appearance."}
        )
        form.fields["antithesis"].widget.attrs.update(
            {
                "placeholder": "What is your character's Antithesis? What causes them to gain Banality?"
            }
        )
        return form


class ChangelingFreebiesView(HumanFreebiesView):
    model = Changeling
    form_class = HumanFreebiesForm
    template_name = "characters/changeling/changeling/chargen.html"

    def get_category_functions(self):
        d = super().get_category_functions()
        d.update(
            {
                "art": self.object.art_freebies,
                "realm": self.object.realm_freebies,
                "glamour": self.object.glamour_freebies,
            }
        )
        return d


class ChangelingFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Changeling
    template_name = "characters/core/human/load_examples_dropdown_list.html"

    def category_method_map(self):
        base_map = super().category_method_map()
        base_map.update(
            {
                "Art": self.art_options,
                "Realm": self.realm_options,
                "Glamour": self.glamour_options,
            }
        )
        return base_map

    def art_options(self):
        """Return all arts that are below 5 dots"""
        arts = [
            "autumn",
            "chicanery",
            "chronos",
            "contract",
            "dragons_ire",
            "legerdemain",
            "metamorphosis",
            "naming",
            "oneiromancy",
            "primal",
            "pyretics",
            "skycraft",
            "soothsay",
            "sovereign",
            "spring",
            "summer",
            "wayfare",
            "winter",
        ]
        return [
            Statistic.objects.get(property_name=art)
            for art in arts
            if getattr(self.character, art, 0) < 5
        ]

    def realm_options(self):
        """Return all realms that are below 5 dots"""
        realms = ["actor", "fae", "nature_realm", "prop", "scene", "time"]
        return [
            Statistic.objects.get(property_name=realm)
            for realm in realms
            if getattr(self.character, realm, 0) < 5
        ]

    def glamour_options(self):
        """Glamour doesn't use options"""
        return []


class ChangelingLanguagesView(EditPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/changeling/changeling/chargen.html"

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Changeling, pk=kwargs.get("pk"))
        if "Language" not in obj.merits_and_flaws.values_list("name", flat=True):
            obj.languages.add(Language.objects.get(name="English"))
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        changeling_pk = self.kwargs.get("pk")
        num_languages = Changeling.objects.get(pk=changeling_pk).num_languages()
        kwargs.update({"pk": changeling_pk, "num_languages": int(num_languages)})
        return kwargs

    def form_valid(self, form):
        changeling_pk = self.kwargs.get("pk")
        changeling = get_object_or_404(Changeling, pk=changeling_pk)
        num_languages = changeling.num_languages()
        changeling.languages.add(Language.objects.get(name="English"))
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i+1}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                changeling.languages.add(language)
        changeling.creation_status += 1
        changeling.save()
        messages.success(self.request, "Languages added successfully!")
        return HttpResponseRedirect(changeling.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Changeling, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context


class ChangelingSpecialtiesView(EditPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/changeling/changeling/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = Changeling.objects.get(id=self.kwargs["pk"])
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        changeling = Changeling.objects.get(id=self.kwargs["pk"])
        kwargs["object"] = changeling
        kwargs["specialties_needed"] = changeling.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        changeling = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            changeling.specialties.add(spec)
        changeling.status = "Sub"
        changeling.save()
        messages.success(self.request, f"Changeling '{changeling.name}' submitted for approval!")
        return HttpResponseRedirect(changeling.get_absolute_url())


class ChangelingCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: ChangelingAttributeView,
        2: ChangelingAbilityView,
        3: ChangelingBackgroundsView,
        4: ChangelingArtsRealmsView,
        5: ChangelingExtrasView,
        6: ChangelingFreebiesView,
        7: ChangelingLanguagesView,
        8: ChangelingSpecialtiesView,
    }
    model_class = Changeling
    key_property = "creation_status"
    default_redirect = ChangelingDetailView
