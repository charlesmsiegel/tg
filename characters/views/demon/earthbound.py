from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView

from characters.forms.core.crud_fields import EARTHBOUND_CREATE_FIELDS, EARTHBOUND_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.demon import Earthbound
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


class EarthboundDetailView(XPApprovalMixin, HumanDetailView):
    model = Earthbound
    template_name = "characters/demon/earthbound/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EarthboundCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Earthbound
    fields = EARTHBOUND_CREATE_FIELDS
    template_name = "characters/demon/earthbound/form.html"
    success_message = "Earthbound '{name}' created successfully!"
    error_message = "Failed to create earthbound. Please correct the errors below."


class EarthboundUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Earthbound
    fields = EARTHBOUND_UPDATE_FIELDS
    template_name = "characters/demon/earthbound/form.html"
    success_message = "Earthbound '{name}' updated successfully!"
    error_message = "Failed to update earthbound. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EarthboundListView(VisibilityFilterMixin, ListView):
    model = Earthbound
    template_name = "characters/demon/earthbound/list.html"
    context_object_name = "earthbounds"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        return qs.select_related("owner", "house", "chronicle").order_by("name")
