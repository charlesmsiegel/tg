from typing import Any

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.vampire.revenant import Revenant
from characters.views.core.human import HumanDetailView
from core.mixins import MessageMixin, XPApprovalMixin
from core.permissions import Permission, PermissionManager
from django.views.generic import CreateView, ListView, UpdateView


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


class RevenantUpdateView(MessageMixin, UpdateView):
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
        "blood_pool",
        "max_blood_pool",
        "actual_age",
        "apparent_age",
        "family_flaw",
        # Disciplines
        "potence",
        "celerity",
        "fortitude",
        "auspex",
        "dominate",
        "obfuscate",
        "presence",
        "animalism",
        "necromancy",
        "vicissitude",
    ]
    template_name = "characters/vampire/revenant/form.html"
    success_message = "Revenant updated successfully."
    error_message = "Error updating revenant."

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


class RevenantListView(ListView):
    model = Revenant
    ordering = ["name"]
    template_name = "characters/vampire/revenant/list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("family")
