from characters.models.werewolf.rite import Rite
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class RiteDetailView(DetailView):
    model = Rite
    template_name = "characters/werewolf/rite/detail.html"


class RiteCreateView(MessageMixin, CreateView):
    model = Rite
    fields = ["name", "level", "rite_type", "description"]
    template_name = "characters/werewolf/rite/form.html"
    success_message = "Rite created successfully."
    error_message = "There was an error creating the Rite."


class RiteUpdateView(MessageMixin, UpdateView):
    model = Rite
    fields = ["name", "level", "rite_type", "description"]
    template_name = "characters/werewolf/rite/form.html"
    success_message = "Rite updated successfully."
    error_message = "There was an error updating the Rite."


class RiteListView(ListView):
    model = Rite
    ordering = ["name"]
    template_name = "characters/werewolf/rite/list.html"
