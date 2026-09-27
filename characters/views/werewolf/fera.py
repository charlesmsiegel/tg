from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.forms.core.crud_fields import FERA_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.werewolf.fera import (
    FeraCreationForm,
    FeraFirstChangeForm,
    FeraStartingGiftsForm,
)
from characters.models.werewolf.fera import Fera
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
)
from core.permissions import PermissionManager


class FeraDetailView(HumanDetailView):
    model = Fera
    template_name = "characters/werewolf/fera/detail.html"


class FeraUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Fera
    success_message = "Fera updated successfully."
    error_message = "Error updating fera."
    fields = FERA_UPDATE_FIELDS
    template_name = "characters/werewolf/fera/form.html"

    limited_form_class = LimitedHumanEditForm


class FeraBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = FeraCreationForm
    template_name = "characters/werewolf/fera/basics.html"

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
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class FeraBreedFactionView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    """Breed and faction-like choices; each Changing Breed declares its own."""

    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"

    def get_form_class(self):
        obj = self.get_object()
        return forms.modelform_factory(type(obj), fields=list(obj.chargen_choice_fields))

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field, help_text in self.object.chargen_field_help().items():
            if field in form.fields:
                form.fields[field].help_text = help_text
        for field in self.object.optional_choice_fields:
            form.fields[field].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fera_type"] = type(self.object).__name__
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.apply_chargen_choices(form.changed_data)
        advance(obj, user=self.request.user)
        obj.save()
        return super().form_valid(form)


class FeraAttributeView(HumanAttributeView):
    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"


class FeraAbilityView(WtAHumanAbilityView):
    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class FeraBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/fera/chargen.html"


class FeraGiftsView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Fera
    form_class = FeraStartingGiftsForm
    template_name = "characters/werewolf/fera/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object.starting_gift_groups())
        return context

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class FeraHistoryView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    model = Fera
    form_class = FeraFirstChangeForm
    template_name = "characters/werewolf/fera/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["first_change"].widget.attrs.update(
            {
                "placeholder": "Describe your character's First Change. Include where they were, what triggered it, and how they dealt with the immediate aftermath."
            }
        )
        form.fields["first_change"].help_text = (
            "This is a pivotal moment in every shapeshifter's life."
        )
        form.fields["age_of_first_change"].help_text = (
            "The age at which the character first changed forms."
        )
        return form

    def form_valid(self, form):
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class FeraExtrasView(CharacterExtrasView):
    model = Fera
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
    template_name = "characters/werewolf/fera/chargen.html"
    field_widget_attrs = {
        "description": {
            "placeholder": "Describe your character's physical appearance in all forms. Be detailed, this will be visible to other players."
        },
        "history": {
            "placeholder": "Describe character history/backstory. Include information about their upbringing, their First Change (already detailed above), and their role among their kind."
        },
        "goals": {
            "placeholder": "Describe your character's long and short term goals, whether personal or related to Gaia's war."
        },
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character. Include Renown, deeds, and anything else that would be publicly known."
        },
    }


class FeraFreebiesView(HumanFreebiesView):
    model = Fera
    form_class = ChainedHumanFreebiesForm
    template_name = "characters/werewolf/fera/chargen.html"


class FeraLanguagesView(HumanLanguagesView):
    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"


class FeraAlliesView(GenericBackgroundView):
    primary_object_class = Fera
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/fera/chargen.html"


class FeraSpecialtiesView(HumanSpecialtiesView):
    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"


class FeraCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Fera
    key_property = "creation_status"
    default_redirect = FeraDetailView
