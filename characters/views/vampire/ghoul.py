from typing import Any

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.vampire.ghoul import Ghoul
from characters.views.core.human import HumanDetailView
from core.mixins import MessageMixin, XPApprovalMixin
from core.permissions import Permission, PermissionManager
from django.views.generic import CreateView, ListView, UpdateView


class GhoulDetailView(XPApprovalMixin, HumanDetailView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["disciplines"] = self.object.get_disciplines()
        return context


class GhoulCreateView(MessageMixin, CreateView):
    model = Ghoul
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "domitor",
        "is_independent",
    ]
    template_name = "characters/vampire/ghoul/form.html"
    success_message = "Ghoul created successfully."
    error_message = "Error creating ghoul."


class GhoulUpdateView(MessageMixin, UpdateView):
    model = Ghoul
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "domitor",
        "is_independent",
        "blood_pool",
        "max_blood_pool",
        "years_as_ghoul",
        # Disciplines
        "potence",
        "celerity",
        "fortitude",
        "auspex",
        "dominate",
        "obfuscate",
        "presence",
    ]
    template_name = "characters/vampire/ghoul/form.html"
    success_message = "Ghoul updated successfully."
    error_message = "Error updating ghoul."

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


class GhoulListView(ListView):
    model = Ghoul
    ordering = ["name"]
    template_name = "characters/vampire/ghoul/list.html"
