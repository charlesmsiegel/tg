from typing import Any

from characters.models.vampire.ghoul import Ghoul
from characters.views.core.human import HumanDetailView
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, ListView, UpdateView
from core.mixins import ApprovedUserContextMixin


class GhoulDetailView(ApprovedUserContextMixin, HumanDetailView):
    model = Ghoul
    template_name = "characters/vampire/ghoul/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["disciplines"] = self.object.get_disciplines()
        return context


class GhoulCreateView(MessageMixin, CreateView):
    model = Ghoul
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "domitor",
        "is_independent",
    ]
    template_name = "characters/vampire/ghoul/form.html"
    success_message = "Ghoul created successfully."
    error_message = "Error creating ghoul."


class GhoulUpdateView(MessageMixin, UpdateView):
    model = Ghoul
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "domitor",
        "is_independent",
        "blood_pool",
        "max_blood_pool",
        "years_as_ghoul",
        # Disciplines
        "potence",
        "celerity",
        "fortitude",
        "auspex",
        "dominate",
        "obfuscate",
        "presence",
    ]
    template_name = "characters/vampire/ghoul/form.html"
    success_message = "Ghoul updated successfully."
    error_message = "Error updating ghoul."


class GhoulListView(ListView):
    model = Ghoul
    ordering = ["name"]
    template_name = "characters/vampire/ghoul/list.html"
