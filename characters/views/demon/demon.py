from django.views.generic import ListView, UpdateView

from characters.forms.core.crud_fields import DEMON_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.demon import Demon
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


class DemonDetailView(XPApprovalMixin, HumanDetailView):
    model = Demon
    template_name = "characters/demon/demon/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DemonUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Demon
    fields = DEMON_UPDATE_FIELDS
    template_name = "characters/demon/demon/form.html"
    success_message = "Demon '{name}' updated successfully!"
    error_message = "Failed to update demon. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DemonListView(VisibilityFilterMixin, ListView):
    model = Demon
    template_name = "characters/demon/demon/list.html"
    context_object_name = "demons"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        return qs.select_related("owner", "house", "faction", "chronicle").order_by("name")
