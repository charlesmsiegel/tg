import logging
from typing import Any

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.crud_fields import MAGE_CREATE_FIELDS
from characters.views.core.chargen_mixins import ChargenStepMixin
from characters.views.core.human import HumanLanguagesView, HumanSpecialtiesView
from core.mixins import ScopedCreationFormMixin, ScopedEditFormMixin

logger = logging.getLogger(__name__)

import re
from itertools import zip_longest

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, FormView, UpdateView

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.mage.chained_freebies import ChainedMageFreebiesForm
from characters.forms.mage.familiar import FamiliarForm
from characters.forms.mage.mage import MageCreationForm, MageFocusForm, MageSpheresForm
from characters.forms.mage.practiceform import PracticeRatingFormSet
from characters.forms.mage.rote import RoteCreationForm
from characters.forms.mage.xp import MageXPForm
from characters.models.core.specialty import Specialty
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Tenet
from characters.models.mage.mage import Mage, ResRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.services.mage_chargen import set_starting_practices
from characters.services.rotes import learn_rote
from characters.services.xp_spending import XPSpendingServiceFactory
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebiesView,
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
        if "retire" in request.POST or "decease" in request.POST:
            return super().post(request, *args, **kwargs)
        context = self.get_context_data()
        form = MageXPForm(request.POST, request.FILES, character=self.object)
        if "spend_xp" in form.data and form.is_valid():
            category = form.cleaned_data["category"]
            if category == "Image":
                self.object.image = form.cleaned_data["image_field"]
                self.object.save()
            elif category == "Rote":
                rote_form = RoteCreationForm(request.POST, instance=self.object)
                if not self.learn_rote(rote_form):
                    context["rote_form"] = rote_form
                    return render(request, self.template_name, context)
            else:
                with XPSpendingServiceFactory.locked(self.object) as service:
                    result = service.spend(
                        category=category,
                        example=form.cleaned_data["example"],
                        value=form.cleaned_data["value"],
                        note=form.cleaned_data["note"],
                        pooled=form.cleaned_data["pooled"],
                        resonance=form.cleaned_data["resonance"],
                    )
                if not result.success:
                    messages.error(request, result.error)
                    context["form"] = form
                    return self.render_to_response(context)
                messages.success(request, result.message)
        if "specialties" in request.POST:
            self.add_specialties(request.POST)
        return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

    @staticmethod
    def learn_rote(rote_form):
        if not rote_form.is_valid():
            return False
        try:
            rote_form.save(rote_form.instance)
        except forms.ValidationError as error:
            rote_form.add_error(None, error)
            return False
        return True

    def add_specialties(self, data):
        """Record the submitted specialties the character actually needs."""
        spec_form = SpecialtiesForm(
            data, object=self.object, specialties_needed=self.object.needed_specialties()
        )
        for field in spec_form.fields.values():
            field.required = False
        if not spec_form.is_valid():
            return
        for stat, name in spec_form.cleaned_data.items():
            if name:
                specialty, _ = Specialty.objects.get_or_create(name=name, stat=stat)
                self.object.specialties.add(specialty)
        self.object.save()


class MageFormContextMixin:
    """Model data the Mage create/edit template shows next to the form.

    The template used to read these off ``form`` (``form.affiliation.name``,
    ``form.paradigms.all``, ``<stat>_spec``, ...), where they never exist, so the
    Technocracy labels, specialties, rotes and resonance never rendered.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mage = self.object  # None while creating
        form = context["form"]
        affiliation = getattr(mage, "affiliation", None)
        context["technocratic"] = bool(affiliation and affiliation.name == "Technocratic Union")
        groups = []
        for _heading, group in Mage.ABILITY_GROUPS:
            stats = sorted(
                (stat for stat in getattr(Mage, group) if stat in Mage.primary_abilities),
                key=Mage.ability_label,
            )
            groups.append(
                [
                    (
                        Mage.ability_label(stat),
                        form[stat] if stat in form.fields else "",
                        mage.get_specialty(stat) if mage else None,
                    )
                    for stat in stats
                ]
            )
        context["ability_rows"] = list(zip_longest(*groups, fillvalue=("", "", None)))
        if mage is not None:
            context["rotes"] = mage.rotes.select_related("effect")
            context["resonance"] = (
                ResRating.objects.filter(mage=mage)
                .select_related("resonance")
                .order_by("resonance__name")
            )
        return context


class MageCreateView(MageFormContextMixin, MessageMixin, CreateView):
    model = Mage
    FORM_FIELDS = MAGE_CREATE_FIELDS
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


class MageUpdateView(MageFormContextMixin, ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Mage
    fields = MageCreateView.FORM_FIELDS
    template_name = "characters/mage/mage/form.html"
    success_message = "Mage '{name}' updated successfully!"
    error_message = "Failed to update mage. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm


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
    form_class = MageFocusForm
    template_name = "characters/mage/mage/chargen.html"

    def get_practice_formset(self):
        if not hasattr(self, "_practice_formset"):
            data = self.request.POST if self.request.method == "POST" else None
            self._practice_formset = PracticeRatingFormSet(
                data, instance=self.object, mage=self.object
            )
        return self._practice_formset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["practice_formset"] = self.get_practice_formset()
        return kwargs

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
        context["practice_formset"] = self.get_practice_formset()
        return context

    def form_valid(self, form):
        if not self.get_practice_formset().is_valid():
            return self.form_invalid(form)
        self.object = set_starting_practices(form).object
        advance(self.object, user=self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


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
        """Record Resonance, buy starting Arete with freebies, and advance."""
        with transaction.atomic():
            self.object.add_resonance(form.cleaned_data["resonance"])
            advance(self.object, user=self.request.user)
            self.object.purchase_starting_arete(form.cleaned_data["arete"])
            self.object.save()
            return super().form_valid(form)


class MageExtrasView(CharacterExtrasView):
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
    field_widget_attrs = {
        "history": {
            "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with mage society since, particularly mentioning important backgrounds."
        },
        "avatar_description": {
            "placeholder": "Describe your Avatar. Both how it appears to you, how you relate to it, and anything it is, in particular, pushing you towards."
        },
        "goals": {
            "placeholder": "Describe your character's long and short term goals, whether personal, professional, or magical."
        },
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        },
    }


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
    model = Mage
    template_name = "characters/mage/mage/chargen.html"


class MageRoteView(ChargenStepMixin, SpecialUserMixin, CreateView):
    model = Rote
    form_class = RoteCreationForm
    template_name = "characters/mage/mage/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        mage_id = self.kwargs.get("pk")
        context["object"] = get_object_or_404(Mage, id=mage_id)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        mage_id = self.kwargs.get("pk")
        mage = get_object_or_404(Mage, pk=mage_id)
        kwargs["instance"] = mage
        return kwargs

    def form_valid(self, form):
        mage = form.instance
        result = learn_rote(mage, form.cleaned_data)
        if not result.success:
            form.add_error(None, result.error)
            return self.form_invalid(form)
        if mage.rote_points == 0:
            advance(mage, user=self.request.user)
        return HttpResponseRedirect(mage.get_absolute_url())


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
    model = Mage
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
