from characters.models.demon import DemonFaction
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class DemonFactionDetailView(DetailView):
    model = DemonFaction
    template_name = "characters/demon/faction/detail.html"


class DemonFactionCreateView(MessageMixin, CreateView):
    model = DemonFaction
    fields = [
        "name",
        "description",
        "philosophy",
        "goal",
        "leadership",
        "tactics",
    ]
    template_name = "characters/demon/faction/form.html"
    success_message = "Demon Faction created successfully."
    error_message = "There was an error creating the Demon Faction."


class DemonFactionUpdateView(MessageMixin, UpdateView):
    model = DemonFaction
    fields = [
        "name",
        "description",
        "philosophy",
        "goal",
        "leadership",
        "tactics",
    ]
    template_name = "characters/demon/faction/form.html"
    success_message = "Demon Faction updated successfully."
    error_message = "There was an error updating the Demon Faction."


class DemonFactionListView(ListView):
    model = DemonFaction
    ordering = ["name"]
    template_name = "characters/demon/faction/list.html"
