from typing import Any

from characters.models.vampire.revenant import Revenant
from characters.views.core.human import HumanDetailView
from core.mixins import MessageMixin
from django.views.generic import CreateView, ListView, UpdateView


class RevenantDetailView(HumanDetailView):
    model = Revenant
    template_name = "characters/vampire/revenant/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["disciplines"] = self.object.get_disciplines()
        context["family_disciplines"] = self.object.get_family_disciplines()
        return context


class RevenantCreateView(MessageMixin, CreateView):
    model = Revenant
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "family",
        "pseudo_generation",
    ]
    template_name = "characters/vampire/revenant/form.html"
    success_message = "Revenant created successfully."
    error_message = "Error creating revenant."


class RevenantUpdateView(MessageMixin, UpdateView):
    model = Revenant
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "family",
        "pseudo_generation",
        "blood_pool",
        "max_blood_pool",
        "actual_age",
        "apparent_age",
        "family_flaw",
        # Disciplines
        "potence",
        "celerity",
        "fortitude",
        "auspex",
        "dominate",
        "obfuscate",
        "presence",
        "animalism",
        "necromancy",
        "vicissitude",
    ]
    template_name = "characters/vampire/revenant/form.html"
    success_message = "Revenant updated successfully."
    error_message = "Error updating revenant."


class RevenantListView(ListView):
    model = Revenant
    ordering = ["name"]
    template_name = "characters/vampire/revenant/list.html"
