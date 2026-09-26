from typing import Any

from django.views.generic import UpdateView

from characters.forms.core.crud_fields import VAMPIRE_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.vampire.vampire import Vampire
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin, ScopedEditFormMixin, XPApprovalMixin


class VampireDetailView(XPApprovalMixin, HumanDetailView):
    model = Vampire
    template_name = "characters/vampire/vampire/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["disciplines"] = self.object.get_disciplines()
        if self.object.clan:
            context["clan_disciplines"] = self.object.get_clan_disciplines()
        return context


class VampireUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    model = Vampire
    fields = VAMPIRE_UPDATE_FIELDS
    template_name = "characters/vampire/vampire/form.html"
    success_message = "Vampire '{name}' updated successfully!"
    error_message = "Failed to update vampire. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm
