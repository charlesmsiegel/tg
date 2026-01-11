from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.demon import Ritual
from core.mixins import MessageMixin


class RitualDetailView(DetailView):
    model = Ritual
    template_name = "characters/demon/ritual/detail.html"


class RitualCreateView(MessageMixin, CreateView):
    model = Ritual
    fields = [
        "name",
        "description",
        "house",
        "primary_lore",
        "primary_lore_rating",
        "secondary_lore_requirements",
        "base_cost",
        "restrictions",
        "minimum_casting_time",
        "system",
        "torment_effect",
        "variations",
        "flavor_text",
        "source_page",
    ]
    template_name = "characters/demon/ritual/form.html"
    success_message = "Ritual created successfully."
    error_message = "There was an error creating the Ritual."


class RitualUpdateView(MessageMixin, UpdateView):
    model = Ritual
    fields = [
        "name",
        "description",
        "house",
        "primary_lore",
        "primary_lore_rating",
        "secondary_lore_requirements",
        "base_cost",
        "restrictions",
        "minimum_casting_time",
        "system",
        "torment_effect",
        "variations",
        "flavor_text",
        "source_page",
    ]
    template_name = "characters/demon/ritual/form.html"
    success_message = "Ritual updated successfully."
    error_message = "There was an error updating the Ritual."


class RitualListView(ListView):
    model = Ritual
    ordering = ["name"]
    template_name = "characters/demon/ritual/list.html"
