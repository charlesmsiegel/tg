from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import ViewPermissionMixin, EditPermissionMixin
from locations.models import LocationModel


class LocationDetailView(ViewPermissionMixin, DetailView):
    model = LocationModel
    template_name = "locations/core/location/detail.html"


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = LocationModel
    fields = [
        "name",
        "parent",
        "gauntlet",
        "shroud",
        "dimension_barrier",
        "description",
    ]
    template_name = "locations/core/location/form.html"
    success_message = "Location '{name}' created successfully!"
    error_message = "Failed to create location. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form


class LocationUpdateView(EditPermissionMixin, UpdateView):
    model = LocationModel
    fields = [
        "name",
        "parent",
        "gauntlet",
        "shroud",
        "dimension_barrier",
        "description",
    ]
    template_name = "locations/core/location/form.html"
    success_message = "Location '{name}' updated successfully!"
    error_message = "Failed to update location. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form
