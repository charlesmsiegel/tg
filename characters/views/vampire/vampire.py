from typing import Any

from characters.models.vampire.vampire import Vampire
from characters.views.core.human import HumanDetailView
from django.views.generic import CreateView, ListView, UpdateView


class VampireDetailView(HumanDetailView):
    model = Vampire
    template_name = "characters/vampire/vampire/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        context["disciplines"] = self.object.get_disciplines()
        if self.object.clan:
            context["clan_disciplines"] = self.object.get_clan_disciplines()
        return context


class VampireCreateView(CreateView):
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


class VampireUpdateView(UpdateView):
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


class VampireListView(ListView):
    model = Vampire
    ordering = ["name"]
    template_name = "characters/vampire/vampire/list.html"
