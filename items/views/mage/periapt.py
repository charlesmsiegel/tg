from typing import Any

from core.mixins import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.mage import Periapt, WonderResonanceRating


class PeriaptDetailView(DetailView):
    model = Periapt
    template_name = "items/mage/periapt/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(wonder=self.object).order_by(
            "resonance__name"
        )
        return context


class PeriaptListView(ListView):
    model = Periapt
    ordering = ["name"]
    template_name = "items/mage/periapt/list.html"


class PeriaptCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Periapt
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "power",
        "arete",
        "max_charges",
        "current_charges",
        "is_consumable",
    ]
    template_name = "items/mage/periapt/form.html"
    success_message = "Periapt '{name}' created successfully!"
    error_message = "Failed to create Periapt. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form


class PeriaptUpdateView(MessageMixin, UpdateView):
    model = Periapt
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "power",
        "arete",
        "max_charges",
        "current_charges",
        "is_consumable",
    ]
    template_name = "items/mage/periapt/form.html"
    success_message = "Periapt '{name}' updated successfully!"
    error_message = "Failed to update Periapt. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form
