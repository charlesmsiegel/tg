from characters.models.vampire.path import Path
from core.mixins import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import CreateView, DetailView, ListView, UpdateView


@method_decorator([vary_on_cookie, cache_page(60 * 15)], name="dispatch")
class PathDetailView(LoginRequiredMixin, DetailView):
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


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class PathListView(ListView):
    model = Path
    ordering = ["name"]
    template_name = "characters/vampire/path/list.html"
