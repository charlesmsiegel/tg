from typing import Any

from characters.forms.core.ally import AllyForm
from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.vampire.vtmhuman import VtMHumanCreationForm
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.models.vampire.vtmhuman import VtMHuman
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAbilityView,
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
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
from django.views.generic import CreateView, FormView, UpdateView


class VtMHumanDetailView(HumanDetailView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class VtMHumanCreateView(MessageMixin, CreateView):
    model = VtMHuman
    success_message = "VtM Human created successfully."
    error_message = "Error creating VtM Human."
    fields = [
        "name",
        "owner",
        "description",
        "nature",
        "demeanor",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
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
        "xp",
        "awareness",
        "leadership",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
    ]
    template_name = "characters/vampire/vtmhuman/form.html"


class VtMHumanUpdateView(MessageMixin, SpecialUserMixin, UpdateView):
    model = VtMHuman
    success_message = "VtM Human updated successfully."
    error_message = "Error updating VtM Human."
    fields = [
        "name",
        "owner",
        "description",
        "nature",
        "demeanor",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
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
        "xp",
        "awareness",
        "leadership",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
    ]
    template_name = "characters/vampire/vtmhuman/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class VtMHumanBasicsView(LoginRequiredMixin, FormView):
    form_class = VtMHumanCreationForm
    template_name = "characters/vampire/vtmhuman/basics.html"

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


class VtMHumanAttributeView(HumanAttributeView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class VtMHumanAbilityView(HumanAbilityView):
    model = VtMHuman
    fields = VtMHuman.primary_abilities
    template_name = "characters/vampire/vtmhuman/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4


class VtMHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanExtrasView(SpecialUserMixin, UpdateView):
    model = VtMHuman
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
    template_name = "characters/vampire/vtmhuman/chargen.html"

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
                "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with vampire society since, particularly mentioning important backgrounds."
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


class VtMHumanFreebiesView(HumanFreebiesView):
    model = VtMHuman
    form_class = HumanFreebiesForm
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = VtMHuman
    template_name = "characters/core/human/load_examples_dropdown_list.html"


class VtMHumanLanguagesView(SpecialUserMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/vampire/vtmhuman/chargen.html"

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


class VtMHumanAlliesView(GenericBackgroundView):
    primary_object_class = VtMHuman
    background_name = "allies"
    form_class = AllyForm
    template_name = "characters/vampire/vtmhuman/chargen.html"


class VtMHumanSpecialtiesView(SpecialUserMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/vampire/vtmhuman/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = VtMHuman.objects.get(id=self.kwargs["pk"])
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        vampire = VtMHuman.objects.get(id=self.kwargs["pk"])
        kwargs["object"] = vampire
        kwargs["specialties_needed"] = vampire.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        vampire = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            vampire.specialties.add(spec)
        vampire.status = "Sub"
        vampire.save()
        return HttpResponseRedirect(vampire.get_absolute_url())


class VtMHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: VtMHumanAttributeView,
        2: VtMHumanAbilityView,
        3: VtMHumanBackgroundsView,
        4: VtMHumanExtrasView,
        5: VtMHumanFreebiesView,
        6: VtMHumanLanguagesView,
        7: VtMHumanAlliesView,
        8: VtMHumanSpecialtiesView,
    }
    model_class = VtMHuman
    key_property = "creation_status"
    default_redirect = VtMHumanDetailView
