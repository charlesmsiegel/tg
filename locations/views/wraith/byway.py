from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ViewPermissionMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.wraith import Byway


class BywayDetailView(ViewPermissionMixin, DetailView):
    model = Byway
    template_name = "locations/wraith/byway/detail.html"


class BywayCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Byway
    fields = [
        "name",
        "description",
        "parent",
        "danger_level",
        "stability",
        "origin",
        "destination",
        "travel_time",
        "maelstrom_proximity",
        "spectral_activity",
        "has_waystation",
        "patrolled",
        "haunted",
    ]
    template_name = "locations/wraith/byway/form.html"
    success_message = "Byway '{name}' created successfully!"
    error_message = "Failed to create byway. Please correct the errors below."


class BywayUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Byway
    fields = [
        "name",
        "description",
        "parent",
        "danger_level",
        "stability",
        "origin",
        "destination",
        "travel_time",
        "maelstrom_proximity",
        "spectral_activity",
        "has_waystation",
        "patrolled",
        "haunted",
    ]
    template_name = "locations/wraith/byway/form.html"
    success_message = "Byway '{name}' updated successfully!"
    error_message = "Failed to update byway. Please correct the errors below."


class BywayListView(ListView):
    model = Byway
    ordering = ["name"]
    template_name = "locations/wraith/byway/list.html"
