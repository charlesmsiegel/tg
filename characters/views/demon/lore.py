from characters.models.demon import Lore
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class LoreDetailView(DetailView):
    model = Lore
    template_name = "characters/demon/lore/detail.html"


class LoreCreateView(MessageMixin, CreateView):
    model = Lore
    fields = [
        "name",
        "description",
        "property_name",
        "houses",
    ]
    template_name = "characters/demon/lore/form.html"
    success_message = "Lore created successfully."
    error_message = "There was an error creating the Lore."


class LoreUpdateView(MessageMixin, UpdateView):
    model = Lore
    fields = [
        "name",
        "description",
        "property_name",
        "houses",
    ]
    template_name = "characters/demon/lore/form.html"
    success_message = "Lore updated successfully."
    error_message = "There was an error updating the Lore."


class LoreListView(ListView):
    model = Lore
    ordering = ["name"]
    template_name = "characters/demon/lore/list.html"
