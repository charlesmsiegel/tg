from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    prepare_created_object,
)
from core.permissions import PermissionManager
from locations.forms.core.limited_edit import LimitedLocationEditForm
from locations.registry import registry


class _LocationCreateView(LoginRequiredMixin, CreateView):

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["contained_within"].help_text = "Select one or more parent locations"
        return form

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        return super().form_valid(form)


LocationCreateView = registry.view("locations.LocationModel", "create")


class _LocationUpdateView(EditPermissionMixin, MessageMixin, UpdateView):

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedLocationEditForm.
        STs and admins get full access to all fields.
        """
        # Check if user has full edit permission
        has_full_edit = PermissionManager.user_has_scoped_editor_role(
            self.request.user, self.get_object(), request=self.request
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
        if "contained_within" in form.fields:
            form.fields["contained_within"].help_text = "Select one or more parent locations"
        return form


LocationUpdateView = registry.view("locations.LocationModel", "update")


LocationDetailView = registry.view("locations.LocationModel", "detail")
LocationListView = registry.view("locations.LocationModel", "list")
