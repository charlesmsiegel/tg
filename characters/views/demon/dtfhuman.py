from django.views.generic import ListView, UpdateView

from characters.forms.core.crud_fields import DT_F_HUMAN_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.demon import DtFHuman
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


class DtFHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/detail.html"


class DtFHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = DtFHuman
    success_message = "DtF Human updated successfully."
    error_message = "Error updating DtF Human."
    fields = DT_F_HUMAN_UPDATE_FIELDS
    template_name = "characters/demon/dtfhuman/form.html"

    limited_form_class = LimitedHumanEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DtFHumanListView(VisibilityFilterMixin, ListView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/list.html"
    context_object_name = "dtfhumans"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        return qs.select_related("owner", "chronicle").order_by("name")
