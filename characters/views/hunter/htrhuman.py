from django.views.generic import CreateView, ListView, UpdateView

from characters.forms.core.crud_fields import HT_R_HUMAN_CREATE_FIELDS, HT_R_HUMAN_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.hunter import HtRHuman
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


class HtRHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = HtRHuman
    template_name = "characters/hunter/htrhuman/detail.html"


class HtRHumanCreateView(MessageMixin, CreateView):
    model = HtRHuman
    fields = HT_R_HUMAN_CREATE_FIELDS
    template_name = "characters/hunter/htrhuman/form.html"
    success_message = "Human (Hunter) '{name}' created successfully!"
    error_message = "Failed to create human. Please correct the errors below."

    def get_success_url(self):
        return self.object.get_absolute_url()


class HtRHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = HtRHuman
    fields = HT_R_HUMAN_UPDATE_FIELDS
    template_name = "characters/hunter/htrhuman/form.html"
    success_message = "Human (Hunter) '{name}' updated successfully!"
    error_message = "Failed to update human. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm


class HtRHumanListView(VisibilityFilterMixin, ListView):
    model = HtRHuman
    template_name = "characters/hunter/htrhuman/list.html"
    context_object_name = "humans"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "chronicle").order_by("name")
