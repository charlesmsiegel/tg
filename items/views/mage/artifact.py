from typing import Any

from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.mage import WonderResonanceRating
from items.models.mage.artifact import Artifact


class ArtifactDetailView(DetailView):
    model = Artifact
    template_name = "items/mage/artifact/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(
            wonder=self.object
        ).order_by("resonance__name")
        return context


class ArtifactListView(ListView):
    model = Artifact
    ordering = ["name"]
    template_name = "items/mage/artifact/list.html"


class ArtifactCreateView(MessageMixin, CreateView):
    model = Artifact
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "power",
    ]
    template_name = "items/mage/artifact/form.html"
    success_message = "Artifact '{name}' created successfully!"
    error_message = "Failed to create Artifact. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class ArtifactUpdateView(MessageMixin, UpdateView):
    model = Artifact
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "power",
    ]
    template_name = "items/mage/artifact/form.html"
    success_message = "Artifact '{name}' updated successfully!"
    error_message = "Failed to update Artifact. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
