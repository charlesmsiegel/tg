from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.changeling.chimera import Chimera
from core.mixins import MessageMixin


class ChimeraDetailView(DetailView):
    model = Chimera
    template_name = "characters/changeling/chimera/detail.html"


class ChimeraCreateView(MessageMixin, CreateView):
    model = Chimera
    fields = [
        "name",
        "chimera_type",
        "chimera_points",
        "sentience_level",
        "behavior",
        "appearance",
        "durability",
        "can_interact_with_physical",
        "loyalty",
        "creator",
        "origin",
        "is_permanent",
        "dream_source",
    ]
    template_name = "characters/changeling/chimera/form.html"
    success_message = "Chimera created successfully."
    error_message = "There was an error creating the Chimera."


class ChimeraUpdateView(MessageMixin, UpdateView):
    model = Chimera
    fields = [
        "name",
        "chimera_type",
        "chimera_points",
        "sentience_level",
        "behavior",
        "appearance",
        "durability",
        "can_interact_with_physical",
        "loyalty",
        "creator",
        "origin",
        "is_permanent",
        "dream_source",
    ]
    template_name = "characters/changeling/chimera/form.html"
    success_message = "Chimera updated successfully."
    error_message = "There was an error updating the Chimera."


class ChimeraListView(ListView):
    model = Chimera
    ordering = ["name"]
    template_name = "characters/changeling/chimera/list.html"
