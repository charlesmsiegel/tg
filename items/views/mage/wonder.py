from typing import Any

from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.forms.mage.wonder import WonderForm
from items.models.mage import Wonder, WonderResonanceRating


class WonderDetailView(DetailView):
    model = Wonder
    template_name = "items/mage/wonder/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(
            wonder=self.object
        ).order_by("resonance__name")
        return context


class WonderListView(ListView):
    model = Wonder
    ordering = ["name"]
    template_name = "items/mage/wonder/list.html"


class WonderCreateView(MessageMixin, CreateView):
    form_class = WonderForm
    template_name = "items/mage/wonder/form.html"
    success_message = "Wonder '{name}' created successfully!"
    error_message = "Failed to create wonder. Please correct the errors below."


class WonderUpdateView(MessageMixin, UpdateView):
    form_class = WonderForm
    template_name = "items/mage/wonder/form.html"
    success_message = "Wonder '{name}' updated successfully!"
    error_message = "Failed to update wonder. Please correct the errors below."
