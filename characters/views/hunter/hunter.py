from django.views.generic import CreateView, ListView, UpdateView

from characters.forms.core.crud_fields import HUNTER_CREATE_FIELDS, HUNTER_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.hunter import Hunter
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


class HunterDetailView(XPApprovalMixin, HumanDetailView):
    model = Hunter
    template_name = "characters/hunter/hunter/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edges"] = self.object.get_edges()
        return context


class HunterCreateView(MessageMixin, CreateView):
    model = Hunter
    fields = HUNTER_CREATE_FIELDS
    template_name = "characters/hunter/hunter/form.html"
    success_message = "Hunter '{name}' created successfully!"
    error_message = "Failed to create hunter. Please correct the errors below."

    def get_success_url(self):
        return self.object.get_absolute_url()


class HunterUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = Hunter
    fields = HUNTER_UPDATE_FIELDS
    template_name = "characters/hunter/hunter/form.html"
    success_message = "Hunter '{name}' updated successfully!"
    error_message = "Failed to update hunter. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm


class HunterListView(VisibilityFilterMixin, ListView):
    model = Hunter
    template_name = "characters/hunter/hunter/list.html"
    context_object_name = "hunters"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "creed", "chronicle").order_by("name")
