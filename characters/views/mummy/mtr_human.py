from django.views.generic import CreateView, ListView, UpdateView

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.mummy.mtr_human import MtRHumanCreationForm
from characters.models.mummy.mtr_human import MtRHuman
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)


class MtRHumanDetailView(XPApprovalMixin, HumanDetailView):
    model = MtRHuman
    template_name = "characters/mummy/mtrhuman/detail.html"


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


class MtRHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
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

    limited_form_class = LimitedHumanEditForm


class MtRHumanListView(VisibilityFilterMixin, ListView):
    model = MtRHuman
    template_name = "characters/mummy/mtrhuman/list.html"
    context_object_name = "humans"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "chronicle").order_by("name")
