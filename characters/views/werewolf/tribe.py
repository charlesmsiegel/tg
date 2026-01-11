from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.werewolf.tribe import Tribe
from core.mixins import MessageMixin


class TribeDetailView(DetailView):
    model = Tribe
    template_name = "characters/werewolf/tribe/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TribeCreateView(MessageMixin, CreateView):
    model = Tribe
    fields = ["name", "willpower", "description"]
    template_name = "characters/werewolf/tribe/form.html"
    success_message = "Tribe created successfully."
    error_message = "There was an error creating the Tribe."


class TribeUpdateView(MessageMixin, UpdateView):
    model = Tribe
    fields = ["name", "willpower", "description"]
    template_name = "characters/werewolf/tribe/form.html"
    success_message = "Tribe updated successfully."
    error_message = "There was an error updating the Tribe."


class TribeListView(ListView):
    model = Tribe
    ordering = ["name"]
    template_name = "characters/werewolf/tribe/list.html"
