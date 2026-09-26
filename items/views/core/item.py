from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from core.mixins import EditPermissionMixin, MessageMixin
from core.permissions import PermissionManager
from items.forms.core.limited_edit import LimitedItemEditForm
from items.registry import registry


class _ItemCreateView(LoginRequiredMixin, MessageMixin, CreateView):

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form

    def form_valid(self, form):
        # Set owner to current user if not already set
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)


ItemCreateView = registry.view("items.ItemModel", "create")


class _ItemUpdateView(EditPermissionMixin, MessageMixin, UpdateView):

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedItemEditForm.
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
            return LimitedItemEditForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only customize fields if they exist in the form
        if "name" in form.fields:
            form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        if "description" in form.fields:
            form.fields["description"].widget.attrs.update(
                {"placeholder": "Enter description here"}
            )
        return form


ItemUpdateView = registry.view("items.ItemModel", "update")


ItemDetailView = registry.view("items.ItemModel", "detail")
ItemListView = registry.view("items.ItemModel", "list")
