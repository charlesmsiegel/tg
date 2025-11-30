from typing import Any

from characters.forms.core.limited_edit import LimitedMtRHumanEditForm
from characters.forms.mummy.mtr_human import MtRHumanCreationForm
from characters.models.mummy.mtr_human import MtRHuman
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    VisibilityFilterMixin,
)
from core.permissions import Permission, PermissionManager
from django.views.generic import CreateView, ListView, UpdateView


class MtRHumanDetailView(HumanDetailView):
    model = MtRHuman
    template_name = "characters/mummy/mtrhuman/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class MtRHumanCreateView(MessageMixin, CreateView):
    model = MtRHuman
    form_class = MtRHumanCreationForm
    template_name = "characters/mummy/mtrhuman/form.html"
    success_message = "Human (Mummy) '{name}' created successfully!"
    error_message = "Failed to create human. Please correct the errors below."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MtRHumanUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = MtRHuman
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "description",
        "notes",
    ]
    template_name = "characters/mummy/mtrhuman/form.html"
    success_message = "Human (Mummy) '{name}' updated successfully!"
    error_message = "Failed to update human. Please correct the errors below."

    def get_form_class(self):
        """Return different form based on user permissions."""
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )
        if has_full_edit:
            return super().get_form_class()
        return LimitedMtRHumanEditForm


class MtRHumanListView(VisibilityFilterMixin, ListView):
    model = MtRHuman
    template_name = "characters/mummy/mtrhuman/list.html"
    context_object_name = "humans"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "chronicle").order_by("name")
