from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.core import Archetype
from core.mixins import MessageMixin


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class ArchetypeDetailView(DetailView):
    model = Archetype
    template_name = "characters/core/archetype/detail.html"


class ArchetypeCreateView(MessageMixin, CreateView):
    model = Archetype
    fields = ["name", "description"]
    template_name = "characters/core/archetype/form.html"
    success_message = "Archetype '{name}' created successfully!"
    error_message = "Failed to create Archetype. Please correct the errors below."


class ArchetypeUpdateView(MessageMixin, UpdateView):
    model = Archetype
    fields = ["name", "description"]
    template_name = "characters/core/archetype/form.html"
    success_message = "Archetype '{name}' updated successfully!"
    error_message = "Failed to update Archetype. Please correct the errors below."


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class ArchetypeListView(ListView):
    model = Archetype
    ordering = ["name"]
    template_name = "characters/core/archetype/list.html"
