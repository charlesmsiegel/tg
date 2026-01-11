from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.forms.changeling.house_faction import HouseFactionForm
from characters.models.changeling.house_faction import HouseFaction
from core.mixins import MessageMixin


class HouseFactionDetailView(DetailView):
    model = HouseFaction
    template_name = "characters/changeling/house_faction/detail.html"


class HouseFactionCreateView(MessageMixin, CreateView):
    model = HouseFaction
    form_class = HouseFactionForm
    template_name = "characters/changeling/house_faction/form.html"
    success_message = "House Faction created successfully."
    error_message = "There was an error creating the House Faction."


class HouseFactionUpdateView(MessageMixin, UpdateView):
    model = HouseFaction
    form_class = HouseFactionForm
    template_name = "characters/changeling/house_faction/form.html"
    success_message = "House Faction updated successfully."
    error_message = "There was an error updating the House Faction."


class HouseFactionListView(ListView):
    model = HouseFaction
    ordering = ["name"]
    template_name = "characters/changeling/house_faction/list.html"
