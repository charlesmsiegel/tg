from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from core.mixins import EditPermissionMixin, MessageMixin
from core.permissions import PermissionManager
from items.forms.vampire import LimitedVampireArtifactEditForm, VampireArtifactForm

# VampireArtifact Views
from items.registry import registry


class _VampireArtifactCreateView(LoginRequiredMixin, MessageMixin, CreateView):

    def form_valid(self, form):
        # Set owner to current user if not already set
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)


VampireArtifactCreateView = registry.view("items.VampireArtifact", "create")


class _VampireArtifactUpdateView(EditPermissionMixin, MessageMixin, UpdateView):

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedVampireArtifactEditForm.
        STs and admins get full access to all fields.
        """
        # Check if user has full edit permission
        has_full_edit = PermissionManager.user_has_scoped_editor_role(
            self.request.user, self.get_object(), request=self.request
        )

        if has_full_edit:
            # STs and admins get all fields
            return VampireArtifactForm
        else:
            # Owners get limited fields (description, history)
            return LimitedVampireArtifactEditForm


VampireArtifactUpdateView = registry.view("items.VampireArtifact", "update")


# Bloodstone Views


VampireArtifactDetailView = registry.view("items.VampireArtifact", "detail")
VampireArtifactListView = registry.view("items.VampireArtifact", "list")
BloodstoneDetailView = registry.view("items.Bloodstone", "detail")
BloodstoneListView = registry.view("items.Bloodstone", "list")
BloodstoneCreateView = registry.view("items.Bloodstone", "create")
BloodstoneUpdateView = registry.view("items.Bloodstone", "update")
