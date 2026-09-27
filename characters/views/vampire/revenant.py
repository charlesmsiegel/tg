from typing import Any

from django.views.generic import CreateView, UpdateView

from characters.forms.core.crud_fields import REVENANT_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.vampire.revenant import Revenant
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin, ScopedEditFormMixin, XPApprovalMixin


class RevenantDetailView(XPApprovalMixin, HumanDetailView):
    model = Revenant
    template_name = "characters/vampire/revenant/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["disciplines"] = self.object.get_disciplines()
        context["family_disciplines"] = self.object.get_family_disciplines()
        return context


class RevenantCreateView(MessageMixin, CreateView):
    model = Revenant
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "family",
        "pseudo_generation",
    ]
    template_name = "characters/vampire/revenant/form.html"
    success_message = "Revenant created successfully."
    error_message = "Error creating revenant."


class RevenantUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    model = Revenant
    fields = REVENANT_UPDATE_FIELDS
    template_name = "characters/vampire/revenant/form.html"
    success_message = "Revenant updated successfully."
    error_message = "Error updating revenant."

    limited_form_class = LimitedHumanEditForm
