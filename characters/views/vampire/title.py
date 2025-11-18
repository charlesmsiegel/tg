from typing import Any

from characters.models.vampire.title import VampireTitle
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class VampireTitleDetailView(DetailView):
    model = VampireTitle
    template_name = "characters/vampire/title/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.object.sect:
            context["sect"] = self.object.sect
        return context


class VampireTitleCreateView(CreateView):
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


class VampireTitleUpdateView(UpdateView):
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


class VampireTitleListView(ListView):
    model = VampireTitle
    ordering = ["-value", "name"]
    template_name = "characters/vampire/title/list.html"
