from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.wraith.haunt import Haunt


class HauntDetailView(ViewPermissionMixin, DetailView):
    model = Haunt
    template_name = "locations/wraith/haunt/detail.html"


class HauntCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Haunt
    fields = [
        "name",
        "description",
        "contained_within",
        "rank",
        "shroud_rating",
        "haunt_type",
        "haunt_size",
        "faith_resonance",
        "attracts_ghosts",
    ]
    template_name = "locations/wraith/haunt/form.html"
    success_message = "Haunt '{name}' created successfully!"
    error_message = "Failed to create haunt. Please correct the errors below."


class HauntUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Haunt
    fields = [
        "name",
        "description",
        "contained_within",
        "rank",
        "shroud_rating",
        "haunt_type",
        "haunt_size",
        "faith_resonance",
        "attracts_ghosts",
    ]
    template_name = "locations/wraith/haunt/form.html"
    success_message = "Haunt '{name}' updated successfully!"
    error_message = "Failed to update haunt. Please correct the errors below."


class HauntListView(ListView):
    model = Haunt
    ordering = ["name"]
    template_name = "locations/wraith/haunt/list.html"
