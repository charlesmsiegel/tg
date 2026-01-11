from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.mage.fellowship import SorcererFellowship
from core.mixins import MessageMixin


class SorcererFellowshipDetailView(DetailView):
    model = SorcererFellowship
    template_name = "characters/mage/fellowship/detail.html"


class SorcererFellowshipCreateView(MessageMixin, CreateView):
    model = SorcererFellowship
    fields = ["name", "description", "favored_attributes", "favored_paths"]
    template_name = "characters/mage/fellowship/form.html"
    success_message = "Sorcerer Fellowship created successfully."
    error_message = "There was an error creating the Sorcerer Fellowship."


class SorcererFellowshipUpdateView(MessageMixin, UpdateView):
    model = SorcererFellowship
    fields = ["name", "description", "favored_attributes", "favored_paths"]
    template_name = "characters/mage/fellowship/form.html"
    success_message = "Sorcerer Fellowship updated successfully."
    error_message = "There was an error updating the Sorcerer Fellowship."


class SorcererFellowshipListView(ListView):
    model = SorcererFellowship
    ordering = ["name"]
    template_name = "characters/mage/fellowship/list.html"
