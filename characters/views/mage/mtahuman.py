from typing import Any

from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.mage.mtahuman import MtAHumanCreationForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import (
    Background,
    BackgroundRating,
    PooledBackgroundRating,
)
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from characters.models.mage.faction import MageFaction
from characters.models.mage.mtahuman import MtAHuman
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
)
from characters.views.mage.background_views import MtAEnhancementView
from core.forms.language import HumanLanguageForm
from core.models import CharacterTemplate, Language
from core.mixins import ViewPermissionMixin, EditPermissionMixin, SpendFreebiesPermissionMixin, SpendXPPermissionMixin
from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
from core.models import Language
from core.mixins import ViewPermissionMixin, EditPermissionMixin, SpendFreebiesPermissionMixin, SpendXPPermissionMixin, ApprovedUserContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, UpdateView
from items.forms.mage.wonder import WonderForm
from locations.forms.mage.chantry import ChantrySelectOrCreateForm
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


class MtAHumanDetailView(ApprovedUserContextMixin, HumanDetailView):
    model = MtAHuman
    template_name = "characters/mage/mtahuman/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MtAHumanCreateView(MessageMixin, CreateView):
    model = MtAHuman
    success_message = "MtA Human created successfully."
    error_message = "Error creating MtA Human."
    fields = [
        "name",
        "owner",
        "description",
        "nature",
        "demeanor",
        "specialties",
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
        "awareness",
        "art",
        "leadership",
        "animal_kinship",
        "blatancy",
        "carousing",
        "flying",
        "high_ritual",
        "lucid_dreaming",
        "search",
        "seduction",
        "larceny",
        "meditation",
        "research",
        "survival",
        "technology",
        "acrobatics",
        "archery",
        "biotech",
        "energy_weapons",
        "jetpack",
        "riding",
        "torture",
        "cosmology",
        "enigmas",
        "finance",
        "law",
        "occult",
        "politics",
        "area_knowledge",
        "belief_systems",
        "cryptography",
        "demolitions",
        "lore",
        "media",
        "pharmacopeia",
        "cooking",
        "diplomacy",
        "instruction",
        "intrigue",
        "intuition",
        "mimicry",
        "negotiation",
        "newspeak",
        "scan",
        "scrounging",
        "style",
        "blind_fighting",
        "climbing",
        "disguise",
        "elusion",
        "escapology",
        "fast_draw",
        "fast_talk",
        "fencing",
        "fortune_telling",
        "gambling",
        "gunsmith",
        "heavy_weapons",
        "hunting",
        "hypnotism",
        "jury_rigging",
        "microgravity_operations",
        "misdirection",
        "networking",
        "pilot",
        "psychology",
        "security",
        "speed_reading",
        "swimming",
        "conspiracy_theory",
        "chantry_politics",
        "covert_culture",
        "cultural_savvy",
        "helmsman",
        "history_knowledge",
        "power_brokering",
        "propaganda",
        "theology",
        "unconventional_warface",
        "vice",
    ]
    template_name = "characters/mage/mtahuman/form.html"


class MtAHumanUpdateView(EditPermissionMixin, UpdateView):
    model = MtAHuman
    success_message = "MtA Human updated successfully."
    error_message = "Error updating MtA Human."
    fields = [
        "name",
        "owner",
        "description",
        "nature",
        "demeanor",
        "specialties",
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
        "awareness",
        "art",
        "leadership",
        "animal_kinship",
        "blatancy",
        "carousing",
        "flying",
        "high_ritual",
        "lucid_dreaming",
        "search",
        "seduction",
        "larceny",
        "meditation",
        "research",
        "survival",
        "technology",
        "acrobatics",
        "archery",
        "biotech",
        "energy_weapons",
        "jetpack",
        "riding",
        "torture",
        "cosmology",
        "enigmas",
        "finance",
        "law",
        "occult",
        "politics",
        "area_knowledge",
        "belief_systems",
        "cryptography",
        "demolitions",
        "lore",
        "media",
        "pharmacopeia",
        "cooking",
        "diplomacy",
        "instruction",
        "intrigue",
        "intuition",
        "mimicry",
        "negotiation",
        "newspeak",
        "scan",
        "scrounging",
        "style",
        "blind_fighting",
        "climbing",
        "disguise",
        "elusion",
        "escapology",
        "fast_draw",
        "fast_talk",
        "fencing",
        "fortune_telling",
        "gambling",
        "gunsmith",
        "heavy_weapons",
        "hunting",
        "hypnotism",
        "jury_rigging",
        "microgravity_operations",
        "misdirection",
        "networking",
        "pilot",
        "psychology",
        "security",
        "speed_reading",
        "swimming",
        "conspiracy_theory",
        "chantry_politics",
        "covert_culture",
        "cultural_savvy",
        "helmsman",
        "history_knowledge",
        "power_brokering",
        "propaganda",
        "theology",
        "unconventional_warface",
        "vice",
    ]
    template_name = "characters/mage/mtahuman/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MtAHumanAbilityView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = MtAHuman
    fields = [
        "awareness",
        "art",
        "leadership",
        "larceny",
        "meditation",
        "research",
        "survival",
        "technology",
        "cosmology",
        "enigmas",
        "finance",
        "law",
        "occult",
        "politics",
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
    ]
    template_name = "characters/mage/mtahuman/chargen.html"

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
        awareness = form.cleaned_data.get("awareness")
        art = form.cleaned_data.get("art")
        leadership = form.cleaned_data.get("leadership")
        larceny = form.cleaned_data.get("larceny")
        meditation = form.cleaned_data.get("meditation")
        research = form.cleaned_data.get("research")
        survival = form.cleaned_data.get("survival")
        technology = form.cleaned_data.get("technology")
        cosmology = form.cleaned_data.get("cosmology")
        enigmas = form.cleaned_data.get("enigmas")
        finance = form.cleaned_data.get("finance")
        law = form.cleaned_data.get("law")
        occult = form.cleaned_data.get("occult")
        politics = form.cleaned_data.get("politics")
        alertness = form.cleaned_data.get("alertness")
        athletics = form.cleaned_data.get("athletics")
        brawl = form.cleaned_data.get("brawl")
        empathy = form.cleaned_data.get("empathy")
        expression = form.cleaned_data.get("expression")
        intimidation = form.cleaned_data.get("intimidation")
        streetwise = form.cleaned_data.get("streetwise")
        subterfuge = form.cleaned_data.get("subterfuge")
        crafts = form.cleaned_data.get("crafts")
        drive = form.cleaned_data.get("drive")
        etiquette = form.cleaned_data.get("etiquette")
        firearms = form.cleaned_data.get("firearms")
        melee = form.cleaned_data.get("melee")
        stealth = form.cleaned_data.get("stealth")
        academics = form.cleaned_data.get("academics")
        computer = form.cleaned_data.get("computer")
        investigation = form.cleaned_data.get("investigation")
        medicine = form.cleaned_data.get("medicine")
        science = form.cleaned_data.get("science")

        for ability in [
            awareness,
            art,
            leadership,
            larceny,
            meditation,
            research,
            survival,
            technology,
            cosmology,
            enigmas,
            finance,
            law,
            occult,
            politics,
            alertness,
            athletics,
            brawl,
            empathy,
            expression,
            intimidation,
            streetwise,
            subterfuge,
            crafts,
            drive,
            etiquette,
            firearms,
            melee,
            stealth,
            academics,
            computer,
            investigation,
            medicine,
            science,
        ]:
            if ability < 0 or ability > 3:
                form.add_error(None, "Abilities must range from 0-3")
                return self.form_invalid(form)

        triple = [
            alertness
            + art
            + athletics
            + awareness
            + brawl
            + empathy
            + expression
            + intimidation
            + leadership
            + streetwise
            + subterfuge,
            crafts
            + drive
            + etiquette
            + firearms
            + larceny
            + meditation
            + melee
            + research
            + stealth
            + survival
            + technology,
            academics
            + computer
            + cosmology
            + enigmas
            + finance
            + investigation
            + law
            + medicine
            + occult
            + politics
            + science,
        ]
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


class MtAHumanBasicsView(LoginRequiredMixin, FormView):
    form_class = MtAHumanCreationForm
    template_name = "characters/mage/mtahuman/basics.html"

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
        return reverse("characters:mage:mtahuman_template", kwargs={"pk": self.object.pk})


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
                gameline="mta", character_type="mage", is_public=True
            ).order_by("name")


class MtAHumanTemplateSelectView(LoginRequiredMixin, FormView):
    """Step 0.5: Optional template selection after basics"""

    form_class = CharacterTemplateSelectionForm
    template_name = "characters/mage/mtahuman/template_select.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            MtAHuman, pk=kwargs["pk"], owner=request.user
        )
        # Only allow template selection if character creation hasn't started yet
        if self.object.creation_status > 0:
            return redirect("characters:mage:mtahuman_creation", pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object
        context["available_templates"] = CharacterTemplate.objects.filter(
            gameline="mta", character_type="mage", is_public=True
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
            messages.info(
                self.request, "Starting with blank character. Fill in all attributes."
            )

        # Set creation_status to 1 to proceed to attribute allocation
        self.object.creation_status = 1
        self.object.save()

        return redirect("characters:mage:mtahuman_creation", pk=self.object.pk)


class MtAHumanAttributeView(ApprovedUserContextMixin, HumanAttributeView):
    model = MtAHuman
    template_name = "characters/mage/mtahuman/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MtAHumanBackgroundsView(HumanBackgroundsView):
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanExtrasView(ApprovedUserContextMixin, SpecialUserMixin, UpdateView):
    model = MtAHuman
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
    template_name = "characters/mage/mtahuman/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
                "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with mage society since, particularly mentioning important backgrounds."
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


class MtAHumanFreebiesView(HumanFreebiesView):
    model = MtAHuman
    form_class = HumanFreebiesForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = MtAHuman
    template_name = "characters/core/human/load_examples_dropdown_list.html"


class MtAHumanLanguagesView(EditPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/mage/mtahuman/chargen.html"

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


class MtAHumanAlliesView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanEnhancementView(MtAEnhancementView):
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanLibraryView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "library"
    form_class = LibraryForm
    template_name = "characters/mage/mtahuman/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        form.fields["name"].initial = (
            self.current_background.note or f"{obj.name}'s Library"
        )
        form.fields["faction"].queryset = MageFaction.objects.all()
        return form


class MtAHumanNodeView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "node"
    form_class = NodeForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanSpecialtiesView(EditPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/mage/mtahuman/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = MtAHuman.objects.get(id=self.kwargs["pk"])
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        mage = MtAHuman.objects.get(id=self.kwargs["pk"])
        kwargs["object"] = mage
        kwargs["specialties_needed"] = mage.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        mage = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            mage.specialties.add(spec)
        mage.status = "Sub"
        mage.save()
        return HttpResponseRedirect(mage.get_absolute_url())


class MtAHumanWonderView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "wonder"
    potential_skip = [
        "enhancement",
        "sanctum",
        "allies",
    ]
    form_class = WonderForm
    template_name = "characters/mage/mtahuman/chargen.html"
    multiple_ownership = True


class MtAHumanSanctumView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "sanctum"
    potential_skip = [
        "allies",
    ]
    form_class = SanctumForm
    template_name = "characters/mage/mtahuman/chargen.html"


class MtAHumanChantryView(GenericBackgroundView):
    primary_object_class = MtAHuman
    background_name = "chantry"
    form_class = ChantrySelectOrCreateForm
    template_name = "characters/mage/mtahuman/chargen.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.primary_object_class.objects.get(
            pk=self.kwargs["pk"]
        )
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.chantry_creation_form.fields[
            "total_points"
        ].initial = self.current_background.rating
        form.chantry_creation_form.fields["total_points"].widget.attrs.update(
            {
                "min": self.current_background.rating,
                "max": self.current_background.rating,
            }
        )
        return form


class MtAHumanCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: MtAHumanAttributeView,
        2: MtAHumanAbilityView,
        3: MtAHumanBackgroundsView,
        4: MtAHumanExtrasView,
        5: MtAHumanFreebiesView,
        6: MtAHumanLanguagesView,
        7: MtAHumanNodeView,
        8: MtAHumanLibraryView,
        9: MtAHumanWonderView,
        10: MtAHumanEnhancementView,
        11: MtAHumanSanctumView,
        12: MtAHumanAlliesView,
        13: MtAHumanChantryView,
        14: MtAHumanSpecialtiesView,
    }
    model_class = MtAHuman
    key_property = "creation_status"
    default_redirect = MtAHumanDetailView
