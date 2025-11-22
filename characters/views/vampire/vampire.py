from typing import Any

from characters.models.vampire.vampire import Vampire
from characters.views.core.human import HumanDetailView
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, ListView, UpdateView


class VampireDetailView(ApprovedUserContextMixin, HumanDetailView):
    model = Vampire
    template_name = "characters/vampire/vampire/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["disciplines"] = self.object.get_disciplines()
        if self.object.clan:
            context["clan_disciplines"] = self.object.get_clan_disciplines()
        return context


class VampireCreateView(MessageMixin, CreateView):
    model = Vampire
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "clan",
        "sect",
        "sire",
        "generation_rating",
        "path",
    ]
    template_name = "characters/vampire/vampire/form.html"
    success_message = "Vampire '{name}' created successfully!"
    error_message = "Failed to create vampire. Please correct the errors below."


class VampireUpdateView(MessageMixin, UpdateView):
    model = Vampire
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "clan",
        "sect",
        "sire",
        "generation_rating",
        "blood_pool",
        "humanity",
        "path",
        "path_rating",
        "willpower",
        "current_willpower",
        "conscience",
        "self_control",
        "courage",
        "conviction",
        "instinct",
        # Disciplines
        "celerity",
        "fortitude",
        "potence",
        "auspex",
        "dominate",
        "dementation",
        "presence",
        "animalism",
        "protean",
        "obfuscate",
        "chimerstry",
        "necromancy",
        "obtenebration",
        "quietus",
        "serpentis",
        "thaumaturgy",
        "vicissitude",
        "daimoinon",
        "melpominee",
        "mytherceria",
        "obeah",
        "temporis",
        "thanatosis",
        "valeren",
        "visceratika",
    ]
    template_name = "characters/vampire/vampire/form.html"
    success_message = "Vampire '{name}' updated successfully!"
    error_message = "Failed to update vampire. Please correct the errors below."


class VampireListView(ListView):
    model = Vampire
    ordering = ["name"]
    template_name = "characters/vampire/vampire/list.html"
