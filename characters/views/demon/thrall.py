from django.views.generic import ListView, UpdateView

from characters.forms.core.crud_fields import THRALL_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.demon import Thrall
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


class ThrallDetailView(XPApprovalMixin, HumanDetailView):
    model = Thrall
    template_name = "characters/demon/thrall/detail.html"


class ThrallUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Thrall
    success_message = "Thrall updated successfully."
    error_message = "Error updating thrall."
    fields = THRALL_UPDATE_FIELDS
    template_name = "characters/demon/thrall/form.html"

    limited_form_class = LimitedHumanEditForm


class ThrallListView(VisibilityFilterMixin, ListView):
    model = Thrall
    template_name = "characters/demon/thrall/list.html"
    context_object_name = "thralls"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        return qs.select_related("owner", "master", "chronicle").order_by("name")
