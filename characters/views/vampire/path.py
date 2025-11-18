from characters.models.vampire.path import Path
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class PathDetailView(DetailView):
    model = Path
    template_name = "characters/vampire/path/detail.html"


class PathCreateView(CreateView):
    model = Path
    fields = [
        "name",
        "description",
        "virtues_required",
        "ethics",
    ]
    template_name = "characters/vampire/path/form.html"


class PathUpdateView(UpdateView):
    model = Path
    fields = [
        "name",
        "description",
        "virtues_required",
        "ethics",
    ]
    template_name = "characters/vampire/path/form.html"


class PathListView(ListView):
    model = Path
    ordering = ["name"]
    template_name = "characters/vampire/path/list.html"
