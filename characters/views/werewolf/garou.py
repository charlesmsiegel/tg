from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.crud_fields import WEREWOLF_UPDATE_FIELDS
from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.werewolf.garou import (
    WerewolfCreationForm,
    WerewolfGiftsForm,
    WerewolfHistoryForm,
)
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift
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
from characters.views.werewolf.wtahuman import WtAHumanAbilityView
from core.mixins import (
    EditPermissionMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
    SpecialUserMixin,
    XPApprovalMixin,
)
from core.permissions import PermissionManager


class WerewolfDetailView(XPApprovalMixin, HumanDetailView):
    model = Werewolf
    template_name = "characters/werewolf/garou/detail.html"


class WerewolfUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Werewolf
    fields = WEREWOLF_UPDATE_FIELDS
    template_name = "characters/werewolf/garou/form.html"
    success_message = "Werewolf '{name}' updated successfully!"
    error_message = "Failed to update werewolf. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm


class WerewolfBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = WerewolfCreationForm
    template_name = "characters/werewolf/garou/basics.html"

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


class WerewolfGiftsView(ChargenStepMixin, SpecialUserMixin, UpdateView):
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
        context["breed_gifts"] = (
            Gift.objects.filter(
                rank=1, allowed__shifter="werewolf", allowed__condition=self.object.breed
            )
            .distinct()
            .order_by("name")
        )
        context["auspice_gifts"] = (
            Gift.objects.filter(
                rank=1, allowed__shifter="werewolf", allowed__condition=self.object.auspice
            )
            .distinct()
            .order_by("name")
        )
        if self.object.tribe:
            context["tribe_gifts"] = (
                Gift.objects.filter(
                    rank=1, allowed__shifter="werewolf", allowed__condition=self.object.tribe.name
                )
                .distinct()
                .order_by("name")
            )
        else:
            context["tribe_gifts"] = []
        return context

    def form_valid(self, form):
        """Handle successful form validation. Validation logic is in the form."""
        advance(self.object, user=self.request.user)
        self.object.save()
        messages.success(self.request, "Gifts selected successfully!")
        return super().form_valid(form)


class WerewolfHistoryView(ChargenStepMixin, SpecialUserMixin, UpdateView):
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
        advance(self.object, user=self.request.user)
        self.object.save()
        messages.success(self.request, "First Change details saved successfully!")
        return super().form_valid(form)


class WerewolfExtrasView(CharacterExtrasView):
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
    success_message = "Character details saved successfully!"
    field_widget_attrs = {
        "description": {
            "placeholder": "Describe your character's physical appearance in all forms (Homid, Glabro, Crinos, Hispo, Lupus). Be detailed, this will be visible to other players."
        },
        "history": {
            "placeholder": "Describe character history/backstory. Include information about their upbringing, their First Change (already detailed above), and how they've integrated into Garou society. Mention important backgrounds and pack relationships."
        },
        "goals": {
            "placeholder": "Describe your character's long and short term goals, whether personal, pack-related, or related to Gaia's war."
        },
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character. Include Renown, Deeds, and anything else that would be publicly known in Garou society."
        },
    }


class WerewolfFreebiesView(HumanFreebiesView):
    """Freebie spending view for Werewolf characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    GarouFreebieSpendingService with Werewolf-specific handlers.
    """

    model = Werewolf
    form_class = HumanFreebiesForm
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfLanguagesView(HumanLanguagesView):
    model = Werewolf
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


class WerewolfSpecialtiesView(HumanSpecialtiesView):
    model = Werewolf
    template_name = "characters/werewolf/garou/chargen.html"


class WerewolfCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Werewolf
    key_property = "creation_status"
    default_redirect = WerewolfDetailView
