from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.wraith.faction import WraithFaction
from core.mixins import MessageMixin


@method_decorator(cache_page(60 * 15), name="dispatch")
class WraithFactionDetailView(DetailView):
    model = WraithFaction
    template_name = "characters/wraith/faction/detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("subfactions")


class WraithFactionCreateView(MessageMixin, CreateView):
    model = WraithFaction
    fields = ["name", "description", "faction_type", "parent"]
    template_name = "characters/wraith/faction/form.html"
    success_message = "Wraith Faction created successfully."
    error_message = "There was an error creating the Wraith Faction."


class WraithFactionUpdateView(MessageMixin, UpdateView):
    model = WraithFaction
    fields = ["name", "description", "faction_type", "parent"]
    template_name = "characters/wraith/faction/form.html"
    success_message = "Wraith Faction updated successfully."
    error_message = "There was an error updating the Wraith Faction."


@method_decorator(cache_page(60 * 15), name="dispatch")
class WraithFactionListView(ListView):
    model = WraithFaction
    ordering = ["faction_type", "name"]
    template_name = "characters/wraith/faction/list.html"
