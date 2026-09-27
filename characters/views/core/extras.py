"""Biography form presentation and persistence, with explicit gameline hooks."""

from django import forms
from django.contrib import messages
from django.db import transaction
from django.views.generic import UpdateView

from characters.chargen.transitions import advance
from characters.views.core.chargen_mixins import ChargenStepMixin
from core.mixins import SpecialUserMixin


class CharacterExtrasView(ChargenStepMixin, SpecialUserMixin, UpdateView):
    date_fields = ("date_of_birth",)
    optional_fields = ()
    field_help_text = {}
    field_widget_attrs = {}
    success_message = None

    default_widget_attrs = {
        "description": {
            "placeholder": "Describe your character's physical appearance. Be detailed, this will be visible to other players."
        },
        "history": {
            "placeholder": "Describe your character's history and background, including important people and events."
        },
        "goals": {"placeholder": "Describe your character's long and short term goals."},
        "notes": {"placeholder": "Notes"},
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character."
        },
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name in self.date_fields:
            form.fields[name].widget = forms.DateInput(attrs={"type": "date"})
        for name in self.optional_fields:
            form.fields[name].required = False
        for name, attrs in {**self.default_widget_attrs, **self.field_widget_attrs}.items():
            if name in form.fields:
                form.fields[name].widget.attrs.update(attrs)
        for name, help_text in self.field_help_text.items():
            form.fields[name].help_text = help_text
        return form

    def validate_extras(self, form):
        """Attach any gameline errors before saving or advancing."""
        return True

    def prepare_character(self, form):
        """Apply existing gameline effects before navigation tests applicability."""

    @transaction.atomic
    def form_valid(self, form):
        if not self.validate_extras(form):
            return self.form_invalid(form)
        self.prepare_character(form)
        advance(self.object, user=self.request.user)
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response
