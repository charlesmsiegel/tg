from characters.models.werewolf.battlescar import BattleScar
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class BattleScarDetailView(DetailView):
    model = BattleScar
    template_name = "characters/werewolf/battlescar/detail.html"


class BattleScarCreateView(MessageMixin, CreateView):
    model = BattleScar
    fields = ["name", "description", "glory"]
    template_name = "characters/werewolf/battlescar/form.html"
    success_message = "Battle Scar created successfully."
    error_message = "There was an error creating the Battle Scar."


class BattleScarUpdateView(MessageMixin, UpdateView):
    model = BattleScar
    fields = ["name", "description", "glory"]
    template_name = "characters/werewolf/battlescar/form.html"
    success_message = "Battle Scar updated successfully."
    error_message = "There was an error updating the Battle Scar."


class BattleScarListView(ListView):
    model = BattleScar
    ordering = ["name"]
    template_name = "characters/werewolf/battlescar/list.html"
