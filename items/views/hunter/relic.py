from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.hunter import HunterRelic


class HunterRelicDetailView(DetailView):
    model = HunterRelic
    template_name = "items/hunter/relic/detail.html"


class HunterRelicListView(ListView):
    model = HunterRelic
    ordering = ["name"]
    template_name = "items/hunter/relic/list.html"


class HunterRelicCreateView(MessageMixin, CreateView):
    model = HunterRelic
    fields = [
        "name",
        "description",
        "power_level",
        "background_cost",
        "is_blessed",
        "is_cursed",
        "requires_faith",
        "is_unique",
        "powers",
        "activation_cost",
        "origin",
        "limitations",
    ]
    template_name = "items/hunter/relic/form.html"
    success_message = "Hunter Relic '{name}' created successfully!"
    error_message = "Failed to create relic. Please correct the errors below."


class HunterRelicUpdateView(MessageMixin, UpdateView):
    model = HunterRelic
    fields = [
        "name",
        "description",
        "power_level",
        "background_cost",
        "is_blessed",
        "is_cursed",
        "requires_faith",
        "is_unique",
        "powers",
        "activation_cost",
        "origin",
        "limitations",
    ]
    template_name = "items/hunter/relic/form.html"
    success_message = "Hunter Relic '{name}' updated successfully!"
    error_message = "Failed to update relic. Please correct the errors below."
