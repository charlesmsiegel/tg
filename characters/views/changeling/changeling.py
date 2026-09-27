from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.changeling.chained_freebies import ChainedChangelingFreebiesForm
from characters.forms.changeling.changeling import ChangelingCreationForm
from characters.forms.core.crud_fields import CHANGELING_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.models.changeling.changeling import Changeling
from characters.models.core.merit_flaw_block import MeritFlawRating
from characters.views.changeling.ctdhuman import CtDHumanAbilityView
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.chargen_mixins import ChargenStepMixin
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from core.mixins import (
    EditPermissionMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
    SpecialUserMixin,
    XPApprovalMixin,
)
from core.permissions import PermissionManager


class ChangelingDetailView(XPApprovalMixin, HumanDetailView):
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

        context["merits_and_flaws"] = MeritFlawRating.objects.order_by("mf__name").filter(
            character=self.object
        )
        return context


class ChangelingUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Changeling
    fields = CHANGELING_UPDATE_FIELDS
    template_name = "characters/changeling/changeling/form.html"
    success_message = "Changeling '{name}' updated successfully!"
    error_message = "Failed to update changeling. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChangelingBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = ChangelingCreationForm
    template_name = "characters/changeling/changeling/basics.html"

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
        messages.success(
            self.request,
            f"Changeling '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ChangelingAttributeView(HumanAttributeView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChangelingAbilityView(CtDHumanAbilityView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class ChangelingBackgroundsView(HumanBackgroundsView):
    template_name = "characters/changeling/changeling/chargen.html"


class ChangelingArtsRealmsView(ChargenStepMixin, SpecialUserMixin, UpdateView):
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
            messages.error(
                self.request,
                f"Arts allocation error: You must spend exactly 3 dots. You have {total_arts}.",
            )
            return self.form_invalid(form)

        # Validate realms total is 5
        total_realms = sum(realms.values())
        if total_realms != 5:
            form.add_error(None, f"Realms must total 5 dots (currently {total_realms})")
            messages.error(
                self.request,
                f"Realms allocation error: You must spend exactly 5 dots. You have {total_realms}.",
            )
            return self.form_invalid(form)

        # Validate individual values don't exceed 5
        for art_name, value in arts.items():
            if value > 5:
                form.add_error(art_name, "Cannot exceed 5 dots")
                messages.error(
                    self.request,
                    f"{art_name.replace('_', ' ').title()} cannot exceed 5 dots.",
                )
                return self.form_invalid(form)

        for realm_name, value in realms.items():
            if value > 5:
                form.add_error(realm_name, "Cannot exceed 5 dots")
                messages.error(
                    self.request,
                    f"{realm_name.replace('_', ' ').title()} cannot exceed 5 dots.",
                )
                return self.form_invalid(form)

        # All validations passed, increment creation_status and save
        advance(self.object, user=self.request.user)
        self.object.save()
        messages.success(self.request, "Arts and Realms allocated successfully!")
        return super().form_valid(form)


class ChangelingExtrasView(CharacterExtrasView):
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
    success_message = "Character details saved successfully!"
    date_fields = ("date_of_birth", "date_of_crysalis")
    optional_fields = ("date_of_birth", "date_of_crysalis")
    field_widget_attrs = {
        "history": {
            "placeholder": "Describe character history/backstory. Include information about their mortal life and their Chrysalis."
        },
        "true_name": {"placeholder": "Your character's fae true name"},
        "crysalis": {
            "placeholder": "Describe your character's Chrysalis - how they awakened to their fae nature."
        },
        "fae_mien": {"placeholder": "Describe your character's fae appearance."},
        "antithesis": {
            "placeholder": "What is your character's Antithesis? What causes them to gain Banality?"
        },
    }


class ChangelingFreebiesView(HumanFreebiesView):
    """Freebie spending view for Changeling characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    ChangelingFreebieSpendingService with Changeling-specific handlers.
    """

    model = Changeling
    form_class = ChainedChangelingFreebiesForm
    template_name = "characters/changeling/changeling/chargen.html"


class ChangelingLanguagesView(HumanLanguagesView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"
    success_message = "Languages added successfully!"


class ChangelingAlliesView(GenericBackgroundView):
    primary_object_class = Changeling
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/changeling/changeling/chargen.html"


class ChangelingSpecialtiesView(HumanSpecialtiesView):
    model = Changeling
    template_name = "characters/changeling/changeling/chargen.html"
    success_message = "Changeling '{name}' submitted for approval!"


class ChangelingCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Changeling
    key_property = "creation_status"
    default_redirect = ChangelingDetailView
