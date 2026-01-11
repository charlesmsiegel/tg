from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.vampire.title import VampireTitle
from core.mixins import MessageMixin


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class VampireTitleDetailView(DetailView):
    model = VampireTitle
    template_name = "characters/vampire/title/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["sect"] = self.object.sect
        return context


class VampireTitleCreateView(MessageMixin, CreateView):
    model = VampireTitle
    fields = [
        "name",
        "description",
        "sect",
        "value",
        "is_negative",
        "powers",
    ]
    template_name = "characters/vampire/title/form.html"
    success_message = "Vampire Title created successfully."
    error_message = "There was an error creating the Vampire Title."


class VampireTitleUpdateView(MessageMixin, UpdateView):
    model = VampireTitle
    fields = [
        "name",
        "description",
        "sect",
        "value",
        "is_negative",
        "powers",
    ]
    template_name = "characters/vampire/title/form.html"
    success_message = "Vampire Title updated successfully."
    error_message = "There was an error updating the Vampire Title."


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class VampireTitleListView(ListView):
    model = VampireTitle
    ordering = ["-value", "name"]
    template_name = "characters/vampire/title/list.html"
