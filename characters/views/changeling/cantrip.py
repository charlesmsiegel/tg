from characters.models.changeling.cantrip import Cantrip
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class CantripDetailView(DetailView):
    model = Cantrip
    template_name = "characters/changeling/cantrip/detail.html"


class CantripCreateView(MessageMixin, CreateView):
    model = Cantrip
    fields = [
        "name",
        "art",
        "primary_realm",
        "level",
        "difficulty",
        "glamour_cost",
        "duration",
        "range",
        "effect",
        "type_of_effect",
    ]
    template_name = "characters/changeling/cantrip/form.html"
    success_message = "Cantrip created successfully."
    error_message = "There was an error creating the Cantrip."


class CantripUpdateView(MessageMixin, UpdateView):
    model = Cantrip
    fields = [
        "name",
        "art",
        "primary_realm",
        "level",
        "difficulty",
        "glamour_cost",
        "duration",
        "range",
        "effect",
        "type_of_effect",
    ]
    template_name = "characters/changeling/cantrip/form.html"
    success_message = "Cantrip updated successfully."
    error_message = "There was an error updating the Cantrip."


class CantripListView(ListView):
    model = Cantrip
    ordering = ["art", "level", "name"]
    template_name = "characters/changeling/cantrip/list.html"
