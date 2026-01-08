from characters.models.wraith.faction import WraithFaction
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class WraithFactionDetailView(DetailView):
    model = WraithFaction
    template_name = "characters/wraith/faction/detail.html"


class WraithFactionCreateView(MessageMixin, CreateView):
    model = WraithFaction
    fields = ["name", "description", "faction_type", "parent"]
    template_name = "characters/wraith/faction/form.html"
    success_message = "Wraith Faction created successfully."
    error_message = "There was an error creating the Wraith Faction."


class WraithFactionUpdateView(MessageMixin, UpdateView):
    model = WraithFaction
    fields = ["name", "description", "faction_type", "parent"]
    template_name = "characters/wraith/faction/form.html"
    success_message = "Wraith Faction updated successfully."
    error_message = "There was an error updating the Wraith Faction."


class WraithFactionListView(ListView):
    model = WraithFaction
    ordering = ["faction_type", "name"]
    template_name = "characters/wraith/faction/list.html"
