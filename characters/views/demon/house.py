from characters.models.demon import DemonHouse
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class DemonHouseDetailView(DetailView):
    model = DemonHouse
    template_name = "characters/demon/house/detail.html"


class DemonHouseCreateView(MessageMixin, CreateView):
    model = DemonHouse
    fields = [
        "name",
        "description",
        "celestial_name",
        "starting_torment",
        "domain",
    ]
    template_name = "characters/demon/house/form.html"
    success_message = "Demon House created successfully."
    error_message = "There was an error creating the Demon House."


class DemonHouseUpdateView(MessageMixin, UpdateView):
    model = DemonHouse
    fields = [
        "name",
        "description",
        "celestial_name",
        "starting_torment",
        "domain",
    ]
    template_name = "characters/demon/house/form.html"
    success_message = "Demon House updated successfully."
    error_message = "There was an error updating the Demon House."


class DemonHouseListView(ListView):
    model = DemonHouse
    ordering = ["name"]
    template_name = "characters/demon/house/list.html"
