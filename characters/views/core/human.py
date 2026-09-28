from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from characters.chargen import get_workflow
from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.crud_fields import HUMAN_CREATE_FIELDS, HUMAN_UPDATE_FIELDS
from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.models.core import Human
from characters.models.core.specialty import Specialty
from characters.rules.limits import ability_rule, attribute_rule
from characters.views.core.allocations import AllocationStepMixin
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.character import CharacterDetailView
from characters.views.core.chargen_mixins import ChargenProgressMixin, ChargenStepMixin
from characters.views.core.form_steps import CharacterFormStepView
from characters.views.core.spending import FreebieSpendingView
from core.forms.language import HumanLanguageForm
from core.htmx import hx_redirect, is_fragment_request, vary_on_htmx
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedEditFormMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SuccessMessageMixin,
    prepare_created_object,
)
from core.models import Language
from core.views.generic import DictView


class HumanDetailView(CharacterDetailView):
    """Detail view for Human characters. Inherits permissions from CharacterDetailView."""

    model = Human
    template_name = "characters/core/human/detail.html"


class HumanCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    """Create view for Human characters."""

    model = Human
    fields = HUMAN_CREATE_FIELDS
    template_name = "characters/core/human/form.html"
    success_message = "Human created successfully."
    error_message = "Error creating Human."

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        return super().form_valid(form)


class HumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    """
    Update view for Human characters.
    Only STs and Admins can directly edit character fields; an owner (who may reach
    this page while the character is a draft) gets the limited form, and sets traits
    through the creation workflow or XP spending, which enforce the rules.
    """

    model = Human
    fields = HUMAN_UPDATE_FIELDS
    limited_form_class = LimitedHumanEditForm
    template_name = "characters/core/human/form.html"
    success_message = "Human updated successfully."
    error_message = "Error updating Human."


class HumanBasicsView(LoginRequiredMixin, CreateView):
    """First step of character creation."""

    model = Human
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
    ]
    template_name = "characters/core/human/humanbasics.html"

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        return super().form_valid(form)


class HumanAttributeView(
    AllocationStepMixin, ChargenStepMixin, SpendFreebiesPermissionMixin, UpdateView
):
    """
    Character creation step: allocating attribute points.
    Uses SpendFreebiesPermissionMixin - only owners of unfinished characters can access.
    """

    model = Human
    fields = [
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
    ]
    template_name = "characters/core/human/attributes.html"

    primary = 7
    secondary = 5
    tertiary = 3

    def get_allocation_rules(self):
        return [attribute_rule(self.primary, self.secondary, self.tertiary)]

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["primary"] = self.primary
        context["secondary"] = self.secondary
        context["tertiary"] = self.tertiary
        return context


class HumanAbilityView(
    AllocationStepMixin,
    ChargenStepMixin,
    SpendFreebiesPermissionMixin,
    SpecialUserMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Human
    fields = Human.primary_abilities
    template_name = "characters/core/human/chargen.html"
    primary = 11
    secondary = 7
    tertiary = 4
    rating_error_message = ""
    allocation_error_message = ""

    def get_allocation_rules(self):
        return [
            ability_rule(
                self.model,
                tuple(self.fields),
                self.primary,
                self.secondary,
                self.tertiary,
                range_flash=self.rating_error_message,
                flash=self.allocation_error_message,
            )
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(primary=self.primary, secondary=self.secondary, tertiary=self.tertiary)
        return context

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        return super().form_valid(form)


class HumanBiographicalInformation(ChargenStepMixin, SpendFreebiesPermissionMixin, UpdateView):
    model = Human
    fields = [
        "age",
        "apparent_age",
        "date_of_birth",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/core/human/bio.html"

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class HumanFreebiesView(FreebieSpendingView):
    """Human adapter for the shared service-based spending lifecycle."""

    model = Human
    form_class = HumanFreebiesForm
    template_name = "characters/core/human/chargen_form.html"


class HumanLanguagesView(CharacterFormStepView):
    form_class = HumanLanguageForm
    template_name = "characters/core/human/chargen_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        character = self.get_object()
        kwargs.update(pk=character.pk, num_languages=int(character.num_languages()))
        return kwargs

    def form_valid(self, form):
        character = self.get_object()
        english, _ = Language.objects.get_or_create(name="English")
        character.languages.add(english)
        for field in form.fields:
            name = form.cleaned_data[field]
            if name:
                language, _ = Language.objects.get_or_create(name=name)
                character.languages.add(language)
        advance(character, user=self.request.user)
        return super().form_valid(form)


class HumanSpecialtiesView(CharacterFormStepView):
    form_class = SpecialtiesForm
    template_name = "characters/core/human/chargen.html"

    def get_specialties_needed(self):
        return self.get_object().needed_specialties()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["object"] = self.get_object()
        kwargs["specialties_needed"] = self.get_specialties_needed()
        return kwargs

    def form_valid(self, form):
        character = self.get_object()
        for field in form.fields:
            specialty, _ = Specialty.objects.get_or_create(
                name=form.cleaned_data[field], stat=field
            )
            character.specialties.add(specialty)
        character.status = "Sub"
        character.save()
        return super().form_valid(form)


# Compatibility for existing callers; order and labels belong to the registry.
HUMAN_CHARGEN_STEPS = [(i, step.label) for i, step in enumerate(get_workflow("human").steps, 1)]


class HumanAttributeChargenView(ChargenProgressMixin, HumanAttributeView):
    chargen_step_labels = HUMAN_CHARGEN_STEPS


class HumanAbilityChargenView(ChargenProgressMixin, HumanAbilityView):
    chargen_step_labels = HUMAN_CHARGEN_STEPS


class HumanBackgroundsChargenView(ChargenProgressMixin, HumanBackgroundsView):
    chargen_step_labels = HUMAN_CHARGEN_STEPS


class HumanBiographicalInformationChargenView(ChargenProgressMixin, HumanBiographicalInformation):
    chargen_step_labels = HUMAN_CHARGEN_STEPS


class HumanFreebiesChargenView(ChargenProgressMixin, HumanFreebiesView):
    chargen_step_labels = HUMAN_CHARGEN_STEPS


class HumanLanguagesChargenView(ChargenProgressMixin, HumanLanguagesView):
    chargen_step_labels = HUMAN_CHARGEN_STEPS


class HumanSpecialtiesChargenView(ChargenProgressMixin, HumanSpecialtiesView):
    chargen_step_labels = HUMAN_CHARGEN_STEPS


class HumanCharacterCreationView(DictView):
    chargen_router = True
    view_mapping = WorkflowViews()
    model_class = Human
    key_property = "creation_status"
    default_redirect = HumanDetailView

    def is_valid_key(self, obj, key):
        return key in self.view_mapping and obj.status in {"Un", "Rev"}

    def get_default_redirect(self, request, *args, **kwargs):
        # A step fragment was requested for a character that has left the
        # wizard (or that this user may only view): render the real page.
        if is_fragment_request(request):
            subject = kwargs.get("subject")
            target = subject.get_absolute_url() if subject is not None else request.path
            return vary_on_htmx(hx_redirect(target))
        return super().get_default_redirect(request, *args, **kwargs)
