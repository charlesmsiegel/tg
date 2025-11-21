from characters.models.changeling.kith import Kith
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class KithDetailView(DetailView):
    model = Kith
    template_name = "characters/changeling/kith/detail.html"


class KithCreateView(MessageMixin, CreateView):
    model = Kith
    fields = ["name", "description", "affinity", "frailty"]
    template_name = "characters/changeling/kith/form.html"
    success_message = "Kith created successfully."
    error_message = "There was an error creating the Kith."


class KithUpdateView(MessageMixin, UpdateView):
    model = Kith
    fields = ["name", "description", "affinity", "frailty"]
    template_name = "characters/changeling/kith/form.html"
    success_message = "Kith updated successfully."
    error_message = "There was an error updating the Kith."


class KithListView(ListView):
    model = Kith
    ordering = ["name"]
    template_name = "characters/changeling/kith/list.html"
