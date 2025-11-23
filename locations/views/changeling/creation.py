"""
Multi-step views for Freehold creation.
Follows the pattern from character creation (DictView).
"""
from typing import Any

from core.mixins import EditPermissionMixin
from core.views.generic import DictView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView
from locations.forms.changeling.creation import (
    FreeholdBasicsForm,
    FreeholdDetailsForm,
    FreeholdFeaturesForm,
    FreeholdPowersForm,
)
from locations.models.changeling import Freehold
from locations.views.changeling.freehold import FreeholdDetailView


class FreeholdBasicsView(LoginRequiredMixin, CreateView):
    """
    Step 1: Basic information (Name, Archetype, Aspect, Acquisition).
    Creates the freehold object with creation_status = 1.
    """

    model = Freehold
    form_class = FreeholdBasicsForm
    template_name = "locations/changeling/freehold/chargen/basics.html"

    def form_valid(self, form):
        # Set owner if not set
        if not form.instance.owned_by and self.request.user.profile.characters.exists():
            form.instance.owned_by = self.request.user.profile.characters.first()

        # Set initial creation status
        form.instance.creation_status = 1

        return super().form_valid(form)

    def get_success_url(self):
        # Go to next step (Features)
        return self.object.get_update_url()


class FreeholdFeaturesView(EditPermissionMixin, UpdateView):
    """
    Step 2: Feature allocation (Balefire, Size, Sanctuary, Resources, Passages).
    Requires creation_status = 1.
    """

    model = Freehold
    form_class = FreeholdFeaturesForm
    template_name = "locations/changeling/freehold/chargen/features.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate current feature points for display
        if hasattr(self, "object"):
            context["current_feature_points"] = self.object.get_total_feature_points()
        return context

    def form_valid(self, form):
        # Increment creation status
        self.object.creation_status = 2
        self.object.save()

        # Store feature points in context for display
        feature_points = getattr(form, "feature_points", 0)
        self.feature_points = feature_points

        return super().form_valid(form)

    def get_success_url(self):
        # Go to next step (Powers)
        return self.object.get_update_url()


class FreeholdPowersView(EditPermissionMixin, UpdateView):
    """
    Step 3: Powers selection.
    Requires creation_status = 2.
    """

    model = Freehold
    form_class = FreeholdPowersForm
    template_name = "locations/changeling/freehold/chargen/powers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show current feature points
        if hasattr(self, "object"):
            context["feature_points"] = self.object.get_total_feature_points()
            context["holdings_required"] = self.object.get_holdings_required()
        return context

    def form_valid(self, form):
        # Increment creation status
        self.object.creation_status = 3
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Go to next step (Details)
        return self.object.get_update_url()


class FreeholdDetailsView(EditPermissionMixin, UpdateView):
    """
    Step 4: Final details and descriptions.
    Requires creation_status = 3.
    """

    model = Freehold
    form_class = FreeholdDetailsForm
    template_name = "locations/changeling/freehold/chargen/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show final tallies
        if hasattr(self, "object"):
            context["feature_points"] = self.object.get_total_feature_points()
            context["holdings_required"] = self.object.get_holdings_required()
        return context

    def form_valid(self, form):
        # Mark creation as complete
        self.object.creation_status = 5
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Go to freehold detail view
        return self.object.get_absolute_url()


class FreeholdCreationView(DictView):
    """
    Router view that directs to the appropriate step based on creation_status.
    Similar to HumanCharacterCreationView.
    """

    view_mapping = {
        1: FreeholdFeaturesView,
        2: FreeholdPowersView,
        3: FreeholdDetailsView,
    }
    model_class = Freehold
    key_property = "creation_status"
    default_redirect = FreeholdDetailView

    def is_valid_key(self, obj, key):
        # Only allow creation steps if status is "Un" (unfinished)
        return key in self.view_mapping and obj.status == "Un"
