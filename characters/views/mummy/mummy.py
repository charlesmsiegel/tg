from typing import Any

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.mummy.mummy import MummyCreationForm
from characters.models.mummy.mummy import Mummy
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)
from core.permissions import Permission, PermissionManager
from django.views.generic import CreateView, ListView, UpdateView


class MummyDetailView(XPApprovalMixin, HumanDetailView):
    model = Mummy
    template_name = "characters/mummy/mummy/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["hekau"] = self.object.get_hekau()
        if self.object.dynasty:
            context["dynasty"] = self.object.dynasty
        return context


class MummyCreateView(MessageMixin, CreateView):
    model = Mummy
    form_class = MummyCreationForm
    template_name = "characters/mummy/mummy/form.html"
    success_message = "Mummy '{name}' created successfully!"
    error_message = "Failed to create mummy. Please correct the errors below."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MummyUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Mummy
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "dynasty",
        "web",
        "ancient_name",
        "balance",
        "sekhem",
        "ba",
        "conviction",
        "restraint",
        "incarnation",
        "years_since_rebirth",
        "mummified_appearance",
        "can_pass_as_mortal",
        # Hekau
        "alchemy",
        "celestial",
        "effigy",
        "necromancy",
        "nomenclature",
        "ushabti",
        "judge",
        "phoenix",
        "vision",
        "divination",
        # Text fields
        "death_in_first_life",
        "past_lives_memory",
        "description",
        "notes",
    ]
    template_name = "characters/mummy/mummy/form.html"
    success_message = "Mummy '{name}' updated successfully!"
    error_message = "Failed to update mummy. Please correct the errors below."

    def get_form_class(self):
        """Return different form based on user permissions."""
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )
        if has_full_edit:
            return super().get_form_class()
        return LimitedHumanEditForm


class MummyListView(VisibilityFilterMixin, ListView):
    model = Mummy
    template_name = "characters/mummy/mummy/list.html"
    context_object_name = "mummies"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "dynasty", "chronicle").order_by("name")
