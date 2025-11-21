from typing import Any

from characters.forms.changeling.ctdhuman import CtDHumanCreationForm
from characters.forms.core.ally import AllyForm
from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAbilityView,
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
)
from core.forms.language import HumanLanguageForm
from core.models import Language
from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, UpdateView


class CtDHumanDetailView(SpecialUserMixin, DetailView):
    model = CtDHuman
    template_name = "characters/changeling/ctdhuman/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class CtDHumanCreateView(MessageMixin, CreateView):
    model = CtDHuman
    success_message = "CtD Human created successfully."
    error_message = "Error creating CtD Human."
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
    ]
    template_name = "characters/changeling/ctdhuman/form.html"


class CtDHumanUpdateView(MessageMixin, SpecialUserMixin, UpdateView):
    model = CtDHuman
    success_message = "CtD Human updated successfully."
    error_message = "Error updating CtD Human."
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
    ]
    template_name = "characters/changeling/ctdhuman/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class CtDHumanBasicsView(LoginRequiredMixin, FormView):
    form_class = CtDHumanCreationForm
    template_name = "characters/changeling/ctdhuman/basics.html"

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


class CtDHumanAttributeView(HumanAttributeView):
    model = CtDHuman
    template_name = "characters/changeling/ctdhuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class CtDHumanAbilityView(HumanAbilityView):
    model = CtDHuman
    fields = CtDHuman.primary_abilities
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanExtrasView(SpecialUserMixin, UpdateView):
    model = CtDHuman
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
    template_name = "characters/changeling/ctdhuman/chargen.html"

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
                "placeholder": "Describe your character's physical appeareance. Be detailed, this will be visible to other players."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with changeling society since, particularly mentioning important backgrounds."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {
                "placeholder": "Describe your character's long and short term goals, whether personal, professional, or magical."
            }
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
            }
        )
        return form


class CtDHumanFreebiesView(HumanFreebiesView):
    model = CtDHuman
    form_class = HumanFreebiesForm
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = CtDHuman
    template_name = "characters/core/human/load_examples_dropdown_list.html"


class CtDHumanLanguagesView(SpecialUserMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/changeling/ctdhuman/chargen.html"

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Human, pk=kwargs.get("pk"))
        if "Language" not in obj.merits_and_flaws.values_list("name", flat=True):
            obj.languages.add(Language.objects.get(name="English"))
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    # Overriding `get_form_kwargs` to pass custom arguments to the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        human_pk = self.kwargs.get("pk")
        num_languages = Human.objects.get(pk=human_pk).num_languages()
        kwargs.update({"pk": human_pk, "num_languages": int(num_languages)})
        return kwargs

    # Overriding `form_valid` to handle saving the data
    def form_valid(self, form):
        # Get the human instance from the pased `pk`
        human_pk = self.kwargs.get("pk")
        human = get_object_or_404(Human, pk=human_pk)
        num_languages = human.num_languages()
        human.languages.add(Language.objects.get(name="English"))
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i+1}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                human.languages.add(language)
        human.creation_status += 1
        human.save()
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context


class CtDHumanAlliesView(GenericBackgroundView):
    primary_object_class = CtDHuman
    background_name = "allies"
    form_class = AllyForm
    template_name = "characters/changeling/ctdhuman/chargen.html"


class CtDHumanSpecialtiesView(SpecialUserMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/changeling/ctdhuman/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = CtDHuman.objects.get(id=self.kwargs["pk"])
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        changeling = CtDHuman.objects.get(id=self.kwargs["pk"])
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
        return HttpResponseRedirect(changeling.get_absolute_url())


class CtDHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: CtDHumanAttributeView,
        2: CtDHumanAbilityView,
        3: CtDHumanBackgroundsView,
        4: CtDHumanExtrasView,
        5: CtDHumanFreebiesView,
        6: CtDHumanLanguagesView,
        7: CtDHumanAlliesView,
        8: CtDHumanSpecialtiesView,
    }
    model_class = CtDHuman
    key_property = "creation_status"
    default_redirect = CtDHumanDetailView
