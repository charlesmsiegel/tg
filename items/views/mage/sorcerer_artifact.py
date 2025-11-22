from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.mage.sorcerer_artifact import SorcererArtifact


class SorcererArtifactDetailView(DetailView):
    model = SorcererArtifact
    template_name = "items/mage/sorcerer_artifact/detail.html"


class SorcererArtifactListView(ListView):
    model = SorcererArtifact
    ordering = ["name"]
    template_name = "items/mage/sorcerer_artifact/list.html"


class SorcererArtifactCreateView(MessageMixin, CreateView):
    model = SorcererArtifact
    fields = ["name", "rank", "background_cost", "description", "power"]
    template_name = "items/mage/sorcerer_artifact/form.html"
    success_message = "Sorcerer Artifact '{name}' created successfully!"
    error_message = (
        "Failed to create Sorcerer Artifact. Please correct the errors below."
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class SorcererArtifactUpdateView(MessageMixin, UpdateView):
    model = SorcererArtifact
    fields = ["name", "rank", "background_cost", "description", "power"]
    template_name = "items/mage/sorcerer_artifact/form.html"
    success_message = "Sorcerer Artifact '{name}' updated successfully!"
    error_message = (
        "Failed to update Sorcerer Artifact. Please correct the errors below."
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
