from typing import Any

from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.werewolf.garou import (
    WerewolfCreationForm,
    WerewolfGiftsForm,
    WerewolfHistoryForm,
)
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift, GiftPermission
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
from characters.views.werewolf.wtahuman import WtAHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
    XPApprovalMixin,
)
from core.models import Language
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, UpdateView
from items.models.werewolf.fetish import Fetish


class WerewolfDetailView(XPApprovalMixin, ViewPermissionMixin, DetailView):
    model = Werewolf
    template_name = "characters/werewolf/garou/detail.html"


class WerewolfUpdateView(EditPermissionMixin, UpdateView):
    model = Werewolf
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
        "rank",
        "auspice",
        "breed",
        "tribe",
        "camps",
        "gnosis",
        "rage",
        "glory",
        "temporary_glory",
        "wisdom",
        "temporary_wisdom",
        "honor",
        "temporary_honor",
        "gifts",
        "rites_known",
        "fetishes_owned",
        "first_change",
        "battle_scars",
        "age_of_first_change",
    ]
    template_name = "characters/werewolf/garou/form.html"
    success_message = "Werewolf '{name}' updated successfully!"
    error_message = "Failed to update werewolf. Please correct the errors below."


class WerewolfCreateView(MessageMixin, CreateView):
    model = Werewolf
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
        "rank",
        "auspice",
        "breed",
        "tribe",
        "camps",
        "gnosis",
        "rage",
        "glory",
        "temporary_glory",
        "wisdom",
        "temporary_wisdom",
        "honor",
        "temporary_honor",
        "gifts",
        "rites_known",
        "fetishes_owned",
        "first_change",
        "battle_scars",
        "age_of_first_change",
    ]
    template_name = "characters/werewolf/garou/form.html"
    success_message = "Werewolf '{name}' created successfully!"
    error_message = "Failed to create werewolf. Please correct the errors below."


class WerewolfBasicsView(LoginRequiredMixin, FormView):
    form_class = WerewolfCreationForm
    template_name = "characters/werewolf/garou/basics.html"

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
            f"Werewolf '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class WerewolfAttributeView(HumanAttributeView):
    model = Werewolf
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfAbilityView(WtAHumanAbilityView):
    model = Werewolf
    template_name = "characters/werewolf/garou/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class WerewolfBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfGiftsView(SpecialUserMixin, UpdateView):
    model = Werewolf
    form_class = WerewolfGiftsForm
    template_name = "characters/werewolf/garou/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter gifts to only show rank 1 gifts with appropriate permissions
        form.fields["gifts"].queryset = Gift.objects.filter(
            rank=1, allowed__in=self.object.gift_permissions.all()
        ).order_by("name")
        form.fields["gifts"].help_text = (
            "Choose 3 starting Gifts: one from your Breed, one from your Auspice, "
            "and one from your Tribe."
        )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get gift permission objects for filtering
        breed_perm = GiftPermission.objects.get_or_create(
            shifter="werewolf", condition=self.object.breed
        )[0]
        auspice_perm = GiftPermission.objects.get_or_create(
            shifter="werewolf", condition=self.object.auspice
        )[0]
        if self.object.tribe:
            tribe_perm = GiftPermission.objects.get_or_create(
                shifter="werewolf", condition=self.object.tribe.name
            )[0]
        else:
            tribe_perm = None

        context["breed_gifts"] = Gift.objects.filter(rank=1, allowed=breed_perm).order_by("name")
        context["auspice_gifts"] = Gift.objects.filter(rank=1, allowed=auspice_perm).order_by(
            "name"
        )
        if tribe_perm:
            context["tribe_gifts"] = Gift.objects.filter(rank=1, allowed=tribe_perm).order_by(
                "name"
            )
        else:
            context["tribe_gifts"] = []
        return context

    def form_valid(self, form):
        """Handle successful form validation. Validation logic is in the form."""
        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Gifts selected successfully!")
        return super().form_valid(form)


class WerewolfHistoryView(SpecialUserMixin, UpdateView):
    model = Werewolf
    form_class = WerewolfHistoryForm
    template_name = "characters/werewolf/garou/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["first_change"].widget.attrs.update(
            {
                "placeholder": "Describe your character's First Change. Include where they were, what triggered it, and how they dealt with the immediate aftermath."
            }
        )
        form.fields["first_change"].help_text = "This is a pivotal moment in every Garou's life."
        form.fields["age_of_first_change"].help_text = (
            "The age at which the character first changed into Crinos form."
        )
        return form

    def form_valid(self, form):
        """Handle successful form validation. Validation logic is in the form."""
        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "First Change details saved successfully!")
        return super().form_valid(form)


class WerewolfExtrasView(SpecialUserMixin, UpdateView):
    model = Werewolf
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
    template_name = "characters/werewolf/garou/chargen.html"

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Character details saved successfully!")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's physical appearance in all forms (Homid, Glabro, Crinos, Hispo, Lupus). Be detailed, this will be visible to other players."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory. Include information about their upbringing, their First Change (already detailed above), and how they've integrated into Garou society. Mention important backgrounds and pack relationships."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {
                "placeholder": "Describe your character's long and short term goals, whether personal, pack-related, or related to Gaia's war."
            }
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "This will be displayed to all players who look at your character. Include Renown, Deeds, and anything else that would be publicly known in Garou society."
            }
        )
        return form


class WerewolfFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Werewolf


class WerewolfFreebiesView(HumanFreebiesView):
    model = Werewolf
    form_class = HumanFreebiesForm
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfLanguagesView(HumanLanguagesView):
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfAlliesView(GenericBackgroundView):
    primary_object_class = Werewolf
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfMentorView(GenericBackgroundView):
    primary_object_class = Werewolf
    background_name = "mentor"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfContactsView(GenericBackgroundView):
    primary_object_class = Werewolf
    background_name = "contacts"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfFetishView(GenericBackgroundView):
    primary_object_class = Werewolf
    background_name = "fetish"
    form_class = None  # We'll handle this specially
    template_name = "characters/werewolf/garou/chargen.html"
    multiple_ownership = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current background rating for fetish
        fetish_bg, _ = Background.objects.get_or_create(
            property_name="fetish", defaults={"name": "Fetish"}
        )
        fetish_rating = BackgroundRating.objects.filter(char=self.object, bg=fetish_bg).first()
        if fetish_rating:
            context["max_fetish_rating"] = fetish_rating.rating
            context["current_fetish_total"] = self.object.total_fetish_rating()
        else:
            context["max_fetish_rating"] = 0
            context["current_fetish_total"] = 0
        context["available_fetishes"] = self.object.filter_fetishes(
            min_rating=0,
            max_rating=(fetish_rating.rating if fetish_rating else 0),
        )
        return context


class WerewolfSpecialtiesView(HumanSpecialtiesView):
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: WerewolfAttributeView,
        2: WerewolfAbilityView,
        3: WerewolfBackgroundsView,
        4: WerewolfGiftsView,
        5: WerewolfHistoryView,
        6: WerewolfExtrasView,
        7: WerewolfFreebiesView,
        8: WerewolfLanguagesView,
        9: WerewolfAlliesView,
        10: WerewolfMentorView,
        11: WerewolfContactsView,
        12: WerewolfSpecialtiesView,
    }
    model_class = Werewolf
    key_property = "creation_status"
    default_redirect = WerewolfDetailView
