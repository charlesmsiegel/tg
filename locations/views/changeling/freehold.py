from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormView

from core.mixins import EditPermissionMixin, ViewPermissionMixin, prepare_created_object
from locations.registry import registry


class _FreeholdDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Freehold"""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Add any additional context needed for the template
        context["feature_points"] = self.object.get_total_feature_points()
        context["holdings_required"] = self.object.get_holdings_required()
        return context


FreeholdDetailView = registry.view("locations.Freehold", "detail")


class _FreeholdCreateView(LoginRequiredMixin, FormView):
    """Create view for a new Freehold"""

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        self.object = form.save()
        # Set the owner to the current user's first character if they have one
        if self.request.user.profile.characters.exists():
            self.object.owned_by = self.request.user.profile.characters.first()
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, "object"):
            context["object"] = self.object
        return context


FreeholdCreateView = registry.view("locations.Freehold", "create")


class _FreeholdUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Freehold"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feature_points"] = self.object.get_total_feature_points()
        context["holdings_required"] = self.object.get_holdings_required()
        return context


FreeholdUpdateView = registry.view("locations.Freehold", "update")


FreeholdListView = registry.view("locations.Freehold", "list")
