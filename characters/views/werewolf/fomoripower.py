from characters.models.werewolf.fomoripower import FomoriPower
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class FomoriPowerDetailView(DetailView):
    model = FomoriPower
    template_name = "characters/werewolf/fomoripower/detail.html"


class FomoriPowerCreateView(MessageMixin, CreateView):
    model = FomoriPower
    fields = ["name", "description"]
    template_name = "characters/werewolf/fomoripower/form.html"
    success_message = "Fomori Power created successfully."
    error_message = "There was an error creating the Fomori Power."


class FomoriPowerUpdateView(MessageMixin, UpdateView):
    model = FomoriPower
    fields = ["name", "description"]
    template_name = "characters/werewolf/fomoripower/form.html"
    success_message = "Fomori Power updated successfully."
    error_message = "There was an error updating the Fomori Power."


class FomoriPowerListView(ListView):
    model = FomoriPower
    ordering = ["name"]
    template_name = "characters/werewolf/fomoripower/list.html"
