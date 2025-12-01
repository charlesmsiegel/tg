from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.demon.bastion import Bastion


class BastionDetailView(ViewPermissionMixin, DetailView):
    model = Bastion
    template_name = "locations/demon/bastion/detail.html"


class BastionListView(ListView):
    model = Bastion
    ordering = ["name"]
    template_name = "locations/demon/bastion/list.html"


class BastionCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Bastion
    fields = [
        "name",
        "parent",
        "description",
        "ritual_strength",
        "warding_level",
        "consecration_date",
    ]
    template_name = "locations/demon/bastion/form.html"
    success_message = "Bastion '{name}' created successfully!"
    error_message = "Failed to create bastion. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["parent"].empty_label = "Parent Location"
        return form


class BastionUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Bastion
    fields = [
        "name",
        "description",
        "parent",
        "ritual_strength",
        "warding_level",
        "consecration_date",
    ]
    template_name = "locations/demon/bastion/form.html"
    success_message = "Bastion '{name}' updated successfully!"
    error_message = "Failed to update bastion. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["parent"].empty_label = "Parent Location"
        return form
