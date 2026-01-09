from characters.models.wraith.shadow_archetype import ShadowArchetype
from core.mixins import MessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView


@method_decorator(cache_page(60 * 15), name="dispatch")
class ShadowArchetypeDetailView(DetailView):
    model = ShadowArchetype
    template_name = "characters/wraith/shadow_archetype/detail.html"


class ShadowArchetypeCreateView(MessageMixin, CreateView):
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


class ShadowArchetypeUpdateView(MessageMixin, UpdateView):
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


@method_decorator(cache_page(60 * 15), name="dispatch")
class ShadowArchetypeListView(ListView):
    model = ShadowArchetype
    ordering = ["point_cost", "name"]
    template_name = "characters/wraith/shadow_archetype/list.html"
