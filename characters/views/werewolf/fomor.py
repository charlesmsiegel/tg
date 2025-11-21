from typing import Any

from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.werewolf.fomor import FomorCreationForm
from characters.models.core import Human
from characters.models.core.specialty import Specialty
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.fomoripower import FomoriPower
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
)
from characters.views.werewolf.wtahuman import WtAHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.models import Language
from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, UpdateView


class FomorDetailView(SpecialUserMixin, DetailView):
    model = Fomor
    template_name = "characters/werewolf/fomor/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class FomorCreateView(MessageMixin, CreateView):
    model = Fomor
    success_message = "Fomor created successfully."
    error_message = "Error creating fomor."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
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
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "leadership",
        "primal_urge",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "law",
        "occult",
        "rituals",
        "technology",
        "rage",
        "gnosis",
        "powers",
    ]
    template_name = "characters/werewolf/fomor/form.html"


class FomorUpdateView(MessageMixin, SpecialUserMixin, UpdateView):
    model = Fomor
    success_message = "Fomor updated successfully."
    error_message = "Error updating fomor."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
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
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "leadership",
        "primal_urge",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "law",
        "occult",
        "rituals",
        "technology",
        "rage",
        "gnosis",
        "powers",
    ]
    template_name = "characters/werewolf/fomor/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class FomorBasicsView(LoginRequiredMixin, FormView):
    form_class = FomorCreationForm
    template_name = "characters/werewolf/fomor/basics.html"

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
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class FomorAttributeView(HumanAttributeView):
    model = Fomor
    template_name = "characters/werewolf/fomor/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class FomorAbilityView(WtAHumanAbilityView):
    model = Fomor
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorPowersView(SpecialUserMixin, UpdateView):
    model = Fomor
    fields = ["powers", "rage", "gnosis"]
    template_name = "characters/werewolf/fomor/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["powers"].queryset = FomoriPower.objects.all()
        form.fields["powers"].required = False
        form.fields["powers"].help_text = (
            "Select the powers your Fomor possesses. Fomori typically have 1-3 powers."
        )
        form.fields["rage"].help_text = "Fomori typically have 1-5 Rage"
        form.fields["gnosis"].help_text = "Fomori typically have 1-5 Gnosis"
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


class FomorExtrasView(SpecialUserMixin, UpdateView):
    model = Fomor
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/werewolf/fomor/chargen.html"

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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's physical appearance. Be detailed, this will be visible to other players."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory. Include information about their transformation into a Fomor, how they gained their powers, and their relationship with the Wyrm."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {
                "placeholder": "Describe your character's goals and motivations."
            }
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "This will be displayed to all players who look at your character."
            }
        )
        return form


class FomorFreebiesView(HumanFreebiesView):
    model = Fomor
    form_class = HumanFreebiesForm
    template_name = "characters/werewolf/fomor/chargen.html"


class FomorFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Fomor
    template_name = "characters/core/human/load_examples_dropdown_list.html"


class FomorLanguagesView(SpecialUserMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/werewolf/fomor/chargen.html"

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Fomor, pk=kwargs.get("pk"))
        if "Language" not in obj.merits_and_flaws.values_list("name", flat=True):
            obj.languages.add(Language.objects.get(name="English"))
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        fomor_pk = self.kwargs.get("pk")
        num_languages = Fomor.objects.get(pk=fomor_pk).num_languages()
        kwargs.update({"pk": fomor_pk, "num_languages": int(num_languages)})
        return kwargs

    def form_valid(self, form):
        fomor_pk = self.kwargs.get("pk")
        fomor = get_object_or_404(Fomor, pk=fomor_pk)
        num_languages = fomor.num_languages()
        fomor.languages.add(Language.objects.get(name="English"))
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i+1}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                fomor.languages.add(language)
        fomor.creation_status += 1
        fomor.save()
        return HttpResponseRedirect(fomor.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Fomor, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context


class FomorSpecialtiesView(SpecialUserMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/werewolf/fomor/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = Fomor.objects.get(id=self.kwargs["pk"])
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        fomor = Fomor.objects.get(id=self.kwargs["pk"])
        kwargs["object"] = fomor
        kwargs["specialties_needed"] = fomor.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        fomor = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            fomor.specialties.add(spec)
        fomor.status = "Sub"
        fomor.save()
        return HttpResponseRedirect(fomor.get_absolute_url())


class FomorCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: FomorAttributeView,
        2: FomorAbilityView,
        3: FomorBackgroundsView,
        4: FomorPowersView,
        5: FomorExtrasView,
        6: FomorFreebiesView,
        7: FomorLanguagesView,
        8: FomorSpecialtiesView,
    }
    model_class = Fomor
    key_property = "creation_status"
    default_redirect = FomorDetailView
