from typing import Any

from core.mixins import EditPermissionMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import FormView
from locations.forms.changeling.freehold import FreeholdForm
from locations.models.changeling import Freehold


class FreeholdDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Freehold"""
    model = Freehold
    template_name = "locations/changeling/freehold/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Add any additional context needed for the template
        context["feature_points"] = self.object.get_total_feature_points()
        context["holdings_required"] = self.object.get_holdings_required()
        return context


class FreeholdListView(ListView):
    """List view for all Freeholds"""
    model = Freehold
    ordering = ["name"]
    template_name = "locations/changeling/freehold/list.html"


class FreeholdCreateView(LoginRequiredMixin, FormView):
    """Create view for a new Freehold"""
    template_name = "locations/changeling/freehold/form.html"
    form_class = FreeholdForm
    success_message = "Freehold '{name}' created successfully!"
    error_message = "Failed to create freehold. Please correct the errors below."

    def form_valid(self, form):
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
        if hasattr(self, 'object'):
            context['object'] = self.object
        return context


class FreeholdUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Freehold"""
    model = Freehold
    form_class = FreeholdForm
    template_name = "locations/changeling/freehold/form.html"
    success_message = "Freehold '{name}' updated successfully!"
    error_message = "Failed to update freehold. Please correct the errors below."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feature_points"] = self.object.get_total_feature_points()
        context["holdings_required"] = self.object.get_holdings_required()
        return context
