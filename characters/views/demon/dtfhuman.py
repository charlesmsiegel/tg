from characters.models.demon import DtFHuman
from core.mixins import (
    ApprovedUserContextMixin,
    EditPermissionMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from core.views.message_mixin import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView


class DtFHumanDetailView(ApprovedUserContextMixin, ViewPermissionMixin, DetailView):
    model = DtFHuman
    template_name = "characters/demon/dtfhuman/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DtFHumanCreateView(MessageMixin, CreateView):
    model = DtFHuman
    success_message = "DtF Human created successfully."
    error_message = "Error creating DtF Human."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "intuition",
        "leadership",
        "seduction",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "performance",
        "security",
        "survival",
        "technology",
        "animal_ken",
        "demolitions",
        "academics",
        "computer",
        "finance",
        "investigation",
        "law",
        "enigmas",
        "medicine",
        "occult",
        "politics",
        "religion",
        "research",
        "science",
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/demon/dtfhuman/form.html"


class DtFHumanUpdateView(ApprovedUserContextMixin, EditPermissionMixin, UpdateView):
    model = DtFHuman
    success_message = "DtF Human updated successfully."
    error_message = "Error updating DtF Human."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "intuition",
        "leadership",
        "seduction",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "performance",
        "security",
        "survival",
        "technology",
        "animal_ken",
        "demolitions",
        "academics",
        "computer",
        "finance",
        "investigation",
        "law",
        "enigmas",
        "medicine",
        "occult",
        "politics",
        "religion",
        "research",
        "science",
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/demon/dtfhuman/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
