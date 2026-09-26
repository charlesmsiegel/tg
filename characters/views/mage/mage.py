import logging
from typing import Any

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.views.core.chargen_mixins import ChargenStepMixin
from core.mixins import ScopedCreationFormMixin

logger = logging.getLogger(__name__)

import re

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, FormView, UpdateView

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.mage.chained_freebies import ChainedMageFreebiesForm
from characters.forms.mage.familiar import FamiliarForm
from characters.forms.mage.mage import MageCreationForm, MageSpheresForm
from characters.forms.mage.practiceform import PracticeRatingFormSet
from characters.forms.mage.rote import RoteCreationForm
from characters.forms.mage.xp import MageXPForm
from characters.models.core.specialty import Specialty
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Tenet
from characters.models.mage.mage import Mage, PracticeRating, ResRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.services.xp_spending import XPSpendingServiceFactory
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.mage.background_views import (
    CharacterChantryBackgroundView,
    MtAEnhancementView,
)
from characters.views.mage.mtahuman import MtAHumanAbilityView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    SpecialUserMixin,
)
from core.permissions import Permission, PermissionManager
from core.widgets import AutocompleteTextInput
from game.models import XPSpendingRequest
from game.spending_approval import SpendingDecisionError, decide_spending_request
from items.forms.mage.wonder import WonderForm
from items.models.core.item import ItemModel
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


class MageDetailView(HumanDetailView):
    model = Mage
    template_name = "characters/mage/mage/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["items_owned"] = ItemModel.objects.filter(owned_by=self.object)
        if "form" not in context:
            context["form"] = MageXPForm(character=self.object)
        context["rote_form"] = RoteCreationForm(instance=self.object)
        context["spec_form"] = SpecialtiesForm(
            object=self.object, specialties_needed=self.object.needed_specialties()
        )
        context["resonance"] = (
            ResRating.objects.filter(mage=self.object)
            .select_related("resonance")
            .order_by("resonance__name")
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "Approve" in request.POST.values() or "Reject" in request.POST.values():
            buttons = [
                (key, value)
                for key, value in request.POST.items()
                if value in {"Approve", "Reject"}
            ]
            if len(buttons) != 1:
                return HttpResponseBadRequest("Invalid approval action")
            key, value = buttons[0]
            match = re.fullmatch(r"xp_request_([1-9][0-9]*)_(approve|reject)", key)
            if match is None or (value == "Approve") != (match.group(2) == "approve"):
                return HttpResponseBadRequest("Invalid approval action")
            try:
                result = decide_spending_request(
                    XPSpendingRequest,
                    self.object,
                    int(match.group(1)),
                    request.user,
                    "approve" if value == "Approve" else "deny",
                )
            except SpendingDecisionError as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, result.message)
            return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

        if "spend_xp" in request.POST and not PermissionManager.user_has_permission(
            request.user, self.object, Permission.SPEND_XP
        ):
            raise PermissionDenied("Cannot spend XP for this character")
        if "specialties" in request.POST and not PermissionManager.user_has_permission(
            request.user, self.object, Permission.EDIT_FULL
        ):
            raise PermissionDenied("Cannot edit this character")
        can_edit = PermissionManager.user_has_scoped_editor_role(
            request.user, self.object, request=request
        )
        if "retire" in request.POST and not (can_edit or self.object.owner_id == request.user.pk):
            raise PermissionDenied("Cannot retire this character")
        if "decease" in request.POST and not can_edit:
            raise PermissionDenied("Cannot mark this character deceased")
        context = self.get_context_data()
        form = MageXPForm(request.POST, request.FILES, character=self.object)
        rote_form = RoteCreationForm(request.POST, instance=self.object)
        form_errors = False
        if "spend_xp" in form.data.keys():
            if form.is_valid():
                category = form.cleaned_data["category"]
                example = form.cleaned_data["example"]
                value = form.cleaned_data["value"]
                note = form.cleaned_data["note"]
                pooled = form.cleaned_data["pooled"]
                image_field = form.cleaned_data["image_field"]
                resonance = form.cleaned_data["resonance"]
                if category == "Image":
                    self.object.image = image_field
                    self.object.save()
                if category not in ["Image", "Rote"]:
                    # Use XP spending service for cleaner handling
                    service = XPSpendingServiceFactory.get_service(self.object)
                    result = service.spend(
                        category=category,
                        example=example,
                        value=value,
                        note=note,
                        pooled=pooled,
                        resonance=resonance,
                    )
                    if result.success:
                        messages.success(request, result.message)
                    else:
                        messages.error(request, result.error)
                        context["form"] = form
                        form_errors = True
                elif category == "Rote":
                    if rote_form.is_valid():
                        if (
                            not rote_form.cleaned_data["select_or_create_rote"]
                            and not rote_form.cleaned_data["rote_options"]
                        ):
                            rote_form.add_error(None, "Must create or select a rote")
                            context["rote_form"] = rote_form
                            return render(request, self.template_name, context)
                        if rote_form.cleaned_data["select_or_create_rote"]:
                            if (
                                not rote_form.cleaned_data["select_or_create_effect"]
                                and not rote_form.cleaned_data["effect_options"]
                            ):
                                rote_form.add_error(None, "Must create or select an effect")
                                context["rote_form"] = rote_form
                                return render(request, self.template_name, context)
                            if not rote_form.cleaned_data["name"]:
                                rote_form.add_error(None, "Must choose rote name")
                                context["rote_form"] = rote_form
                                return render(request, self.template_name, context)
                            if not rote_form.cleaned_data["practice"]:
                                rote_form.add_error(None, "Must choose rote Practice")
                                context["rote_form"] = rote_form
                                return render(request, self.template_name, context)
                            if not rote_form.cleaned_data["attribute"]:
                                rote_form.add_error(None, "Must choose rote Attribute")
                                context["rote_form"] = rote_form
                                return render(request, self.template_name, context)
                            if not rote_form.cleaned_data["ability"]:
                                rote_form.add_error(None, "Must choose rote Ability")
                                context["rote_form"] = rote_form
                                return render(request, self.template_name, context)
                            if not rote_form.cleaned_data["description"]:
                                rote_form.add_error(None, "Must choose rote description")
                                context["rote_form"] = rote_form
                                return render(request, self.template_name, context)
                            if rote_form.cleaned_data["select_or_create_effect"]:
                                if not rote_form.cleaned_data["systems"]:
                                    rote_form.add_error(None, "Must choose rote systems")
                                    context["rote_form"] = rote_form
                                    return render(request, self.template_name, context)
                                if (
                                    rote_form.cleaned_data["correspondence"]
                                    + rote_form.cleaned_data["entropy"]
                                    + rote_form.cleaned_data["forces"]
                                    + rote_form.cleaned_data["life"]
                                    + rote_form.cleaned_data["matter"]
                                    + rote_form.cleaned_data["mind"]
                                    + rote_form.cleaned_data["prime"]
                                    + rote_form.cleaned_data["spirit"]
                                    + rote_form.cleaned_data["time"]
                                    == 0
                                ):
                                    rote_form.add_error(None, "Effects must have sphere ratings")
                                    context["rote_form"] = rote_form
                                    return render(request, self.template_name, context)
                        try:
                            rote_form.save(self.object)
                        except forms.ValidationError:
                            context["rote_form"] = rote_form
                            return render(request, self.template_name, context)
            else:
                pass
        if "specialties" in form.data.keys():
            specs = {
                k: v
                for k, v in form.data.items()
                if k not in ["csrfmiddlewaretoken", "specialties"]
            }
            for stat, spec in specs.items():
                spec = Specialty.objects.get_or_create(name=spec, stat=stat)[0]
                self.object.specialties.add(spec)
            self.object.save()
        if "retire" in form.data.keys():
            self.object.status = "Ret"
            self.object.save()
        if "decease" in form.data.keys():
            self.object.status = "Dec"
            self.object.save()
        if form_errors:
            return self.render_to_response(context)
        return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))


class MageCreateView(MessageMixin, CreateView):
    model = Mage
    FORM_FIELDS = [
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
        "essence",
        "correspondence",
        "time",
        "spirit",
        "mind",
        "entropy",
        "time",
        "forces",
        "matter",
        "life",
        "arete",
        "affinity_sphere",
        "corr_name",
        "prime_name",
        "spirit_name",
        "age_of_awakening",
        "avatar_description",
        "rote_points",
        "quintessence",
        "paradox",
        "quiet",
        "quiet_type",
        "affiliation",
        "faction",
        "subfaction",
        "public_info",
    ]
    fields = FORM_FIELDS
    template_name = "characters/mage/mage/form.html"
    success_message = "Mage '{name}' created successfully!"
    error_message = "Failed to create mage. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["affiliation"].queryset = MageFaction.objects.top_level()
        form.fields["faction"].queryset = MageFaction.objects.none()
        form.fields["subfaction"].queryset = MageFaction.objects.none()
        return form


class MageUpdateView(EditPermissionMixin, UpdateView):
    model = Mage
    fields = MageCreateView.FORM_FIELDS
    template_name = "characters/mage/mage/form.html"
    success_message = "Mage '{name}' updated successfully!"
    error_message = "Failed to update mage. Please correct the errors below."

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedHumanEditForm.
        STs and admins get full access via the default form.
        """
        has_full_edit = PermissionManager.user_has_scoped_editor_role(
            self.request.user, self.get_object(), request=self.request
        )
        if has_full_edit:
            return super().get_form_class()
        else:
            return LimitedHumanEditForm


class MageBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = MageCreationForm
    template_name = "characters/mage/mage/magebasics.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["storyteller"] = PermissionManager.user_can_manage_creation(
            self.request.user, context["form"], request=self.request
        )
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.willpower = 5
        self.object.save()
        messages.success(
            self.request,
            f"Mage '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class MageAttributeView(HumanAttributeView):
    model = Mage
    template_name = "characters/mage/mage/chargen.html"


class MageAbilityView(MtAHumanAbilityView):
    model = Mage
    template_name = "characters/mage/mage/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class MageBackgroundsView(HumanBackgroundsView):
    template_name = "characters/mage/mage/chargen.html"


class MageFocusView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Mage
    fields = [
        "metaphysical_tenet",
        "personal_tenet",
        "ascension_tenet",
        "other_tenets",
    ]
    template_name = "characters/mage/mage/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["metaphysical_tenet"].queryset = Tenet.objects.filter(tenet_type="met")
        form.fields["personal_tenet"].queryset = Tenet.objects.filter(tenet_type="per")
        form.fields["ascension_tenet"].queryset = Tenet.objects.filter(tenet_type="asc")
        form.fields["other_tenets"].queryset = Tenet.objects.filter(tenet_type="oth")
        form.fields["personal_tenet"].empty_label = "Choose Personal Tenet"
        form.fields["ascension_tenet"].empty_label = "Choose Ascension Tenet"
        form.fields["metaphysical_tenet"].empty_label = "Choose Metaphysical Tenet"
        return form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["practice_formset"] = PracticeRatingFormSet(
                self.request.POST, instance=self.object, mage=self.object
            )
        else:
            context["practice_formset"] = PracticeRatingFormSet(
                instance=self.object, mage=self.object
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context["form"].full_clean()
        if context["form"].cleaned_data["metaphysical_tenet"] is None:
            context["form"].add_error(None, "Must include Metaphysical Tenet")
            return self.form_invalid(context["form"])
        if context["form"].cleaned_data["personal_tenet"] is None:
            context["form"].add_error(None, "Must include Personal Tenet")
            return self.form_invalid(context["form"])
        if context["form"].cleaned_data["ascension_tenet"] is None:
            context["form"].add_error(None, "Must include Ascension Tenet")
            return self.form_invalid(context["form"])
        practice_formset = context["practice_formset"]

        if practice_formset.is_valid():
            self.object = form.save()
            ratings = [x.cleaned_data.get("rating") for x in practice_formset]
            ratings = [x for x in ratings if x is not None]
            practice_total = sum(ratings)
            if practice_total != self.object.arete:
                form.add_error(None, "Starting Practices must add up to Arete rating")
                return self.form_invalid(form)
            for practice_form in practice_formset:
                practice = practice_form.cleaned_data.get("practice")
                rating = practice_form.cleaned_data.get("rating")
                if practice is not None:
                    ability_total = 0
                    for ability in practice.abilities.all():
                        ability_total += getattr(self.object, ability.property_name, 0)
                    if practice is not None and rating is not None and rating <= ability_total / 2:
                        pr = PracticeRating.objects.create(
                            mage=self.object, practice=practice, rating=rating
                        )
                    else:
                        form.add_error(
                            None,
                            "You must have at least 2 dots in associated abilities for each dot of a Practice",
                        )
                        return self.form_invalid(form)
            advance(self.object, user=self.request.user)
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response


class MageSpheresView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Mage
    form_class = MageSpheresForm
    template_name = "characters/mage/mage/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["affinity_sphere"].queryset = (
            self.object.get_affinity_sphere_options().order_by("name")
        )
        form.fields["affinity_sphere"].empty_label = "Choose an Affinity"
        form.fields["resonance"].widget = AutocompleteTextInput(
            suggestions=[x.name.title() for x in Resonance.objects.order_by("name")]
        )
        form.fields["affinity_sphere"].required = True
        return form

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["arete"] = 1
        initial["resonance"] = ""
        return initial

    def form_valid(self, form):
        """Handle successful form validation. Validation logic is in the form."""
        arete = form.cleaned_data.get("arete", 1)
        resonance = form.data.get("resonance")

        # Add resonance to character
        self.object.add_resonance(resonance)

        # Update creation status
        advance(self.object, user=self.request.user)

        # Handle freebie spending for Arete above 1
        for i in range(arete - 1):
            self.object.freebies -= 4
            self.object.spent_freebies.append(
                self.object.freebie_spend_record("Arete", "arete", i + 2)
            )

        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors. Remove resonance errors if data was provided."""
        errors = form.errors
        if "resonance" in errors and "resonance" in form.data:
            del errors["resonance"]
        if not errors:
            return self.form_valid(form)
        return super().form_invalid(form)


class MageExtrasView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Mage
    fields = [
        "date_of_birth",
        "apparent_age",
        "age_of_awakening",
        "age",
        "description",
        "history",
        "avatar_description",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/mage/mage/chargen.html"

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
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
        form.fields["avatar_description"].widget.attrs.update(
            {
                "placeholder": "Describe your Avatar. Both how it appears to you, how you relate to it, and anything it is, in particular, pushing you towards."
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


class MageFreebiesView(HumanFreebiesView):
    """Freebie spending view for Mage characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    MageFreebieSpendingService with Mage-specific handlers.
    """

    model = Mage
    form_class = ChainedMageFreebiesForm
    template_name = "characters/mage/mage/chargen.html"


class MageLanguagesView(HumanLanguagesView):
    template_name = "characters/mage/mage/chargen.html"


class MageRoteView(ChargenStepMixin, SpecialUserMixin, CreateView):
    model = Rote
    form_class = RoteCreationForm
    template_name = "characters/mage/mage/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        mage_id = self.kwargs.get("pk")
        context["object"] = get_object_or_404(Mage, id=mage_id)
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        mage_id = self.kwargs.get("pk")
        mage = get_object_or_404(Mage, pk=mage_id)
        kwargs["instance"] = mage
        return kwargs

    def form_invalid(self, form):
        errors = form.errors
        if not errors:
            return self.form_valid(form)
        return super().form_invalid(form)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        mage = context["object"]
        if not form.cleaned_data["select_or_create_rote"] and not form.cleaned_data["rote_options"]:
            form.add_error(None, "Must create or select a rote")
            return super().form_invalid(form)
        if form.cleaned_data["select_or_create_rote"]:
            if (
                not form.cleaned_data["select_or_create_effect"]
                and not form.cleaned_data["effect_options"]
            ):
                form.add_error(None, "Must create or select an effect")
                return super().form_invalid(form)
            if not form.cleaned_data["name"]:
                form.add_error(None, "Must choose rote name")
                return super().form_invalid(form)
            if not form.cleaned_data["practice"]:
                form.add_error(None, "Must choose rote Practice")
                return super().form_invalid(form)
            if not form.cleaned_data["attribute"]:
                form.add_error(None, "Must choose rote Attribute")
                return super().form_invalid(form)
            if not form.cleaned_data["ability"]:
                form.add_error(None, "Must choose rote Ability")
                return super().form_invalid(form)
            if not form.cleaned_data["description"]:
                form.add_error(None, "Must choose rote description")
                return super().form_invalid(form)
            if form.cleaned_data["select_or_create_effect"]:
                if not form.cleaned_data["systems"]:
                    form.add_error(None, "Must choose rote systems")
                    return super().form_invalid(form)
                if (
                    form.cleaned_data["correspondence"]
                    + form.cleaned_data["entropy"]
                    + form.cleaned_data["forces"]
                    + form.cleaned_data["life"]
                    + form.cleaned_data["matter"]
                    + form.cleaned_data["mind"]
                    + form.cleaned_data["prime"]
                    + form.cleaned_data["spirit"]
                    + form.cleaned_data["time"]
                    == 0
                ):
                    form.add_error(None, "Effects must have sphere ratings")
                    return super().form_invalid(form)

        if form.save(mage):
            if mage.rote_points == 0:
                advance(mage, user=self.request.user)
            return HttpResponseRedirect(mage.get_absolute_url())
        return super().form_invalid(form)


class MageAlliesView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/mage/mage/chargen.html"


class MageMentorView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "mentor"
    form_class = LinkedNPCForm
    template_name = "characters/mage/mage/chargen.html"


class MageContactsView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "contacts"
    form_class = LinkedNPCForm
    template_name = "characters/mage/mage/chargen.html"


class MageRetainersView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "retainers"
    form_class = LinkedNPCForm
    template_name = "characters/mage/mage/chargen.html"


class MageEnhancementView(MtAEnhancementView):
    template_name = "characters/mage/mage/chargen.html"


class MageFamiliarView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "familiar"
    form_class = FamiliarForm
    template_name = "characters/mage/mage/chargen.html"

    def special_valid_action(self, background_object):
        background_object.freebies = 10 * self.current_background.rating
        background_object.status = "Un"
        background_object.save()
        return background_object


class MageLibraryView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "library"
    form_class = LibraryForm
    template_name = "characters/mage/mage/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        form.fields["name"].initial = self.current_background.note or f"{obj.name}'s Library"
        tmp = [obj.affiliation, obj.faction, obj.subfaction]
        tmp = [x.pk for x in tmp if hasattr(x, "pk")]
        form.fields["faction"].queryset = MageFaction.objects.filter(pk__in=tmp)
        return form


class MageNodeView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "node"
    form_class = NodeForm
    template_name = "characters/mage/mage/chargen.html"


class MageSpecialtiesView(HumanSpecialtiesView):
    template_name = "characters/mage/mage/chargen.html"


class MageWonderView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "wonder"
    form_class = WonderForm
    template_name = "characters/mage/mage/chargen.html"
    multiple_ownership = True


class MageSanctumView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "sanctum"
    form_class = SanctumForm
    template_name = "characters/mage/mage/chargen.html"


class MageChantryView(CharacterChantryBackgroundView):
    primary_object_class = Mage
    template_name = "characters/mage/mage/chargen.html"


class MageCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Mage
    key_property = "creation_status"
    default_redirect = MageDetailView
