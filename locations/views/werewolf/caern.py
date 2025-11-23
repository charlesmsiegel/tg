from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.werewolf.caern import Caern


class CaernDetailView(ViewPermissionMixin, DetailView):
    model = Caern
    template_name = "locations/werewolf/caern/detail.html"


class CaernListView(ListView):
    model = Caern
    ordering = ["name"]
    template_name = "locations/werewolf/caern/list.html"


class CaernCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Caern
    fields = [
        "name",
        "parent",
        "description",
        "rank",
        "caern_type",
    ]
    template_name = "locations/werewolf/caern/form.html"
    success_message = "Caern '{name}' created successfully!"
    error_message = "Failed to create caern. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form


class CaernUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Caern
    fields = [
        "name",
        "description",
        "parent",
        "rank",
        "caern_type",
    ]
    template_name = "locations/werewolf/caern/form.html"
    success_message = "Caern '{name}' updated successfully!"
    error_message = "Failed to update caern. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form
