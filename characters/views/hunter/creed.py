from characters.models.hunter import Creed
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class CreedDetailView(DetailView):
    model = Creed
    template_name = "characters/hunter/creed/detail.html"


class CreedCreateView(MessageMixin, CreateView):
    model = Creed
    fields = [
        "name",
        "primary_virtue",
        "philosophy",
        "nickname",
        "description",
        "favored_edges",
    ]
    template_name = "characters/hunter/creed/form.html"
    success_message = "Creed created successfully."
    error_message = "There was an error creating the Creed."


class CreedUpdateView(MessageMixin, UpdateView):
    model = Creed
    fields = [
        "name",
        "primary_virtue",
        "philosophy",
        "nickname",
        "description",
        "favored_edges",
    ]
    template_name = "characters/hunter/creed/form.html"
    success_message = "Creed updated successfully."
    error_message = "There was an error updating the Creed."


class CreedListView(ListView):
    model = Creed
    ordering = ["name"]
    template_name = "characters/hunter/creed/list.html"
