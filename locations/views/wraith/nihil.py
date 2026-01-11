from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from locations.models.wraith import Nihil


class NihilDetailView(ViewPermissionMixin, DetailView):
    model = Nihil
    template_name = "locations/wraith/nihil/detail.html"


class NihilCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Nihil
    fields = [
        "name",
        "description",
        "contained_within",
        "void_type",
        "stability",
        "hazard_level",
        "oblivion_proximity",
        "entropy_rating",
        "estimated_size",
        "corpus_drain",
        "pathos_drain",
        "memory_loss",
        "shadow_attraction",
        "avoidable",
        "marked",
        "spectral_activity",
        "contains_relics",
        "origin_story",
    ]
    template_name = "locations/wraith/nihil/form.html"
    success_message = "Nihil '{name}' created successfully!"
    error_message = "Failed to create nihil. Please correct the errors below."


class NihilUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Nihil
    fields = [
        "name",
        "description",
        "contained_within",
        "void_type",
        "stability",
        "hazard_level",
        "oblivion_proximity",
        "entropy_rating",
        "estimated_size",
        "corpus_drain",
        "pathos_drain",
        "memory_loss",
        "shadow_attraction",
        "avoidable",
        "marked",
        "spectral_activity",
        "contains_relics",
        "origin_story",
    ]
    template_name = "locations/wraith/nihil/form.html"
    success_message = "Nihil '{name}' updated successfully!"
    error_message = "Failed to update nihil. Please correct the errors below."


class NihilListView(ListView):
    model = Nihil
    ordering = ["name"]
    template_name = "locations/wraith/nihil/list.html"
