from characters.models.changeling.house import House
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class HouseDetailView(DetailView):
    model = House
    template_name = "characters/changeling/house/detail.html"


class HouseCreateView(MessageMixin, CreateView):
    model = House
    fields = ["name", "description", "court", "boon", "flaw"]
    template_name = "characters/changeling/house/form.html"
    success_message = "House created successfully."
    error_message = "There was an error creating the House."


class HouseUpdateView(MessageMixin, UpdateView):
    model = House
    fields = ["name", "description", "court", "boon", "flaw"]
    template_name = "characters/changeling/house/form.html"
    success_message = "House updated successfully."
    error_message = "There was an error updating the House."


class HouseListView(ListView):
    model = House
    ordering = ["name"]
    template_name = "characters/changeling/house/list.html"
