from typing import Any

from characters.forms.changeling.ctdhuman import CtDHumanCreationForm
from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.wraith.wtohuman import WtOHumanCreationForm
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.models.wraith.wtohuman import WtOHuman
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
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


class WtOHumanDetailView(HumanDetailView):
    model = WtOHuman
    template_name = "characters/wraith/wtohuman/detail.html"


class WtOHumanCreateView(MessageMixin, CreateView):
    model = WtOHuman
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
        "awareness",
        "persuasion",
        "larceny",
        "meditation",
        "performance",
        "bureaucracy",
        "enigmas",
        "occult",
        "politics",
        "technology",
    ]
    template_name = "characters/wraith/wtohuman/form.html"
    success_message = "Wraith Human '{name}' created successfully!"
    error_message = "Failed to create wraith human. Please correct the errors below."


class WtOHumanUpdateView(EditPermissionMixin, UpdateView):
    model = WtOHuman
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
        "awareness",
        "persuasion",
        "larceny",
        "meditation",
        "performance",
        "bureaucracy",
        "enigmas",
        "occult",
        "politics",
        "technology",
    ]
    template_name = "characters/wraith/wtohuman/form.html"
    success_message = "Wraith Human '{name}' updated successfully!"
    error_message = "Failed to update wraith human. Please correct the errors below."


class WtOHumanBasicsView(LoginRequiredMixin, FormView):
    form_class = WtOHumanCreationForm
    template_name = "characters/wraith/wtohuman/basics.html"

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
            f"Wraith Human '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("characters:wraith:wtohuman_template", kwargs={"pk": self.object.pk})


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
                gameline="wto", character_type="wraith", is_public=True
            ).order_by("name")


class WtOHumanTemplateSelectView(LoginRequiredMixin, FormView):
    """Step 0.5: Optional template selection after basics"""

    form_class = CharacterTemplateSelectionForm
    template_name = "characters/wraith/wtohuman/template_select.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(WtOHuman, pk=kwargs["pk"], owner=request.user)
        # Only allow template selection if character creation hasn't started yet
        if self.object.creation_status > 0:
            return redirect("characters:wraith:wtohuman_creation", pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object
        context["available_templates"] = CharacterTemplate.objects.filter(
            gameline="wto", character_type="wraith", is_public=True
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

        return redirect("characters:wraith:wtohuman_creation", pk=self.object.pk)


class WtOHumanAttributeView(HumanAttributeView):
    model = WtOHuman
    template_name = "characters/wraith/wtohuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class WtOHumanAbilityView(SpecialUserMixin, UpdateView):
    model = WtOHuman
    fields = WtOHuman.primary_abilities
    template_name = "characters/wraith/wtohuman/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4

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
                messages.error(self.request, "All abilities must be between 0 and 3 dots.")
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
            messages.error(
                self.request,
                f"Abilities must be distributed {self.primary}/{self.secondary}/{self.tertiary}. Current: {talents} talents, {skills} skills, {knowledges} knowledges.",
            )
            return self.form_invalid(form)
        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Abilities allocated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WtOHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/wraith/wtohuman/chargen.html"


class WtOHumanExtrasView(SpecialUserMixin, UpdateView):
    model = WtOHuman
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
    template_name = "characters/wraith/wtohuman/chargen.html"

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Character details saved successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

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
                "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with wraith society since, particularly mentioning important backgrounds."
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


class WtOHumanFreebiesView(HumanFreebiesView):
    model = WtOHuman
    form_class = HumanFreebiesForm
    template_name = "characters/wraith/wtohuman/chargen.html"


class WtOHumanFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = WtOHuman


class WtOHumanLanguagesView(EditPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/wraith/wtohuman/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Human, pk=kwargs.get("pk"))
        if "Language" not in obj.merits_and_flaws.values_list("name", flat=True):
            english, _ = Language.objects.get_or_create(name="English")
            obj.languages.add(english)
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
        english, _ = Language.objects.get_or_create(name="English")
        human.languages.add(english)
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i+1}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                human.languages.add(language)
        human.creation_status += 1
        human.save()
        messages.success(self.request, "Languages added successfully!")
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context


class WtOHumanAlliesView(GenericBackgroundView):
    primary_object_class = WtOHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wtohuman/chargen.html"


class WtOHumanSpecialtiesView(EditPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/wraith/wtohuman/chargen.html"

    def get_object(self):
        """Return the WtOHuman object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = WtOHuman.objects.get(id=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        wraith = WtOHuman.objects.get(id=self.kwargs["pk"])
        kwargs["object"] = wraith
        kwargs["specialties_needed"] = wraith.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        wraith = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            wraith.specialties.add(spec)
        wraith.status = "Sub"
        wraith.save()
        messages.success(self.request, f"Wraith Human '{wraith.name}' submitted for approval!")
        return HttpResponseRedirect(wraith.get_absolute_url())


class WtOHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: WtOHumanAttributeView,
        2: WtOHumanAbilityView,
        3: WtOHumanBackgroundsView,
        4: WtOHumanExtrasView,
        5: WtOHumanFreebiesView,
        6: WtOHumanLanguagesView,
        7: WtOHumanAlliesView,
        8: WtOHumanSpecialtiesView,
    }
    model_class = WtOHuman
    key_property = "creation_status"
    default_redirect = WtOHumanDetailView
