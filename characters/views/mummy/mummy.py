from typing import Any

from django.views.generic import CreateView, ListView, UpdateView

from characters.forms.core.crud_fields import MUMMY_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.mummy.mummy import MummyCreationForm
from characters.models.mummy.mummy import Mummy
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


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


class MummyUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    model = Mummy
    fields = MUMMY_UPDATE_FIELDS
    template_name = "characters/mummy/mummy/form.html"
    success_message = "Mummy '{name}' updated successfully!"
    error_message = "Failed to update mummy. Please correct the errors below."

    limited_form_class = LimitedHumanEditForm


class MummyListView(VisibilityFilterMixin, ListView):
    model = Mummy
    template_name = "characters/mummy/mummy/list.html"
    context_object_name = "mummies"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "dynasty", "chronicle").order_by("name")
