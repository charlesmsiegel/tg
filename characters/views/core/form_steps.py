"""Shared lifecycle for character steps backed by plain Django forms.

The registry authorizes and navigates; a step supplies its form and persistence.
Named gameline adapters configure the model, template and optional feedback.
"""

from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from characters.models.core import Human
from characters.views.core.chargen_mixins import ChargenStepMixin
from core.mixins import SpecialUserMixin, SpendFreebiesPermissionMixin, SuccessMessageMixin


class CharacterFormStepView(
    ChargenStepMixin,
    SpendFreebiesPermissionMixin,
    SpecialUserMixin,
    SuccessMessageMixin,
    FormView,
):
    model = Human
    template_name = "characters/core/chargen.html"

    def get_object(self):
        if getattr(self, "object", None) is None:
            self.object = get_object_or_404(self.model, pk=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["is_approved_user"] = self.get_is_approved_user(self.object)
        return context

    def get_success_url(self):
        return self.get_object().get_absolute_url()
