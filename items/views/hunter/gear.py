from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.hunter import HunterGear


class HunterGearDetailView(DetailView):
    model = HunterGear
    template_name = "items/hunter/gear/detail.html"


class HunterGearListView(ListView):
    model = HunterGear
    ordering = ["name"]
    template_name = "items/hunter/gear/list.html"


class HunterGearCreateView(MessageMixin, CreateView):
    model = HunterGear
    fields = [
        "name",
        "description",
        "gear_type",
        "damage",
        "range",
        "rate",
        "capacity",
        "concealability",
        "availability",
        "legality",
        "requires_training",
    ]
    template_name = "items/hunter/gear/form.html"
    success_message = "Hunter Gear '{name}' created successfully!"
    error_message = "Failed to create gear. Please correct the errors below."


class HunterGearUpdateView(MessageMixin, UpdateView):
    model = HunterGear
    fields = [
        "name",
        "description",
        "gear_type",
        "damage",
        "range",
        "rate",
        "capacity",
        "concealability",
        "availability",
        "legality",
        "requires_training",
    ]
    template_name = "items/hunter/gear/form.html"
    success_message = "Hunter Gear '{name}' updated successfully!"
    error_message = "Failed to update gear. Please correct the errors below."
