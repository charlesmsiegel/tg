from typing import Any

from django.views.generic import UpdateView

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.wraith.wraith import Wraith
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin, ScopedEditFormMixin, XPApprovalMixin


class WraithDetailView(XPApprovalMixin, HumanDetailView):
    model = Wraith
    template_name = "characters/wraith/wraith/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["arcanoi"] = self.object.get_arcanoi()
        context["dark_arcanoi"] = self.object.get_dark_arcanoi()
        context["fetters"] = self.object.fetters.all()
        context["passions"] = self.object.passions.all()
        return context


class WraithUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    model = Wraith
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "guild",
        "legion",
        "faction",
        "corpus",
        "pathos",
        "temporary_pathos",
        "angst",
        "temporary_angst",
        "willpower",
        "death_description",
        "age_at_death",
    ]
    template_name = "characters/wraith/wraith/form.html"
    success_message = "Wraith '{name}' updated successfully!"
    error_message = "Failed to update wraith. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm
