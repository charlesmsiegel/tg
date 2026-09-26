from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.wraith.fetter import FetterForm
from characters.forms.wraith.freebies import WraithFreebiesForm
from characters.forms.wraith.passion import PassionForm
from characters.forms.wraith.wraith import WraithCreationForm
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import Wraith
from characters.views.core.allocations import PointAllocationView
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.chargen_mixins import ChargenStepMixin
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.wraith.wraith import WraithDetailView
from characters.views.wraith.wtohuman import WtOHumanAbilityView
from core.mixins import (
    ScopedCreationFormMixin,
    SpecialUserMixin,
)
from core.permissions import PermissionManager


class WraithBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = WraithCreationForm
    template_name = "characters/wraith/wraith/basics.html"

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
        # Set initial values based on guild
        if self.object.guild:
            self.object.willpower = self.object.guild.willpower
        self.object.save()
        messages.success(
            self.request,
            f"Wraith '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class WraithAttributeView(HumanAttributeView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"

    primary = 7
    secondary = 5
    tertiary = 3


class WraithAbilityView(WtOHumanAbilityView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class WraithBackgroundsView(HumanBackgroundsView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"


class WraithArcanosView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Wraith
    fields = [
        "argos",
        "castigate",
        "embody",
        "fatalism",
        "flux",
        "inhabit",
        "keening",
        "lifeweb",
        "moliate",
        "mnemosynis",
        "outrage",
        "pandemonium",
        "phantasm",
        "usury",
        "intimation",
    ]
    template_name = "characters/wraith/wraith/chargen.html"

    def form_valid(self, form):
        # Validate that total arcanoi is exactly 5
        arcanoi_total = sum(form.cleaned_data.get(field, 0) for field in self.fields)

        if arcanoi_total != 5:
            form.add_error(
                None,
                f"Arcanoi must total exactly 5 dots (currently {arcanoi_total})",
            )
            messages.error(
                self.request,
                f"Arcanoi allocation error: You must spend exactly 5 dots. You have {arcanoi_total}.",
            )
            return self.form_invalid(form)

        # Validate that no arcanos exceeds 5
        for field in self.fields:
            if form.cleaned_data.get(field, 0) > 5:
                form.add_error(field, "Arcanoi cannot exceed 5 dots")
                messages.error(self.request, "Each Arcanos cannot exceed 5 dots.")
                return self.form_invalid(form)

        advance(self.object, user=self.request.user)
        self.object.save()
        messages.success(self.request, "Arcanoi allocated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WraithShadowView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Wraith
    fields = ["shadow_archetype"]
    template_name = "characters/wraith/wraith/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shadow_archetypes"] = ShadowArchetype.objects.all()
        context["thorns"] = Thorn.objects.all()
        return context

    def form_valid(self, form):
        # Shadow archetype is required
        if not form.cleaned_data.get("shadow_archetype"):
            form.add_error("shadow_archetype", "Shadow Archetype is required")
            messages.error(self.request, "You must select a Shadow Archetype to continue.")
            return self.form_invalid(form)

        advance(self.object, user=self.request.user)
        self.object.save()
        messages.success(self.request, "Shadow Archetype selected successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WraithPassionsView(PointAllocationView):
    model = Wraith
    form_class = PassionForm
    template_name = "characters/wraith/wraith/chargen.html"
    allocation_name = "passion"
    total_attribute = "passion_points"
    spent_method = "total_passion_rating"
    complete_method = "has_passions"
    completion_message = "All Passions allocated successfully!"

    def add_record(self, obj, data):
        obj.add_passion(
            emotion=data["emotion"],
            description=data["description"],
            rating=data["rating"],
            is_dark=data.get("is_dark_passion", False),
        )


class WraithFettersView(PointAllocationView):
    model = Wraith
    form_class = FetterForm
    template_name = "characters/wraith/wraith/chargen.html"
    allocation_name = "fetter"
    total_attribute = "fetter_points"
    spent_method = "total_fetter_rating"
    complete_method = "has_fetters"
    completion_message = "All Fetters allocated successfully!"

    def add_record(self, obj, data):
        obj.add_fetter(
            fetter_type=data["fetter_type"],
            description=data["description"],
            rating=data["rating"],
        )


class WraithExtrasView(CharacterExtrasView):
    model = Wraith
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "age_at_death",
        "death_description",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/wraith/wraith/chargen.html"
    success_message = "Character details saved successfully!"
    field_widget_attrs = {
        "description": {
            "placeholder": "Describe your character's physical appearance (as a wraith). Be detailed, this will be visible to other players."
        },
        "death_description": {
            "placeholder": "Describe how your character died. This is crucial for understanding your wraith's nature."
        },
        "history": {
            "placeholder": "Describe character history/backstory from when they were alive and how they've adapted to being a wraith."
        },
        "goals": {
            "placeholder": "Describe your character's long and short term goals as a wraith."
        },
    }

    def validate_extras(self, form):
        if not form.cleaned_data.get("age_at_death"):
            form.add_error("age_at_death", "Age at death is required")
            messages.error(self.request, "Age at death is required for Wraith characters.")
            return False
        if not form.cleaned_data.get("death_description"):
            form.add_error("death_description", "Death description is required")
            messages.error(self.request, "Death description is required for Wraith characters.")
            return False
        return True

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WraithFreebiesView(HumanFreebiesView):
    """Freebie spending view for Wraith characters.

    Inherits form_valid() from HumanFreebiesView which uses the
    FreebieSpendingServiceFactory to automatically select the correct
    WraithFreebieSpendingService with Wraith-specific handlers.
    """

    model = Wraith
    form_class = WraithFreebiesForm
    template_name = "characters/wraith/wraith/chargen.html"


class WraithLanguagesView(HumanLanguagesView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"
    success_message = "Languages added successfully!"


class WraithAlliesView(GenericBackgroundView):
    primary_object_class = Wraith
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wraith/chargen.html"


class WraithMentorView(GenericBackgroundView):
    primary_object_class = Wraith
    background_name = "mentor"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wraith/chargen.html"


class WraithContactsView(GenericBackgroundView):
    primary_object_class = Wraith
    background_name = "contacts"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wraith/chargen.html"


class WraithSpecialtiesView(HumanSpecialtiesView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"
    success_message = "Wraith '{name}' submitted for approval!"


class WraithCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Wraith
    key_property = "creation_status"
    default_redirect = WraithDetailView
