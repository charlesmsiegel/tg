from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.hunter import HuntingGround


class HuntingGroundDetailView(ViewPermissionMixin, DetailView):
    model = HuntingGround
    template_name = "locations/hunter/huntingground/detail.html"


class HuntingGroundListView(ListView):
    model = HuntingGround
    ordering = ["name"]
    template_name = "locations/hunter/huntingground/list.html"


class HuntingGroundCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = HuntingGround
    fields = [
        "name",
        "contained_within",
        "description",
        "size",
        "population",
        "supernatural_activity",
        "primary_threat",
        "threat_description",
        "is_contested",
        "control_level",
        "contact_network",
        "surveillance_coverage",
        "last_incident",
        "incident_log",
        "key_locations",
    ]
    template_name = "locations/hunter/huntingground/form.html"
    success_message = "Hunting Ground '{name}' created successfully!"
    error_message = "Failed to create hunting ground. Please correct the errors below."


class HuntingGroundUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = HuntingGround
    fields = [
        "name",
        "contained_within",
        "description",
        "size",
        "population",
        "supernatural_activity",
        "primary_threat",
        "threat_description",
        "is_contested",
        "control_level",
        "contact_network",
        "surveillance_coverage",
        "last_incident",
        "incident_log",
        "key_locations",
    ]
    template_name = "locations/hunter/huntingground/form.html"
    success_message = "Hunting Ground '{name}' updated successfully!"
    error_message = "Failed to update hunting ground. Please correct the errors below."
