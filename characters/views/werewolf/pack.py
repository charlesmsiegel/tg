from characters.models.werewolf.pack import Pack
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, UpdateView


class PackDetailView(DetailView):
    model = Pack
    template_name = "characters/werewolf/pack/detail.html"


class PackCreateView(MessageMixin, CreateView):
    model = Pack
    fields = ["name", "description", "members", "leader", "totem"]
    template_name = "characters/werewolf/pack/form.html"
    success_message = "Pack created successfully."
    error_message = "There was an error creating the Pack."


class PackUpdateView(MessageMixin, UpdateView):
    model = Pack
    fields = ["name", "description", "members", "leader", "totem"]
    template_name = "characters/werewolf/pack/form.html"
    success_message = "Pack updated successfully."
    error_message = "There was an error updating the Pack."
