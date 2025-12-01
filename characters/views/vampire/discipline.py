from characters.models.vampire.discipline import Discipline
from core.mixins import MessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
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


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class DisciplineListView(ListView):
    model = Discipline
    ordering = ["name"]
    template_name = "characters/vampire/discipline/list.html"
