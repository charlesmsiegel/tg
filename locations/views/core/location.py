from core.mixins import EditPermissionMixin, ViewPermissionMixin
from core.mixins import MessageMixin
from core.permissions import Permission, PermissionManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from locations.forms.core.limited_edit import LimitedLocationEditForm
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

    def form_valid(self, form):
        # Set owner to current user if not already set
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class LocationUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
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

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedLocationEditForm.
        STs and admins get full access to all fields.
        """
        # Check if user has full edit permission
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )

        if has_full_edit:
            # STs and admins get all fields
            return super().get_form_class()
        else:
            # Owners get limited fields (description, public_info, image)
            return LimitedLocationEditForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only customize fields if they exist in the form
        if "name" in form.fields:
            form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        if "description" in form.fields:
            form.fields["description"].widget.attrs.update(
                {"placeholder": "Enter description here"}
            )
        if "parent" in form.fields:
            form.fields["parent"].empty_label = "Parent Location"
        return form
