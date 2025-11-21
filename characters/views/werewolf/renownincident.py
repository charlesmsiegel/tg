from characters.models.werewolf.renownincident import RenownIncident
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class RenownIncidentDetailView(DetailView):
    model = RenownIncident
    template_name = "characters/werewolf/renownincident/detail.html"


class RenownIncidentCreateView(MessageMixin, CreateView):
    model = RenownIncident
    fields = [
        "name",
        "description",
        "glory",
        "honor",
        "wisdom",
        "posthumous",
        "only_once",
        "breed",
        "rite",
    ]
    template_name = "characters/werewolf/renownincident/form.html"
    success_message = "Renown Incident created successfully."
    error_message = "There was an error creating the Renown Incident."


class RenownIncidentUpdateView(MessageMixin, UpdateView):
    model = RenownIncident
    fields = [
        "name",
        "description",
        "glory",
        "honor",
        "wisdom",
        "posthumous",
        "only_once",
        "breed",
        "rite",
    ]
    template_name = "characters/werewolf/renownincident/form.html"
    success_message = "Renown Incident updated successfully."
    error_message = "There was an error updating the Renown Incident."


class RenownIncidentListView(ListView):
    model = RenownIncident
    ordering = ["name"]
    template_name = "characters/werewolf/renownincident/list.html"
