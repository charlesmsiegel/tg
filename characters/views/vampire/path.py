from characters.models.vampire.path import Path
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class PathDetailView(DetailView):
    model = Path
    template_name = "characters/vampire/path/detail.html"


class PathCreateView(MessageMixin, CreateView):
    model = Path
    fields = [
        "name",
        "description",
        "requires_conviction",
        "requires_instinct",
        "ethics",
    ]
    template_name = "characters/vampire/path/form.html"
    success_message = "Path created successfully."
    error_message = "There was an error creating the Path."


class PathUpdateView(MessageMixin, UpdateView):
    model = Path
    fields = [
        "name",
        "description",
        "requires_conviction",
        "requires_instinct",
        "ethics",
    ]
    template_name = "characters/vampire/path/form.html"
    success_message = "Path updated successfully."
    error_message = "There was an error updating the Path."


class PathListView(ListView):
    model = Path
    ordering = ["name"]
    template_name = "characters/vampire/path/list.html"
