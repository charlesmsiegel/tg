from core.mixins import (
    EditPermissionMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.wraith.necropolis import Necropolis


class NecropolisDetailView(ViewPermissionMixin, DetailView):
    model = Necropolis
    template_name = "locations/wraith/necropolis/detail.html"


class NecropolisCreateView(LoginRequiredMixin, CreateView):
    model = Necropolis
    fields = [
        "name",
        "description",
        "parent",
        "region",
        "population",
        "deathlord",
    ]
    template_name = "locations/wraith/necropolis/form.html"
    success_message = "Necropolis '{name}' created successfully!"
    error_message = "Failed to create necropolis. Please correct the errors below."


class NecropolisUpdateView(EditPermissionMixin, UpdateView):
    model = Necropolis
    fields = [
        "name",
        "description",
        "parent",
        "region",
        "population",
        "deathlord",
    ]
    template_name = "locations/wraith/necropolis/form.html"
    success_message = "Necropolis '{name}' updated successfully!"
    error_message = "Failed to update necropolis. Please correct the errors below."


class NecropolisListView(ListView):
    model = Necropolis
    ordering = ["name"]
    template_name = "locations/wraith/necropolis/list.html"
