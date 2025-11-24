from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from core.permissions import Permission, PermissionManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.forms.vampire import LimitedVampireArtifactEditForm, VampireArtifactForm
from items.models.vampire import Bloodstone, VampireArtifact


# VampireArtifact Views
class VampireArtifactDetailView(ViewPermissionMixin, DetailView):
    model = VampireArtifact
    template_name = "items/vampire/artifact/detail.html"


class VampireArtifactCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = VampireArtifact
    form_class = VampireArtifactForm
    template_name = "items/vampire/artifact/form.html"
    success_message = "Vampire Artifact '{name}' created successfully!"
    error_message = "Failed to create Vampire Artifact. Please correct the errors below."

    def form_valid(self, form):
        # Set owner to current user if not already set
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class VampireArtifactUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = VampireArtifact
    form_class = VampireArtifactForm
    template_name = "items/vampire/artifact/form.html"
    success_message = "Vampire Artifact '{name}' updated successfully!"
    error_message = "Failed to update Vampire Artifact. Please correct the errors below."

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedVampireArtifactEditForm.
        STs and admins get full access to all fields.
        """
        # Check if user has full edit permission
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )

        if has_full_edit:
            # STs and admins get all fields
            return VampireArtifactForm
        else:
            # Owners get limited fields (description, history)
            return LimitedVampireArtifactEditForm


class VampireArtifactListView(ListView):
    model = VampireArtifact
    ordering = ["name"]
    template_name = "items/vampire/artifact/list.html"


# Bloodstone Views
class BloodstoneDetailView(DetailView):
    model = Bloodstone
    template_name = "items/vampire/bloodstone/detail.html"


class BloodstoneCreateView(CreateView):
    model = Bloodstone
    fields = [
        "name",
        "description",
        "blood_stored",
        "max_blood",
        "is_active",
        "created_by_generation",
        "stone_type",
    ]
    template_name = "items/vampire/bloodstone/form.html"


class BloodstoneUpdateView(UpdateView):
    model = Bloodstone
    fields = [
        "name",
        "description",
        "blood_stored",
        "max_blood",
        "is_active",
        "created_by_generation",
        "stone_type",
    ]
    template_name = "items/vampire/bloodstone/form.html"


class BloodstoneListView(ListView):
    model = Bloodstone
    ordering = ["name"]
    template_name = "items/vampire/bloodstone/list.html"
