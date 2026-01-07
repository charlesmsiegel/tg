from typing import Any

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.wraith.wraith import Wraith
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin, XPApprovalMixin
from core.permissions import Permission, PermissionManager
from django.views.generic import CreateView, UpdateView


class WraithDetailView(XPApprovalMixin, HumanDetailView):
    model = Wraith
    template_name = "characters/wraith/wraith/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["arcanoi"] = self.object.get_arcanoi()
        context["dark_arcanoi"] = self.object.get_dark_arcanoi()
        return context


class WraithCreateView(MessageMixin, CreateView):
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
    ]
    template_name = "characters/wraith/wraith/form.html"
    success_message = "Wraith '{name}' created successfully!"
    error_message = "Failed to create wraith. Please correct the errors below."


class WraithUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
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

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedHumanEditForm.
        STs and admins get full access via the default form.
        """
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )
        if has_full_edit:
            return super().get_form_class()
        else:
            return LimitedHumanEditForm
