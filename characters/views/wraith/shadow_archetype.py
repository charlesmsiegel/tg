from characters.models.wraith.shadow_archetype import ShadowArchetype
from core.mixins import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class ShadowArchetypeDetailView(DetailView):
    model = ShadowArchetype
    template_name = "characters/wraith/shadow_archetype/detail.html"


class ShadowArchetypeCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = ShadowArchetype
    fields = [
        "name",
        "description",
        "point_cost",
        "core_function",
        "modus_operandi",
        "dominance_behavior",
        "effect_on_psyche",
        "strengths",
        "weaknesses",
    ]
    template_name = "characters/wraith/shadow_archetype/form.html"
    success_message = "Shadow Archetype created successfully."
    error_message = "There was an error creating the Shadow Archetype."


class ShadowArchetypeUpdateView(LoginRequiredMixin, MessageMixin, UpdateView):
    model = ShadowArchetype
    fields = [
        "name",
        "description",
        "point_cost",
        "core_function",
        "modus_operandi",
        "dominance_behavior",
        "effect_on_psyche",
        "strengths",
        "weaknesses",
    ]
    template_name = "characters/wraith/shadow_archetype/form.html"
    success_message = "Shadow Archetype updated successfully."
    error_message = "There was an error updating the Shadow Archetype."


class ShadowArchetypeListView(ListView):
    model = ShadowArchetype
    ordering = ["point_cost", "name"]
    template_name = "characters/wraith/shadow_archetype/list.html"
