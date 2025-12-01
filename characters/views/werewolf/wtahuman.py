from typing import Any

from characters.forms.changeling.ctdhuman import CtDHumanCreationForm
from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.werewolf.wtahuman import WtAHumanCreationForm
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.models.werewolf.wtahuman import WtAHuman
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
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from core.models import CharacterTemplate, Language
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, UpdateView


class WtAHumanDetailView(HumanDetailView):
    model = WtAHuman
    template_name = "characters/werewolf/wtahuman/detail.html"


class WtAHumanCreateView(MessageMixin, CreateView):
    model = WtAHuman
    success_message = "WtA Human created successfully."
    error_message = "Error creating WtA Human."
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
    ]
    template_name = "characters/werewolf/wtahuman/form.html"


class WtAHumanUpdateView(EditPermissionMixin, UpdateView):
    model = WtAHuman
    success_message = "WtA Human updated successfully."
    error_message = "Error updating WtA Human."
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
    ]
    template_name = "characters/werewolf/wtahuman/form.html"


class WtAHumanBasicsView(LoginRequiredMixin, FormView):
    form_class = WtAHumanCreationForm
    template_name = "characters/werewolf/wtahuman/basics.html"

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
        return reverse("characters:werewolf:wtahuman_template", kwargs={"pk": self.object.pk})


class CharacterTemplateSelectionForm(forms.Form):
    """Form for selecting optional character template"""

    template = forms.ModelChoiceField(
        queryset=CharacterTemplate.objects.none(),
        required=False,
        empty_label="No template - build from scratch",
        widget=forms.RadioSelect,
        help_text="Select a pre-made character concept to speed up creation",
    )

    def __init__(self, *args, character=None, **kwargs):
        super().__init__(*args, **kwargs)
        if character:
            self.fields["template"].queryset = CharacterTemplate.objects.filter(
                gameline="wta", character_type="werewolf", is_public=True
            ).order_by("name")


class WtAHumanTemplateSelectView(LoginRequiredMixin, FormView):
    """Step 0.5: Optional template selection after basics"""

    form_class = CharacterTemplateSelectionForm
    template_name = "characters/werewolf/wtahuman/template_select.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(WtAHuman, pk=kwargs["pk"], owner=request.user)
        # Only allow template selection if character creation hasn't started yet
        if self.object.creation_status > 0:
            return redirect("characters:werewolf:wtahuman_creation", pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object
        context["available_templates"] = CharacterTemplate.objects.filter(
            gameline="wta", character_type="werewolf", is_public=True
        ).order_by("name")
        return context

    def form_valid(self, form):
        template = form.cleaned_data.get("template")
        if template:
            # Apply template
            template.apply_to_character(self.object)
            messages.success(
                self.request,
                f"Applied template '{template.name}'. You can now customize the character further.",
            )
        else:
            messages.info(self.request, "Starting with blank character. Fill in all attributes.")

        # Set creation_status to 1 to proceed to attribute allocation
        self.object.creation_status = 1
        self.object.save()

        return redirect("characters:werewolf:wtahuman_creation", pk=self.object.pk)


class WtAHumanAttributeView(HumanAttributeView):
    model = WtAHuman
    template_name = "characters/werewolf/wtahuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class WtAHumanAbilityView(HumanAbilityView):
    model = WtAHuman
    fields = WtAHuman.primary_abilities
    template_name = "characters/werewolf/wtahuman/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4


class WtAHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanExtrasView(SpecialUserMixin, UpdateView):
    model = WtAHuman
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
    template_name = "characters/werewolf/wtahuman/chargen.html"

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
                "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with werewolf society since, particularly mentioning important backgrounds."
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


class WtAHumanFreebiesView(HumanFreebiesView):
    model = WtAHuman
    form_class = HumanFreebiesForm
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = WtAHuman
    template_name = "characters/core/human/load_examples_dropdown_list.html"


class WtAHumanLanguagesView(EditPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/werewolf/wtahuman/chargen.html"

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


class WtAHumanAlliesView(GenericBackgroundView):
    primary_object_class = WtAHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/wtahuman/chargen.html"


class WtAHumanSpecialtiesView(EditPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/werewolf/wtahuman/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = WtAHuman.objects.get(id=self.kwargs["pk"])
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        werewolf = WtAHuman.objects.get(id=self.kwargs["pk"])
        kwargs["object"] = werewolf
        kwargs["specialties_needed"] = werewolf.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        werewolf = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            werewolf.specialties.add(spec)
        werewolf.status = "Sub"
        werewolf.save()
        return HttpResponseRedirect(werewolf.get_absolute_url())


class WtAHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: WtAHumanAttributeView,
        2: WtAHumanAbilityView,
        3: WtAHumanBackgroundsView,
        4: WtAHumanExtrasView,
        5: WtAHumanFreebiesView,
        6: WtAHumanLanguagesView,
        7: WtAHumanAlliesView,
        8: WtAHumanSpecialtiesView,
    }
    model_class = WtAHuman
    key_property = "creation_status"
    default_redirect = WtAHumanDetailView
