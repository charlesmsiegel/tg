from characters.models.vampire.discipline import Discipline
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class DisciplineDetailView(DetailView):
    model = Discipline
    template_name = "characters/vampire/discipline/detail.html"


class DisciplineCreateView(MessageMixin, CreateView):
    model = Discipline
    fields = [
        "name",
        "property_name",
    ]
    template_name = "characters/vampire/discipline/form.html"
    success_message = "Discipline created successfully."
    error_message = "There was an error creating the Discipline."


class DisciplineUpdateView(MessageMixin, UpdateView):
    model = Discipline
    fields = [
        "name",
        "property_name",
    ]
    template_name = "characters/vampire/discipline/form.html"
    success_message = "Discipline updated successfully."
    error_message = "There was an error updating the Discipline."


class DisciplineListView(ListView):
    model = Discipline
    ordering = ["name"]
    template_name = "characters/vampire/discipline/list.html"
