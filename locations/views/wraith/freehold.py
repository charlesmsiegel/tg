from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ViewPermissionMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.wraith import WraithFreehold


class WraithFreeholdDetailView(ViewPermissionMixin, DetailView):
    model = WraithFreehold
    template_name = "locations/wraith/freehold/detail.html"


class WraithFreeholdCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = WraithFreehold
    fields = [
        "name",
        "description",
        "parent",
        "population",
        "government_type",
        "leader",
        "hierarchy_relation",
        "allied_factions",
        "defense_rating",
        "resource_level",
        "has_soulforges",
        "has_library",
        "has_safe_passage",
        "hidden",
        "founding_principle",
    ]
    template_name = "locations/wraith/freehold/form.html"
    success_message = "Wraith Freehold '{name}' created successfully!"
    error_message = "Failed to create freehold. Please correct the errors below."


class WraithFreeholdUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = WraithFreehold
    fields = [
        "name",
        "description",
        "parent",
        "population",
        "government_type",
        "leader",
        "hierarchy_relation",
        "allied_factions",
        "defense_rating",
        "resource_level",
        "has_soulforges",
        "has_library",
        "has_safe_passage",
        "hidden",
        "founding_principle",
    ]
    template_name = "locations/wraith/freehold/form.html"
    success_message = "Wraith Freehold '{name}' updated successfully!"
    error_message = "Failed to update freehold. Please correct the errors below."


class WraithFreeholdListView(ListView):
    model = WraithFreehold
    ordering = ["name"]
    template_name = "locations/wraith/freehold/list.html"
